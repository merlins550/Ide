# toplantı.py
# Conference Room ana GUI uygulaması.
# LLMChainAutomation entegrasyonu ve yeni ajan aşaması için UI güncellemeleri içerir.

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox # messagebox eklendi
import os
from llm_chain_automation import LLMChainAutomation # LLM otomasyon sınıfımızı import et

# Genel görünüm ayarları
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class ConferenceRoomApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere yapılandırması
        self.title("Conference Room")
        self.geometry("1350x900") # Boyut biraz daha artırıldı
        self.minsize(1000, 750)   # Minimum boyutlar da artırıldı

        # Renkler (start.py - NexusFlow'dan esinlenerek)
        self.COLOR_GRADIENT_START = "#6e8efb"
        self.COLOR_GRADIENT_END = "#a777e3"
        self.COLOR_BACKGROUND = "#F9FAFB"      
        self.COLOR_SURFACE = "#FFFFFF"         
        self.COLOR_TEXT_PRIMARY = "#1F2937"    
        self.COLOR_TEXT_SECONDARY = "#4B5563"  
        self.COLOR_TEXT_TERTIARY = "#6B7280"   
        self.COLOR_TEXT_ACCENT = "#4F46E5"     
        self.COLOR_BUTTON_HOVER = "#F3F4F6"    
        self.COLOR_BUTTON_ACTIVE_BG = "#EEF2FF" 
        self.COLOR_BORDER = "#E5E7EB"          
        self.COLOR_INPUT_BG = "#FFFFFF"
        self.COLOR_INPUT_BORDER = "#D1D5DB"    
        self.COLOR_ASSISTANT_BUBBLE_BG = self.COLOR_SURFACE
        self.COLOR_USER_BUBBLE_BG = "#EEF2FF"  
        self.COLOR_STATUS_GREEN_TEXT = "#065F46" 
        self.COLOR_STATUS_GREEN_BG = "#D1FAE5"   
        self.COLOR_STATUS_YELLOW_TEXT = "#92400E" 
        self.COLOR_STATUS_YELLOW_BG = "#FEF3C7"   
        self.COLOR_STATUS_BLUE_TEXT = "#1E40AF"   
        self.COLOR_STATUS_BLUE_BG = "#DBEAFE"     
        self.COLOR_PROGRESS_INFO_TEXT = "#1D4ED8" 
        self.COLOR_PROGRESS_INFO_BG = "#EFF6FF"

        # Fontlar
        self.FONT_FAMILY = "Segoe UI Variable" 
        self.FONT_BOLD = (self.FONT_FAMILY, 13, "bold")
        self.FONT_NORMAL = (self.FONT_FAMILY, 12)
        self.FONT_MEDIUM_WEIGHT = (self.FONT_FAMILY, 12, "normal") 
        self.FONT_SMALL = (self.FONT_FAMILY, 10)
        self.FONT_SMALL_MEDIUM = (self.FONT_FAMILY, 10, "normal")
        self.FONT_TITLE = (self.FONT_FAMILY, 18, "bold") 
        self.FONT_H1 = (self.FONT_FAMILY, 16, "bold")    
        self.FONT_H2 = (self.FONT_FAMILY, 14, "bold")    
        self.FONT_H3 = (self.FONT_FAMILY, 12, "bold")    

        self.current_view_name = "chat"
        self.llm_automation = LLMChainAutomation()
        
        # Zincir aşamalarını saklamak için bir liste (UI'da yönetilecek)
        self.chain_stages_ui_data = [] 

        self.setup_ui()
        self.show_chat_view()

    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND)
        self.main_container.pack(fill="both", expand=True)
        self.create_sidebar()
        self.create_main_content_area()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.main_container, width=64, fg_color=self.COLOR_SURFACE, corner_radius=0, border_width=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        logo_bg = ctk.CTkFrame(self.sidebar, width=40, height=40, fg_color=self.COLOR_GRADIENT_START, corner_radius=10)
        logo_bg.pack(pady=(20, 30), padx=12)
        logo_icon = ctk.CTkLabel(logo_bg, text="🔗", font=(self.FONT_FAMILY, 20, "bold"), text_color=self.COLOR_SURFACE)
        logo_icon.place(relx=0.5, rely=0.5, anchor="center")
        self.nav_buttons_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_buttons_frame.pack(expand=False, pady=10)
        self.sidebar_buttons = {}
        self.sidebar_buttons["chat"] = self._create_sidebar_button(self.nav_buttons_frame, "💬", "Sohbet", self.show_chat_view)
        self.sidebar_buttons["chain"] = self._create_sidebar_button(self.nav_buttons_frame, "⛓️", "Zincir Ayarları", self.show_chain_config_view_from_sidebar)
        self.sidebar_buttons["history"] = self._create_sidebar_button(self.nav_buttons_frame, "🕒", "Geçmiş", self.show_history_view)
        self.settings_btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.settings_btn_frame.pack(side="bottom", fill="x", pady=(0,20))
        self.sidebar_buttons["settings"] = self._create_sidebar_button(self.settings_btn_frame, "⚙️", "Ayarlar", self.show_settings_view)

    def _create_sidebar_button(self, parent, icon_text, tooltip_text, command):
        button = ctk.CTkButton(parent, text=icon_text, width=48, height=48, fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY, hover_color=self.COLOR_BUTTON_HOVER, font=ctk.CTkFont(family=self.FONT_FAMILY, size=22), corner_radius=10, command=command)
        button.pack(pady=6, padx=8)
        self._create_tooltip(button, tooltip_text)
        return button

    def _update_sidebar_active_state(self):
        for key, button in self.sidebar_buttons.items():
            button.configure(fg_color=self.COLOR_BUTTON_ACTIVE_BG if key == self.current_view_name else "transparent", 
                             text_color=self.COLOR_TEXT_ACCENT if key == self.current_view_name else self.COLOR_TEXT_TERTIARY)

    def _create_tooltip(self, widget, text):
        tooltip = None
        def enter(event):
            nonlocal tooltip
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + widget.winfo_width() + 5 
            y += widget.winfo_rooty() + (widget.winfo_height() // 2) - 10
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{int(x)}+{int(y)}")
            label = tk.Label(tooltip, text=text, background="#2D3748", foreground="white", relief="solid", borderwidth=1, padx=6, pady=3, font=(self.FONT_FAMILY, 9))
            label.pack()
        def leave(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def create_main_content_area(self):
        self.main_content_frame = ctk.CTkFrame(self.main_container, fg_color=self.COLOR_BACKGROUND, corner_radius=0)
        self.main_content_frame.pack(side="right", fill="both", expand=True)
        self.header_frame = ctk.CTkFrame(self.main_content_frame, height=65, fg_color=self.COLOR_SURFACE, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        ctk.CTkFrame(self.header_frame, height=1, fg_color=self.COLOR_BORDER, corner_radius=0).pack(side="bottom", fill="x")
        self.title_label = ctk.CTkLabel(self.header_frame, text="Conference Room", font=self.FONT_TITLE, text_color=self.COLOR_TEXT_PRIMARY)
        self.title_label.pack(side="left", padx=24, pady=18)
        self.header_right_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_right_frame.pack(side="right", padx=24, pady=12)
        self.new_session_btn = ctk.CTkButton(self.header_right_frame, text="Yeni Oturum  +", font=(self.FONT_FAMILY, 11, "normal"), text_color=self.COLOR_TEXT_SECONDARY, fg_color=self.COLOR_BUTTON_HOVER, hover_color="#E5E7EB", corner_radius=16, height=36, width=130, command=self.new_session)
        self.new_session_btn.pack(side="left", padx=(0,16))
        self.user_icon_bg = ctk.CTkFrame(self.header_right_frame, width=36, height=36, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=18)
        self.user_icon_bg.pack(side="left")
        self.user_icon_bg.pack_propagate(False)
        ctk.CTkLabel(self.user_icon_bg, text="👤", font=(self.FONT_FAMILY, 18), text_color=self.COLOR_TEXT_ACCENT).place(relx=0.5, rely=0.5, anchor="center")
        self.view_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True, padx=0, pady=0)
        self._chat_view_frame = None
        self._settings_view_frame = None
        self._chain_view_frame = None
        self._history_view_frame = None
        self._build_chat_view()
        self._build_settings_view()
        self._build_placeholder_views()

    def _build_chat_view(self):
        self._chat_view_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        self.chat_messages_scrollable = ctk.CTkScrollableFrame(self._chat_view_frame, fg_color="transparent", scrollbar_button_color=self.COLOR_GRADIENT_START, scrollbar_button_hover_color=self.COLOR_GRADIENT_END)
        self.chat_messages_scrollable.pack(fill="both", expand=True, padx=24, pady=(20,0))
        self.add_assistant_message("Conference Room'a hoş geldiniz! Ben sizin LLM zincir otomasyon asistanınızım. Fikrinizi veya sorunuzu aşağıya girerek başlayın, optimize edilmiş LLM işlem hattımızda size rehberlik edeceğim.")
        self.add_user_message("Temel bir ürün fikrini alıp özel LLM'ler zinciri kullanarak eksiksiz bir iş planına dönüştüren otomatik bir sistem oluşturmak istiyorum.", idea_title="İlk Fikir")
        self.add_chain_response_message() # Varsayılan zinciri gösterir
        self.input_area_frame = ctk.CTkFrame(self._chat_view_frame, fg_color=self.COLOR_BACKGROUND, height=140)
        self.input_area_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        ctk.CTkFrame(self.input_area_frame, height=1, fg_color=self.COLOR_BORDER, corner_radius=0).pack(side="top", fill="x")
        input_content_wrapper = ctk.CTkFrame(self.input_area_frame, fg_color="transparent")
        input_content_wrapper.pack(pady=15, padx=24, fill="x")
        input_controls_frame = ctk.CTkFrame(input_content_wrapper, fg_color="transparent")
        input_controls_frame.pack(fill="x", expand=True)
        self.textbox_frame = ctk.CTkFrame(input_controls_frame, fg_color=self.COLOR_INPUT_BG, corner_radius=12, border_width=1, border_color=self.COLOR_INPUT_BORDER)
        self.textbox_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_textbox = ctk.CTkTextbox(self.textbox_frame, fg_color="transparent", text_color=self.COLOR_TEXT_SECONDARY, font=self.FONT_NORMAL, border_width=0, wrap="word", height=80)
        self.input_textbox.pack(fill="x", expand=True, padx=12, pady=(8,0))
        self.input_textbox.bind("<Return>", self.on_enter_key_send)
        toolbar_frame = ctk.CTkFrame(self.textbox_frame, fg_color="transparent", height=30)
        toolbar_frame.pack(fill="x", padx=12, pady=(2, 6))
        ctk.CTkFrame(toolbar_frame, height=1, fg_color=self.COLOR_BORDER, corner_radius=0).pack(side="top", fill="x")
        # ... (attachment, magic, advanced buttons) ...
        self.send_message_btn = ctk.CTkButton(input_controls_frame, text="➤", font=(self.FONT_FAMILY, 20), width=52, height=52, corner_radius=10, fg_color=self.COLOR_GRADIENT_START, hover_color=self.COLOR_GRADIENT_END, text_color=self.COLOR_SURFACE, command=self.send_message_from_ui)
        self.send_message_btn.pack(side="right", pady=(0,0))
        # ... (help text) ...

    def _build_settings_view(self):
        self._settings_view_frame = ctk.CTkFrame(self.view_container, fg_color=self.COLOR_SURFACE)
        settings_header_bar = ctk.CTkFrame(self._settings_view_frame, fg_color="transparent", height=60)
        settings_header_bar.pack(fill="x", padx=24, pady=(18,10))
        ctk.CTkFrame(settings_header_bar, height=1, fg_color=self.COLOR_BORDER, corner_radius=0).pack(side="bottom", fill="x")
        ctk.CTkLabel(settings_header_bar, text="Ayarlar & Yapılandırma", font=self.FONT_H1, text_color=self.COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(settings_header_bar, text="API anahtarlarınızı ve LLM zincir ayarlarınızı yönetin", font=(self.FONT_FAMILY, 11), text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w", pady=(2,0))
        settings_scrollable_content = ctk.CTkScrollableFrame(self._settings_view_frame, fg_color=self.COLOR_BACKGROUND, scrollbar_button_color=self.COLOR_GRADIENT_START)
        settings_scrollable_content.pack(fill="both", expand=True, padx=0, pady=0)
        settings_content_wrapper = ctk.CTkFrame(settings_scrollable_content, fg_color="transparent")
        settings_content_wrapper.pack(pady=24, padx=24, fill="x")
        self._create_api_keys_settings_section(settings_content_wrapper)
        self._create_chain_config_settings_section(settings_content_wrapper)
        # ... (Save/Reset buttons) ...

    def _create_api_keys_settings_section(self, parent):
        # ... (Mevcut API anahtarları bölümü kodu - değişiklik yok) ...
        api_keys_card = ctk.CTkFrame(parent, fg_color=self.COLOR_SURFACE, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        api_keys_card.pack(fill="x", pady=(0,20)) 
        api_keys_header_frame = ctk.CTkFrame(api_keys_card, fg_color=self.COLOR_BACKGROUND, corner_radius=0, height=60)
        api_keys_header_frame.pack(fill="x", padx=0, pady=0)
        ctk.CTkFrame(api_keys_header_frame, height=1, fg_color=self.COLOR_BORDER, corner_radius=0).pack(side="bottom", fill="x")
        api_keys_header_content = ctk.CTkFrame(api_keys_header_frame, fg_color="transparent")
        api_keys_header_content.pack(padx=20, pady=12, fill="both", expand=True)
        ctk.CTkLabel(api_keys_header_content, text="LLM Sağlayıcı API Anahtarları", font=self.FONT_H2, text_color=self.COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(api_keys_header_content, text="Zincirinizdeki farklı LLM sağlayıcılarına erişimi yapılandırın", font=(self.FONT_FAMILY, 10), text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w", pady=(2,0))
        providers_list_frame = ctk.CTkFrame(api_keys_card, fg_color="transparent")
        providers_list_frame.pack(fill="x", expand=True)
        # Örnek sağlayıcılar
        self._render_provider_settings_card(providers_list_frame, "OpenAI", "GPT-4, GPT-3.5 modelleri", "🤖", "Aktif", self.COLOR_STATUS_GREEN_TEXT, self.COLOR_STATUS_GREEN_BG, True, False, api_key_value="sk-********************", org_value="org-************")
        ctk.CTkFrame(providers_list_frame, height=1, fg_color=self.COLOR_BORDER).pack(fill="x", padx=20)
        self._render_provider_settings_card(providers_list_frame, "Ollama", "Yerel LLM modelleri", "💻", "Kendin Barındır", self.COLOR_STATUS_BLUE_TEXT, self.COLOR_STATUS_BLUE_BG, True, True, base_url_value="http://localhost:11434", model_value="Llama3", custom_model_name_value="llama3:latest", ollama_connected=True)
        # ... (Add provider button) ...


    def _render_provider_settings_card(self, parent, name, description, icon, status_text, status_color, status_bg_color, has_key=False, is_local=False, **kwargs):
        # ... (Mevcut sağlayıcı kartı render etme kodu - değişiklik yok) ...
        provider_entry_frame = ctk.CTkFrame(parent, fg_color="transparent")
        provider_entry_frame.pack(fill="x", padx=20, pady=(15,10))
        # ... (header, icon, name, desc, status, ellipsis) ...
        # ... (form fields for api key/url/model) ...
        # ... (status and test connection button) ...
        pass # Placeholder for brevity, assume this is filled from previous version


    def _create_chain_config_settings_section(self, parent):
        chain_config_card = ctk.CTkFrame(parent, fg_color=self.COLOR_SURFACE, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        chain_config_card.pack(fill="x", pady=(20,0))
        chain_header_frame = ctk.CTkFrame(chain_config_card, fg_color=self.COLOR_BACKGROUND, corner_radius=0, height=60)
        chain_header_frame.pack(fill="x")
        ctk.CTkFrame(chain_header_frame, height=1, fg_color=self.COLOR_BORDER, corner_radius=0).pack(side="bottom", fill="x")
        chain_header_content = ctk.CTkFrame(chain_header_frame, fg_color="transparent")
        chain_header_content.pack(padx=20, pady=12, fill="both", expand=True)
        ctk.CTkLabel(chain_header_content, text="LLM Zincir Yapılandırması", font=self.FONT_H2, text_color=self.COLOR_TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(chain_header_content, text="LLM işlem zinciriniz için sıralamayı ve parametreleri tanımlayın", font=(self.FONT_FAMILY, 10), text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w", pady=(2,0))
        
        chain_stages_outer_frame = ctk.CTkFrame(chain_config_card, fg_color="transparent")
        chain_stages_outer_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(chain_stages_outer_frame, text="Zincir Aşamaları", font=self.FONT_H3, text_color=self.COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(0,10))
        
        self.stages_list_frame = ctk.CTkFrame(chain_stages_outer_frame, fg_color="transparent")
        self.stages_list_frame.pack(fill="x")

        # Varsayılan/örnek aşamaları yükle
        default_stages_data = [
            {'name': 'Fikir Genişletme', 'type': 'llm_call', 'model': 'gpt-3.5-turbo', 'prompt_template': "Fikir: {input}\n\nGenişletilmiş Kavram:", 'temperature': 0.7, 'max_tokens': 1000},
            {'name': 'Konu Araştırma Ajanı', 'type': 'agent_task', 'model': 'gpt-3.5-turbo', 'task_description_template': "Şu konu hakkında güncel bilgileri web'de araştır: {topic_from_previous_stage}", 'available_tools': ["web_search"], 'output_format_prompt': "Ajanın web araştırması bulgularını ({agent_output}) kullanarak, konuyu özetleyen kısa bir rapor oluştur.", 'temperature': 0.5, 'max_tokens': 800},
            {'name': 'Piyasa Uyumu ve Sonraki Adımlar','type': 'llm_call', 'model': 'gpt-4o', 'prompt_template': "Kavram ve Araştırma: {input}\n\nPiyasa Uyumu ve Sonraki Adımlar:", 'temperature': 0.6, 'max_tokens': 1500 }
        ]
        for i, stage_data in enumerate(default_stages_data):
            self._add_chain_stage_to_ui(i + 1, stage_data, is_new=False) # is_new=False ile mevcutları yükle

        add_stage_btn = ctk.CTkButton(chain_stages_outer_frame, text="+ Aşama Ekle", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_ACCENT, fg_color="transparent", hover_color=self.COLOR_BUTTON_HOVER, height=30, command=lambda: self._add_chain_stage_to_ui(len(self.chain_stages_ui_data) + 1, {}, is_new=True))
        add_stage_btn.pack(anchor="w", pady=(12,0))
        # ... (Context Management - şimdilik basit tutuldu) ...

    def _add_chain_stage_to_ui(self, number, stage_data, is_new=True):
        stage_card = ctk.CTkFrame(self.stages_list_frame, fg_color=self.COLOR_USER_BUBBLE_BG, corner_radius=10)
        stage_card.pack(fill="x", pady=(0,12))
        
        # stage_data'yı ve UI elemanlarını saklamak için bir sözlük
        stage_ui_elements = {'card': stage_card, 'data': stage_data.copy()} # Verinin kopyasını al
        
        # Aşama Numarası ve Adı için başlık
        header_frame = ctk.CTkFrame(stage_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(10,5))
        ctk.CTkLabel(header_frame, text=f"Aşama {number}:", font=self.FONT_H3, text_color=self.COLOR_TEXT_PRIMARY).pack(side="left", padx=(0,5))
        stage_ui_elements['name_entry'] = ctk.CTkEntry(header_frame, placeholder_text="Aşama Adı", fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, font=self.FONT_H3)
        stage_ui_elements['name_entry'].insert(0, stage_data.get('name', f"Yeni Aşama {number}"))
        stage_ui_elements['name_entry'].pack(side="left", fill="x", expand=True)

        # Ayarlar için ana içerik çerçevesi
        stage_content_frame = ctk.CTkFrame(stage_card, fg_color="transparent")
        stage_content_frame.pack(padx=12, pady=5, fill="x", expand=True)
        
        # Aşama Türü Seçimi
        type_frame = ctk.CTkFrame(stage_content_frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=(0,5))
        ctk.CTkLabel(type_frame, text="Aşama Türü:", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).pack(side="left", padx=(0,10))
        stage_ui_elements['type_combo'] = ctk.CTkComboBox(type_frame, values=["llm_call", "agent_task"], state="readonly", font=self.FONT_NORMAL, dropdown_font=self.FONT_NORMAL, command=lambda choice, s=stage_ui_elements: self._on_stage_type_change(choice, s))
        stage_ui_elements['type_combo'].set(stage_data.get('type', 'llm_call'))
        stage_ui_elements['type_combo'].pack(side="left")

        # LLM Ayarları (Model, Sıcaklık, Max Token) - Her iki tür için de ortak olabilir
        common_settings_grid = ctk.CTkFrame(stage_content_frame, fg_color="transparent")
        common_settings_grid.pack(fill="x", pady=(0,5))
        common_settings_grid.columnconfigure((0,1,2), weight=1, uniform="group_common")

        # Model
        model_frame = ctk.CTkFrame(common_settings_grid, fg_color="transparent")
        model_frame.grid(row=0, column=0, sticky="ew", padx=(0,5))
        ctk.CTkLabel(model_frame, text="LLM Model:", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w")
        stage_ui_elements['model_combo'] = ctk.CTkComboBox(model_frame, values=["gpt-4o", "gpt-4", "gpt-3.5-turbo", "ollama/llama3", "ollama/mistral"], font=self.FONT_NORMAL, dropdown_font=self.FONT_NORMAL)
        stage_ui_elements['model_combo'].set(stage_data.get('model', 'gpt-3.5-turbo'))
        stage_ui_elements['model_combo'].pack(fill="x")
        
        # Sıcaklık
        temp_frame_common = ctk.CTkFrame(common_settings_grid, fg_color="transparent")
        temp_frame_common.grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkLabel(temp_frame_common, text="Sıcaklık:", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w")
        stage_ui_elements['temp_slider'] = ctk.CTkSlider(temp_frame_common, from_=0, to=1, number_of_steps=10, button_color=self.COLOR_TEXT_ACCENT)
        stage_ui_elements['temp_slider'].set(float(stage_data.get('temperature', 0.7)))
        stage_ui_elements['temp_slider'].pack(fill="x")
        
        # Max Token
        token_frame_common = ctk.CTkFrame(common_settings_grid, fg_color="transparent")
        token_frame_common.grid(row=0, column=2, sticky="ew", padx=(5,0))
        ctk.CTkLabel(token_frame_common, text="Maks Token:", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w")
        stage_ui_elements['max_tokens_entry'] = ctk.CTkEntry(token_frame_common, fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, font=self.FONT_NORMAL)
        stage_ui_elements['max_tokens_entry'].insert(0, str(stage_data.get('max_tokens', 1000)))
        stage_ui_elements['max_tokens_entry'].pack(fill="x")

        # Aşama türüne özel alanlar için placeholder frame'ler
        stage_ui_elements['llm_call_specific_frame'] = ctk.CTkFrame(stage_content_frame, fg_color="transparent")
        stage_ui_elements['agent_task_specific_frame'] = ctk.CTkFrame(stage_content_frame, fg_color="transparent")

        # LLM Call'a özel: Prompt Template
        ctk.CTkLabel(stage_ui_elements['llm_call_specific_frame'], text="Prompt Şablonu:", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(5,2))
        stage_ui_elements['prompt_template_text'] = ctk.CTkTextbox(stage_ui_elements['llm_call_specific_frame'], height=70, fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, border_width=1, font=self.FONT_NORMAL, wrap="word")
        stage_ui_elements['prompt_template_text'].insert("1.0", stage_data.get('prompt_template', "{input}"))
        stage_ui_elements['prompt_template_text'].pack(fill="x", expand=True)
        
        # Agent Task'a özel: Task Description Template, Available Tools, Output Format Prompt
        ctk.CTkLabel(stage_ui_elements['agent_task_specific_frame'], text="Görev Tanımı Şablonu:", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(5,2))
        stage_ui_elements['task_desc_template_text'] = ctk.CTkTextbox(stage_ui_elements['agent_task_specific_frame'], height=50, fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, border_width=1, font=self.FONT_NORMAL, wrap="word")
        stage_ui_elements['task_desc_template_text'].insert("1.0", stage_data.get('task_description_template', "Görev: {topic_from_previous_stage}"))
        stage_ui_elements['task_desc_template_text'].pack(fill="x", expand=True, pady=(0,5))

        ctk.CTkLabel(stage_ui_elements['agent_task_specific_frame'], text="Mevcut Araçlar (virgülle ayırın):", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(5,2))
        stage_ui_elements['available_tools_entry'] = ctk.CTkEntry(stage_ui_elements['agent_task_specific_frame'], fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, font=self.FONT_NORMAL)
        stage_ui_elements['available_tools_entry'].insert(0, ", ".join(stage_data.get('available_tools', ["web_search", "calculator"])))
        stage_ui_elements['available_tools_entry'].pack(fill="x", pady=(0,5))
        
        ctk.CTkLabel(stage_ui_elements['agent_task_specific_frame'], text="Ajan Çıktı Formatlama Prompt'u (isteğe bağlı):", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(5,2))
        stage_ui_elements['output_format_prompt_text'] = ctk.CTkTextbox(stage_ui_elements['agent_task_specific_frame'], height=50, fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, border_width=1, font=self.FONT_NORMAL, wrap="word")
        stage_ui_elements['output_format_prompt_text'].insert("1.0", stage_data.get('output_format_prompt', ""))
        stage_ui_elements['output_format_prompt_text'].pack(fill="x", expand=True)

        # Silme Butonu
        remove_btn = ctk.CTkButton(header_frame, text="✕", width=28, height=28, fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY, hover_color=self.COLOR_BUTTON_HOVER, command=lambda s=stage_ui_elements: self._remove_chain_stage_from_ui(s))
        remove_btn.pack(side="right")
        self._create_tooltip(remove_btn, "Aşamayı Sil")

        if is_new: # Yeni ekleniyorsa listeye ekle
            self.chain_stages_ui_data.append(stage_ui_elements)
        else: # Var olanı yüklüyorsa, doğru index'e yerleştir.
             # Eğer number-1 index'i listede yoksa veya doluysa append et.
            if number -1 < len(self.chain_stages_ui_data):
                 self.chain_stages_ui_data[number-1] = stage_ui_elements
            else: # Gerekirse listeyi genişlet
                 while len(self.chain_stages_ui_data) < number -1:
                      self.chain_stages_ui_data.append(None) # Placeholder
                 self.chain_stages_ui_data.append(stage_ui_elements)


        self._on_stage_type_change(stage_ui_elements['type_combo'].get(), stage_ui_elements) # Başlangıç durumunu ayarla
        self._renumber_stages()


    def _on_stage_type_change(self, choice, stage_ui_elements):
        """ Bir aşamanın türü değiştiğinde UI'ı günceller. """
        if choice == "llm_call":
            stage_ui_elements['llm_call_specific_frame'].pack(fill="x", expand=True, pady=(5,0))
            stage_ui_elements['agent_task_specific_frame'].pack_forget()
        elif choice == "agent_task":
            stage_ui_elements['llm_call_specific_frame'].pack_forget()
            stage_ui_elements['agent_task_specific_frame'].pack(fill="x", expand=True, pady=(5,0))
        stage_ui_elements['data']['type'] = choice # Veriyi güncelle


    def _remove_chain_stage_from_ui(self, stage_to_remove_ui_elements):
        if stage_to_remove_ui_elements in self.chain_stages_ui_data:
            stage_to_remove_ui_elements['card'].destroy()
            self.chain_stages_ui_data.remove(stage_to_remove_ui_elements)
            self._renumber_stages()

    def _renumber_stages(self):
        for i, stage_ui in enumerate(self.chain_stages_ui_data):
            if stage_ui and stage_ui.get('card'): # Eğer stage_ui None değilse ve card'ı varsa
                # Aşama başlığındaki numarayı güncelle
                # Label'ı bulup güncellemek yerine, name_entry'nin solundaki label'ı hedefleyebiliriz
                # veya daha sağlamı, her aşama kartına bir numara label'ı eklemek.
                # Şimdilik, name_entry placeholder'ını güncelleyebiliriz veya yeni bir label ekleyebiliriz.
                # Örnek: stage_ui['name_entry'].configure(placeholder_text=f"Aşama {i+1} Adı")
                # Veya aşama başlığındaki label'ı bul:
                header_frame = stage_ui['card'].winfo_children()[0] # İlk çocuk header_frame olmalı
                num_name_frame = header_frame.winfo_children()[0] # İlk çocuk numara ve isim içeren frame
                num_label = num_name_frame.winfo_children()[0] # İlk çocuk numara label'ı
                if isinstance(num_label, ctk.CTkLabel) and "Aşama" in num_label.cget("text"):
                     num_label.configure(text=f"Aşama {i+1}:")


    def _get_chain_config_from_ui(self):
        """ UI'dan zincir yapılandırmasını toplar. """
        config = []
        for stage_ui in self.chain_stages_ui_data:
            if not stage_ui: continue # Silinmiş olabilir (None ise)

            stage_data = {'name': stage_ui['name_entry'].get()}
            stage_data['type'] = stage_ui['type_combo'].get()
            stage_data['model'] = stage_ui['model_combo'].get()
            stage_data['temperature'] = float(stage_ui['temp_slider'].get())
            stage_data['max_tokens'] = int(stage_ui['max_tokens_entry'].get())

            if stage_data['type'] == 'llm_call':
                stage_data['prompt_template'] = stage_ui['prompt_template_text'].get("1.0", "end-1c")
            elif stage_data['type'] == 'agent_task':
                stage_data['task_description_template'] = stage_ui['task_desc_template_text'].get("1.0", "end-1c")
                tools_str = stage_ui['available_tools_entry'].get()
                stage_data['available_tools'] = [tool.strip() for tool in tools_str.split(',') if tool.strip()]
                output_format_prompt = stage_ui['output_format_prompt_text'].get("1.0", "end-1c").strip()
                if output_format_prompt: # Sadece doluysa ekle
                    stage_data['output_format_prompt'] = output_format_prompt
            config.append(stage_data)
        return config

    def _build_placeholder_views(self):
        # ... (Mevcut placeholder view kodu - değişiklik yok) ...
        self._chain_view_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        ctk.CTkLabel(self._chain_view_frame, text="Zincir Ayarları Görünümü (Detaylı)", font=self.FONT_H1).pack(pady=20, padx=20, anchor="center")
        self._history_view_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        ctk.CTkLabel(self._history_view_frame, text="Geçmiş Görünümü", font=self.FONT_H1).pack(pady=20, padx=20, anchor="center")

    def add_assistant_message(self, text):
        # ... (Mevcut asistan mesajı kodu - değişiklik yok) ...
        message_wrapper = ctk.CTkFrame(self.chat_messages_scrollable, fg_color="transparent")
        message_wrapper.pack(fill="x", pady=(0,16), anchor="w")
        bubble_frame = ctk.CTkFrame(message_wrapper, fg_color=self.COLOR_ASSISTANT_BUBBLE_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        bubble_frame.pack(side="left", padx=(0, 60))
        bubble_content = ctk.CTkFrame(bubble_frame, fg_color="transparent")
        bubble_content.pack(padx=16, pady=12)
        header_frame = ctk.CTkFrame(bubble_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0,8))
        icon_bg = ctk.CTkFrame(header_frame, width=32, height=32, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=16)
        icon_bg.pack(side="left", padx=(0,12))
        ctk.CTkLabel(icon_bg, text="🤖", font=(self.FONT_FAMILY, 16), text_color=self.COLOR_TEXT_ACCENT).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(header_frame, text="Conference Room AI", font=self.FONT_MEDIUM_WEIGHT, text_color=self.COLOR_TEXT_SECONDARY).pack(side="left", pady=(4,0))
        ctk.CTkLabel(bubble_content, text=text, font=self.FONT_NORMAL, text_color=self.COLOR_TEXT_SECONDARY, wraplength=650, justify="left").pack(fill="x", anchor="w")


    def add_user_message(self, text, idea_title="Fikriniz"):
        # ... (Mevcut kullanıcı mesajı kodu - değişiklik yok) ...
        message_wrapper = ctk.CTkFrame(self.chat_messages_scrollable, fg_color="transparent")
        message_wrapper.pack(fill="x", pady=(0,16), anchor="e")
        bubble_frame = ctk.CTkFrame(message_wrapper, fg_color=self.COLOR_USER_BUBBLE_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        bubble_frame.pack(side="right", padx=(60, 0))
        # ... (rest of the user message rendering)
        pass # Placeholder for brevity

    def add_chain_response_message(self): # Zincir yanıtını ve ilerlemesini gösterir
        # ... (Mevcut zincir yanıt mesajı kodu - llm_automation.py'deki varsayılan zincire göre güncellenebilir) ...
        # Bu fonksiyon, UI'dan alınan geçerli zincir yapılandırmasını yansıtmalıdır.
        # Şimdilik, llm_chain_automation.py'deki varsayılan zinciri temel alarak güncelleyelim.
        chain_config_for_display = self.llm_automation.run_chain("", chain_config=[])[1] # Sadece config almak için boş çalıştır
        if not chain_config_for_display: # Eğer run_chain config döndürmüyorsa (eski versiyon)
             chain_config_for_display = [
                {'name': 'Fikir Genişletme', 'type': 'llm_call'},
                {'name': 'Konu Araştırma Ajanı', 'type': 'agent_task'},
                {'name': 'Piyasa Uyumu', 'type': 'llm_call'}
            ] # Manuel varsayılan

        # ... (Mesaj balonunu ve başlığını oluştur) ...
        # ... (Zincir aşamalarını bu chain_config_for_display'e göre çiz) ...
        # ... (İlerleme göstergesini başlat) ...
        pass # Placeholder for brevity


    def _switch_view(self, view_name, target_frame):
        # ... (Mevcut view switch kodu - değişiklik yok) ...
        if self._chat_view_frame: self._chat_view_frame.pack_forget()
        if self._settings_view_frame: self._settings_view_frame.pack_forget()
        if self._chain_view_frame: self._chain_view_frame.pack_forget()
        if self._history_view_frame: self._history_view_frame.pack_forget()
        if target_frame:
            target_frame.pack(fill="both", expand=True)
            self.current_view_name = view_name
            self._update_sidebar_active_state()
        else:
            self.show_chat_view()

    def show_chat_view(self): self._switch_view("chat", self._chat_view_frame)
    def show_settings_view(self): self._switch_view("settings", self._settings_view_frame)
    def show_chain_config_view_from_sidebar(self): self.show_settings_view() # Ayarlar içinde zincir bölümüne odaklanabilir
    def show_chain_config_view_from_chat(self): self.show_settings_view()
    def show_history_view(self): self._switch_view("history", self._history_view_frame)

    def new_session(self):
        # ... (Mevcut yeni oturum kodu - değişiklik yok) ...
        for widget in self.chat_messages_scrollable.winfo_children(): widget.destroy()
        self.add_assistant_message("Conference Room'a hoş geldiniz! ...")
        self.input_textbox.delete("1.0", "end")


    def send_message_from_ui(self):
        user_message = self.input_textbox.get("1.0", "end-1c").strip()
        if not user_message:
            messagebox.showinfo("Bilgi", "Lütfen işlenecek bir fikir veya soru girin.")
            return

        self.add_user_message(user_message, idea_title="Sizin Girdiniz")
        self.input_textbox.delete("1.0", "end")
        
        self.add_assistant_message(f"\"{user_message}\" fikriniz LLM zinciri ile işleniyor...")
        
        # UI'dan zincir yapılandırmasını al
        current_chain_config = self._get_chain_config_from_ui()
        if not current_chain_config:
            self.add_assistant_message("HATA: Zincir yapılandırması alınamadı. Lütfen ayarlarda en az bir aşama tanımlayın.")
            return

        try:
            # LLM zincirini çalıştır (ideal olarak ayrı bir thread'de)
            # Şimdilik UI donmasını önlemek için after kullanabiliriz ama uzun görevler için thread daha iyi.
            self.after(100, lambda: self._execute_llm_chain_async(user_message, current_chain_config))
            
        except Exception as e:
            self.add_assistant_message(f"LLM zinciri işlenirken bir hata oluştu: {e}")
            messagebox.showerror("Hata", f"Zincir işlenirken hata: {e}")

    def _execute_llm_chain_async(self, user_message, chain_config):
        """ LLM zincirini çalıştırır ve sonucu UI'a ekler. """
        try:
            final_results = self.llm_automation.run_chain(user_message, chain_config=chain_config)
            
            full_response = "LLM Zincir İşlemi Tamamlandı!\n"
            if final_results:
                for stage_name, output_content in final_results.items():
                    full_response += f"\n--- {stage_name} ---\n{output_content}\n"
            else:
                full_response += "\nZincir çıktı üretmedi veya bir sorun oluştu."
            
            self.add_assistant_message(full_response)
        except Exception as e:
            error_message = f"LLM zinciri yürütülürken hata: {e}"
            self.add_assistant_message(error_message)
            messagebox.showerror("Yürütme Hatası", error_message)


    def on_enter_key_send(self, event):
        if not (event.state & 1): # Shift basılı değilse
            self.send_message_from_ui()
            return "break" 
        return None


if __name__ == "__main__":
    app = ConferenceRoomApp()
    app.mainloop()
