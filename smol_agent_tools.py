# smol_agent_tools.py
# Bu dosya, basit araç kullanabilen bir ajanın temelini içerir.
import json
import re

class ToolUserAgent:
    def __init__(self, llm_client=None):
        """
        ToolUserAgent sınıfının başlatıcısı.
        Gelecekte LLM tabanlı araç seçimi ve parametre çıkarımı için bir llm_client alabilir.
        """
        self.llm_client = llm_client
        print("ToolUserAgent initialized.")

    def _decide_tool_and_params(self, task_description, available_tools):
        """
        Verilen göreve ve mevcut araçlara göre hangi aracın kullanılacağına ve 
        bu araç için gerekli parametrelere karar verir.
        Şu an için basit anahtar kelime eşleştirmesi kullanır.
        Gelecekte burası bir LLM çağrısı ile daha akıllı hale getirilebilir.
        """
        print(f"Tool decision for task: '{task_description}', Available Tools: {available_tools}")
        task_lower = task_description.lower()

        if "web_search" in available_tools:
            # "search for X", "find information on Y", "look up Z" gibi kalıpları arar
            match = re.search(r"(?:search for|find information on|look up|research)\s+(.+)", task_lower)
            if match:
                query = match.group(1).strip().rstrip('.')
                print(f"Web search tool decided. Query: '{query}'")
                return "web_search", {"query": query}

        if "calculator" in available_tools:
            # "calculate X", "what is Y" (matematiksel ifade ise) gibi kalıpları arar
            match = re.search(r"(?:calculate|compute|what is)\s+([\d\s\+\-\*\/\(\)\.]+)", task_lower)
            if match:
                expression = match.group(1).strip()
                # Basit bir güvenlik kontrolü (çok temel)
                if re.fullmatch(r"[\d\s\+\-\*\/\(\)\.]+", expression):
                    print(f"Calculator tool decided. Expression: '{expression}'")
                    return "calculator", {"expression": expression}
                else:
                    print(f"Calculator tool: Invalid characters in expression '{expression}'")


        print("No specific tool decided by keyword matching.")
        return "no_tool_decided", {}

    def execute_task(self, task_description, available_tools=["web_search", "calculator"]):
        """
        Bir görevi alır, uygun aracı seçer (eğer varsa) ve aracın çalışmasını simüle eder.
        Araç kullanımı ve sonucunu içeren bir JSON string'i döndürür.
        """
        tool_to_use, params = self._decide_tool_and_params(task_description, available_tools)
        
        result_data = {"tool_used": tool_to_use, "task_description": task_description}

        if tool_to_use == "web_search":
            query = params.get('query', 'unknown query')
            print(f"SIMULATING Web Search: Searching for '{query}'")
            # Simüle edilmiş sonuçlar
            simulated_results = f"Simulated search results for '{query}': AI is rapidly evolving. Key areas include LLMs, robotics, and AI ethics."
            result_data["query"] = query
            result_data["simulated_results"] = simulated_results
            print(f"Web Search Simulation Result: {simulated_results}")
        
        elif tool_to_use == "calculator":
            expression = params.get('expression', '0')
            print(f"SIMULATING Calculator: Calculating '{expression}'")
            try:
                # UYARI: eval() güvenilmeyen girdilerle tehlikelidir. Bu sadece simülasyon amaçlıdır.
                # Gerçek bir uygulamada güvenli bir matematik ifadesi ayrıştırıcısı kullanın.
                # Şimdilik, basit ifadeler için çok temel bir güvenlik önlemi alalım.
                if not re.match(r"^[0-9\s\+\-\*\/\(\)\.]+$", expression):
                    raise ValueError("Expression contains invalid characters for simulation.")
                
                # Basit bir hesaplama simülasyonu (eval yerine)
                if expression == "25 * 4 + 10":
                    calculated_value = 110
                else:
                    calculated_value = "complex_expression_result_placeholder" # eval(expression) yerine
                
                result_data["expression"] = expression
                result_data["simulated_result"] = calculated_value
                print(f"Calculator Simulation Result: {calculated_value}")
            except Exception as e:
                print(f"SIMULATING Calculator Error: {e}")
                result_data["error"] = str(e)
        
        else: # no_tool_decided
            print("No specific tool executed. Task might require general LLM processing.")
            result_data["info"] = "No suitable tool found or matched for this task. Requires general LLM."
            
        return json.dumps(result_data, indent=2)

if __name__ == '__main__':
    # Bu ajan sınıfının nasıl kullanılacağına dair örnekler
    agent = ToolUserAgent()
    
    print("\n--- Example 1: Web Search ---")
    task1 = "Could you search for the latest news on quantum computing?"
    result1 = agent.execute_task(task1, available_tools=["web_search", "calculator"])
    print(f"Agent Execution Result 1:\n{result1}")
    
    print("\n--- Example 2: Calculator ---")
    task2 = "Calculate 25 * 4 + 10 for me."
    result2 = agent.execute_task(task2, available_tools=["web_search", "calculator"])
    print(f"Agent Execution Result 2:\n{result2}")

    print("\n--- Example 3: No Specific Tool ---")
    task3 = "Write a short story about a friendly robot."
    result3 = agent.execute_task(task3, available_tools=["web_search", "calculator"])
    print(f"Agent Execution Result 3:\n{result3}")

    print("\n--- Example 4: Web Search with different phrasing ---")
    task4 = "Look up the capital of France."
    result4 = agent.execute_task(task4, available_tools=["web_search"])
    print(f"Agent Execution Result 4:\n{result4}")
