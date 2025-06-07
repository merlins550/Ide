"""Persona-Driven Analysis Platform (PDAP) prototype.

This module implements a very small subset of the features
described in V2.txt. It provides:

- A `Persona` class that loads/saves JSON persona definitions.
- A naive `Retriever` that selects relevant text snippets from a
  persona's knowledge base.
- A `WorkflowOrchestrator` that selects personas for a user idea and
  generates simple responses using an LLM (OpenAI if configured,
  otherwise a fallback dummy response).

The goal is to demonstrate how personas and retrieval could be wired
into the existing project without a full implementation.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import glob
import argparse

PERSONA_DIR = os.path.join(os.path.dirname(__file__), "personas")

try:
    from openai import OpenAI
except Exception:  # OpenAI package may not be installed in every env
    OpenAI = None  # type: ignore


@dataclass
class Persona:
    persona_id: str
    name: str
    expertise_domains: List[str]
    data_sources: List[Dict[str, str]]
    linguistic_profile: Dict[str, str]
    knowledge: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, path: str) -> "Persona":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)


import logging

def load_personas(directory: str = PERSONA_DIR) -> List[Persona]:
    """Load all persona JSON files from the given directory."""
    personas: List[Persona] = []
    for path in sorted(glob.glob(os.path.join(directory, "*.json"))):
        try:
            personas.append(Persona.load(path))
        except Exception as e:
            logging.error(f"Failed to load persona from {path}: {e}", exc_info=True)
            continue
    return personas


class Retriever:
    """Very small text retriever based on keyword matching."""

    def __init__(self, persona: Persona):
        self.persona = persona

    def search(self, query: str, k: int = 3) -> List[str]:
        """Return up to ``k`` knowledge snippets related to the query."""
        results = []
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        for text in self.persona.knowledge:
            if pattern.search(text):
                results.append(text)
            if len(results) >= k:
                break
        return results


class LLMWrapper:
    """Simple wrapper around OpenAI or a dummy fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key and OpenAI else None

    def chat(self, prompt: str) -> str:
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                return response.choices[0].message.content
            except Exception as exc:  # pragma: no cover - network issues
                return f"[LLM error: {exc}]"
        # Fallback response when no API key is provided
        return f"[dummy LLM] {prompt[:100]}..."


class WorkflowOrchestrator:
    """Select personas, retrieve context and generate answers."""

    def __init__(
        self,
        personas: List[Persona],
        llm: Optional[LLMWrapper] = None,
        parallel: bool = False,
    ) -> None:
        self.personas = personas
        self.llm = llm or LLMWrapper()
        self.parallel = parallel

    def select_personas(self, idea: str) -> List[Persona]:
        idea_lower = idea.lower()
        selected = [
            persona
            for persona in self.personas
            if any(
                domain.lower() in idea_lower
                for domain in persona.expertise_domains
            )
        ]
        return selected or self.personas[:1]

    def run(self, idea: str) -> Dict[str, str]:
        outputs: Dict[str, str] = {}
        accumulated: str = ""
        import tiktoken

        # Set a safe context token limit (e.g., 3000 for a 4096-token model)
        MAX_CONTEXT_TOKENS = 3000
        enc = tiktoken.encoding_for_model(getattr(self.llm, "model_name", "gpt-3.5-turbo"))

        def truncate_context(text, max_tokens):
            tokens = enc.encode(text)
            if len(tokens) <= max_tokens:
                return text
            truncated = enc.decode(tokens[-max_tokens:])
            return truncated

        for persona in self.select_personas(idea):
            retriever = Retriever(persona)
            snippets = retriever.search(idea)
            persona_context = "\n".join(snippets)
            context = persona_context if self.parallel else (accumulated + ("\n" if accumulated else "") + persona_context)
            # Truncate context if it exceeds the token limit
            context = truncate_context(context, MAX_CONTEXT_TOKENS)
            prompt = (
                f"You are {persona.name}. Using the following context, "
                f"analyze the idea: '{idea}'.\nContext:\n{context}"
            )
            response = self.llm.chat(prompt)
            outputs[persona.name] = response
            if not self.parallel:
                accumulated += f"\n[{persona.name}] {response}"
        return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PDAP workflow")
    parser.add_argument("idea", help="Idea to analyze")
    parser.add_argument(
        "--persona-dir",
        default=PERSONA_DIR,
        help="Directory containing persona JSON files",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Analyze with personas independently instead of chaining",
    )
    args = parser.parse_args()

    personas = load_personas(args.persona_dir)
    if not personas:
        raise SystemExit(f"No personas found in {args.persona_dir}")

    orchestrator = WorkflowOrchestrator(personas, parallel=args.parallel)
    results = orchestrator.run(args.idea)
    for persona_name, output in results.items():
        print(f"\n=== {persona_name} ===\n{output}\n")
