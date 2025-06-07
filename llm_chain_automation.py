# llm_chain_automation.py
# LLM zincir otomasyonu için backend mantığını içerir.
# ToolUserAgent entegrasyonu eklendi.

import os
from openai import OpenAI
from smol_agent_tools import ToolUserAgent # Yeni ajan sınıfını import et

class LLMChainAutomation:
    def __init__(self, api_key=None):
        """
        LLMChainAutomation sınıfının başlatıcısı.
        OpenAI istemcisini ve ToolUserAgent'ı başlatır.
        """
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("UYARI: OpenAI API anahtarı ayarlanmamış. Lütfen OPENAI_API_KEY ortam değişkenini ayarlayın veya doğrudan iletin.")
            # API anahtarı olmadan API çağrıları başarısız olacaktır.
            # Gösterim amacıyla devam edilecek, ancak geçerli bir anahtar olmadan LLM çağrıları çalışmayacaktır.
            self.openai_client = None # veya sahte bir istemci
        else:
            self.openai_client = OpenAI(api_key=self.api_key)

        self.tool_agent = ToolUserAgent(llm_client=self.openai_client) # ToolUserAgent'ı başlat
        self.chain_history = [] # Her aşamanın çıktılarını bağlam yönetimi için saklar

    def _call_llm(self, model, prompt, temperature=0.7, max_tokens=1000):
        """
        Belirtilen LLM modeline bir çağrı yapar.
        """
        if not self.openai_client:
            print("HATA: OpenAI istemcisi başlatılmamış (API anahtarı eksik olabilir). LLM çağrısı yapılamıyor.")
            return "Hata: OpenAI istemcisi yapılandırılamadı."
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM çağrısı sırasında hata: {e}")
            return f"Hata: İstek işlenemedi. {e}"

    def _summarize_context(self, history, max_tokens=300):
        """
        Sonraki LLM'ler için bağlamı korumak amacıyla zincir geçmişini özetler.
        Bu basitleştirilmiş bir özettir. Gerçek bir sistemde, daha akıllı özetleme için
        özel bir LLM kullanılabilir.
        """
        full_context = "\n".join(history)
        # Basitçe token sayısını kelime sayısıyla tahmin ediyoruz.
        if len(full_context.split()) > max_tokens:
            summary_prompt = f"Aşağıdaki metni anahtar fikirlere ve gelişmelere odaklanarak yaklaşık {max_tokens} token ile kısaca özetle:\n\n{full_context}"
            # Özetleme için de bir LLM çağrısı gerekiyor.
            return self._call_llm("gpt-3.5-turbo", summary_prompt, temperature=0.3, max_tokens=max_tokens)
        return full_context

    def run_chain(self, initial_idea, chain_config=None):
        """
        LLM zincir otomasyon sürecini çalıştırır.
        chain_config: Her biri bir aşamayı tanımlayan sözlüklerin bir listesi.
                      Örn: [{'name': 'Aşama Adı', 'type': 'llm_call'/'agent_task', 'model': 'gpt-4', ...}]
        """
        self.chain_history = [] # Yeni bir çalıştırma için geçmişi sıfırla
        current_input_for_stage = initial_idea # Aşama için işlenecek mevcut girdi
        
        # Sağlanmazsa varsayılan zincir yapılandırması (gösterim amaçlı)
        if chain_config is None:
            chain_config = [
                {
                    'name': 'Fikir Genişletme',
                    'type': 'llm_call', # Aşama türü: LLM çağrısı
                    'model': 'gpt-3.5-turbo', 
                    'prompt_template': "Aşağıdaki fikri genişlet, daha fazla ayrıntı, potansiyel özellikler ve ilk kullanım senaryoları sağla:\n\nFikir: {input}\n\nGenişletilmiş Kavram:",
                    'temperature': 0.7,
                    'max_tokens': 1000
                },
                {
                    'name': 'Konu Araştırma Ajanı',
                    'type': 'agent_task', # Aşama türü: Ajan görevi
                    'model': 'gpt-3.5-turbo', # Ajan çıktısını işlemek veya ajanı yönlendirmek için LLM
                    'task_description_template': "Şu konu hakkında güncel bilgileri web'de araştır: {topic_from_previous_stage}",
                    # 'input_mapping': {'topic_from_previous_stage': 'previous_output.summary'}, # Daha karmaşık eşleme için örnek
                    'available_tools': ["web_search"], # Bu ajan için mevcut araçlar
                    'output_format_prompt': "Ajanın web araştırması bulgularını ({agent_output}) kullanarak, konuyu özetleyen kısa bir rapor oluştur." # Ajan çıktısını işlemek için prompt
                },
                {
                    'name': 'Piyasa Uyumu ve Sonraki Adımlar',
                    'type': 'llm_call',
                    'model': 'gpt-4o', 
                    'prompt_template': "Aşağıdaki kavram, analiz ve araştırma sonuçlarına dayanarak potansiyel pazar uyumunu değerlendir. Bu fikri uygulanabilir bir projeye dönüştürmek için somut sonraki adımlar öner; potansiyel hedef kitleler, ilk pazarlama fikirleri ve temel geliştirme kilometre taşları dahil.\n\nKavram, Analiz ve Araştırma: {input}\n\nPiyasa Uyumu ve Sonraki Adımlar:",
                    'temperature': 0.6,
                    'max_tokens': 1500
                }
            ]

        results = {}
        
        for i, stage in enumerate(chain_config):
            print(f"\n--- Çalıştırılan Aşama {i+1}: {stage['name']} ---")
            
            stage_type = stage.get('type', 'llm_call') # Varsayılan tür 'llm_call'
            stage_output = ""

            if stage_type == 'llm_call':
                prompt = stage['prompt_template'].format(input=current_input_for_stage)
                
                # İlk aşama değilse ve geçmiş varsa, bağlamı ekle
                if i > 0:
                    context_for_llm = self._summarize_context(self.chain_history)
                    if context_for_llm:
                        prompt = f"Önceki bağlam ve gelişmeler:\n{context_for_llm}\n\n{prompt}"

                stage_output = self._call_llm(
                    model=stage['model'],
                    prompt=prompt,
                    temperature=stage.get('temperature', 0.7),
                    max_tokens=stage.get('max_tokens', 1000)
                )

            elif stage_type == 'agent_task':
                # Ajan görevi için task_description oluştur
                # Şimdilik basitçe bir önceki aşamanın çıktısını {topic_from_previous_stage} yerine koyuyoruz
                task_description = stage['task_description_template'].format(topic_from_previous_stage=current_input_for_stage)
                
                agent_raw_output = self.tool_agent.execute_task(
                    task_description=task_description,
                    available_tools=stage.get('available_tools', ["web_search", "calculator"])
                )
                
                # İsteğe bağlı: Ajanın ham çıktısını bir LLM ile işle
                if 'output_format_prompt' in stage:
                    formatting_prompt = stage['output_format_prompt'].format(agent_output=agent_raw_output)
                    if i > 0 : # Önceki bağlamı ekle
                        context_for_llm = self._summarize_context(self.chain_history)
                        if context_for_llm:
                            formatting_prompt = f"Önceki bağlam ve gelişmeler:\n{context_for_llm}\n\n{formatting_prompt}"
                    
                    stage_output = self._call_llm(
                        model=stage.get('model', 'gpt-3.5-turbo'), # Aşamada belirtilen modeli veya varsayılanı kullan
                        prompt=formatting_prompt,
                        temperature=stage.get('temperature', 0.5), # Farklı bir sıcaklık olabilir
                        max_tokens=stage.get('max_tokens', 800)    # Farklı bir token limiti olabilir
                    )
                else:
                    stage_output = agent_raw_output # Formatlama prompt'u yoksa ham çıktıyı kullan
            
            current_input_for_stage = stage_output # Bir sonraki aşamanın girdisi, bu aşamanın çıktısıdır
            self.chain_history.append(f"Aşama {i+1} ({stage['name']}) Çıktısı:\n{stage_output}")
            results[stage['name']] = stage_output
            print(f"Aşama {i+1} Çıktısı (ilk 500 karakter):\n{str(stage_output)[:500]}...")

        return results

if __name__ == "__main__":
    # Örnek Kullanım:
    # OpenAI API anahtarınızı bir ortam değişkeni olarak ayarlayın veya doğrudan iletin
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
    
    # API anahtarının ayarlandığından emin olun.
    # Gösterim için, placeholder olsa bile devam edeceğiz.
    # Gerçek bir senaryoda, geçerli bir anahtarın mevcut olduğundan emin olmak istersiniz.
    
    automation = LLMChainAutomation() # API anahtarını ortam değişkeninden almayı dener
    
    # Ajan görevi içeren özel bir zincirle test et
    custom_chain_config_for_test = [
        {
            'name': 'İlk Fikir Tanımlama',
            'type': 'llm_call',
            'model': 'gpt-3.5-turbo',
            'prompt_template': "Verilen fikir için üç anahtar zorluk ve üç potansiyel fayda belirle: {input}",
            'temperature': 0.6,
            'max_tokens': 600
        },
        {
            'name': 'Rakip Araştırma Ajanı',
            'type': 'agent_task',
            'model': 'gpt-3.5-turbo', # Ajan çıktısını işlemek için LLM
            'task_description_template': "Şu konuyla ilgili başlıca rakipleri web'de araştır: {topic_from_previous_stage}",
            # 'input_mapping': ... (bir önceki aşamadan gelen çıktının hangi kısmının topic_from_previous_stage olacağını belirtebilir)
            'available_tools': ["web_search"],
            'output_format_prompt': "Ajanın web araştırması bulgularına ({agent_output}) dayanarak, bulunan rakipler hakkında kısa bir özet sun."
        },
        {
            'name': 'Stratejik Özet',
            'type': 'llm_call',
            'model': 'gpt-4o',
            'prompt_template': "İlk fikir tanımlaması ve rakip araştırma özetini dikkate alarak, şu konu için bir sonraki adımları içeren kısa bir stratejik plan oluştur: {input}",
            'temperature': 0.5,
            'max_tokens': 1000
        }
    ]
    
    test_initial_idea = "kişiye özel öğrenme platformları"
    print(f"Test için Başlangıç Fikri: {test_initial_idea}")
    
    final_project_results = automation.run_chain(test_initial_idea, chain_config=custom_chain_config_for_test)
    
    print("\n--- Nihai Proje Çıktısı ---")
    if final_project_results:
        for stage_name, output_content in final_project_results.items():
            print(f"\n{stage_name}:\n{output_content}")
    else:
        print("Zincir çalıştırılırken bir sorun oluştu veya çıktı üretilemedi.")
