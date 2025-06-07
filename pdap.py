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
        if self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

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

    def __init__(self, personas: List[Persona], llm: Optional[LLMWrapper] = None):
        self.personas = personas
        self.llm = llm or LLMWrapper()

    def select_personas(self, idea: str) -> List[Persona]:
        idea_lower = idea.lower()
        selected = []
        for persona in self.personas:
            if any(domain.lower() in idea_lower for domain in persona.expertise_domains):
                selected.append(persona)
        return selected or self.personas[:1]

    def run(self, idea: str) -> Dict[str, str]:
        outputs = {}
        for persona in self.select_personas(idea):
            retriever = Retriever(persona)
            snippets = retriever.search(idea)
            context = "\n".join(snippets)
            prompt = (
                f"You are {persona.name}. Using the following context, "
                f"analyze the idea: '{idea}'.\nContext:\n{context}"
            )
            outputs[persona.name] = self.llm.chat(prompt)
        return outputs


if __name__ == "__main__":
    # Example personas bundled with minimal knowledge
    einstein = Persona(
        persona_id="einstein_001",
        name="Albert Einstein",
        expertise_domains=["physics", "relativity", "mathematics"],
        data_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Albert_Einstein"}],
        linguistic_profile={"style": "thoughtful"},
        knowledge=[
            "Einstein developed the theory of relativity.",
            "He was awarded the 1921 Nobel Prize in Physics.",
        ],
    )

    tesla = Persona(
        persona_id="tesla_001",
        name="Nikola Tesla",
        expertise_domains=["engineering", "electricity", "energy"],
        data_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Nikola_Tesla"}],
        linguistic_profile={"style": "innovative"},
        knowledge=[
            "Tesla pioneered alternating current systems.",
            "He explored wireless transmission of electricity.",
        ],
    )

    orchestrator = WorkflowOrchestrator([einstein, tesla])
    user_idea = input("Enter your idea: ")
    results = orchestrator.run(user_idea)
    for persona_name, output in results.items():
        print(f"\n=== {persona_name} ===\n{output}\n")
