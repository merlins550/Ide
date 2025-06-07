import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
# from PIL import Image, ImageTk # Pillow şu anda aktif olarak kullanılmıyor
# import os
# import io
# import base64
# import webbrowser
# from datetime import datetime

# Genel görünüm ayarları
ctk.set_appearance_mode("Light")  # "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue" (default), "green", "dark-blue"

class ConferenceRoomApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere yapılandırması
        self.title("Conference Room")
        self.geometry("1280x850") # Boyut biraz artırıldı
        self.minsize(960, 720)   # Minimum boyutlar da artırıldı

        # Renkler (start.py'dan esinlenerek - NexusFlow)
        self.COLOR_GRADIENT_START = "#6e8efb"
        self.COLOR_GRADIENT_END = "#a777e3"
        self.COLOR_BACKGROUND = "#F9FAFB"      # bg-gray-50
        self.COLOR_SURFACE = "#FFFFFF"         # bg-white (sidebar, header, kartlar)
        self.COLOR_TEXT_PRIMARY = "#1F2937"    # text-gray-800
        self.COLOR_TEXT_SECONDARY = "#4B5563"  # text-gray-700
        self.COLOR_TEXT_TERTIARY = "#6B7280"   # text-gray-500/600
        self.COLOR_TEXT_ACCENT = "#4F46E5"     # text-indigo-600
        self.COLOR_BUTTON_HOVER = "#F3F4F6"    # bg-gray-100
        self.COLOR_BUTTON_ACTIVE_BG = "#EEF2FF" # bg-indigo-100 (aktif sidebar)
        self.COLOR_BORDER = "#E5E7EB"          # border-gray-200
        self.COLOR_INPUT_BG = "#FFFFFF"
        self.COLOR_INPUT_BORDER = "#D1D5DB"    # border-gray-300
        self.COLOR_ASSISTANT_BUBBLE_BG = self.COLOR_SURFACE
        self.COLOR_USER_BUBBLE_BG = "#EEF2FF"  # bg-indigo-50
        self.COLOR_STATUS_GREEN_TEXT = "#065F46" # text-green-800
        self.COLOR_STATUS_GREEN_BG = "#D1FAE5"   # bg-green-100
        self.COLOR_STATUS_YELLOW_TEXT = "#92400E" # text-yellow-800
        self.COLOR_STATUS_YELLOW_BG = "#FEF3C7"   # bg-yellow-100
        self.COLOR_STATUS_BLUE_TEXT = "#1E40AF"   # text-blue-800 (Ollama)
        self.COLOR_STATUS_BLUE_BG = "#DBEAFE"     # bg-blue-100 (Ollama)
        self.COLOR_PROGRESS_INFO_TEXT = "#1D4ED8" # text-blue-700
        self.COLOR_PROGRESS_INFO_BG = "#EFF6FF"   # bg-blue-50

        # Fontlar (start.py'dan esinlenerek)
        self.FONT_FAMILY = "Segoe UI Variable" # Daha modern bir Segoe UI varyantı
        self.FONT_BOLD = (self.FONT_FAMILY, 13, "bold")
        self.FONT_NORMAL = (self.FONT_FAMILY, 12)
        self.FONT_MEDIUM_WEIGHT = (self.FONT_FAMILY, 12, "normal") # Tailwind'de font-medium için
        self.FONT_SMALL = (self.FONT_FAMILY, 10)
        self.FONT_SMALL_MEDIUM = (self.FONT_FAMILY, 10, "normal")
        self.FONT_TITLE = (self.FONT_FAMILY, 18, "bold") # NexusFlow başlığı için
        self.FONT_H1 = (self.FONT_FAMILY, 16, "bold")    # Ayarlar başlığı
        self.FONT_H2 = (self.FONT_FAMILY, 14, "bold")    # Bölüm başlıkları
        self.FONT_H3 = (self.FONT_FAMILY, 12, "bold")    # Alt bölüm başlıkları

        # Aktif görünümü takip etmek için
        self.current_view_name = "chat"

        # Ana arayüzü oluştur
        self.setup_ui()

        # Varsayılan görünüm
        self.show_chat_view()

    def setup_ui(self):
        # Ana konteyner
        self.main_container = ctk.CTkFrame(self, fg_color=self.COLOR_BACKGROUND)
        self.main_container.pack(fill="both", expand=True)

        # Sidebar ve ana içerik alanı
        self.create_sidebar()
        self.create_main_content_area() # Yeniden adlandırıldı (create_main_content -> create_main_content_area)

    def create_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.main_container, width=64, fg_color=self.COLOR_SURFACE, corner_radius=0, border_width=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        # Kenarlık ile gölge efekti (isteğe bağlı)
        # self.sidebar.configure(border_width=(0, 1, 0, 0), border_color=self.COLOR_BORDER)

        # Logo (start.py'daki gradient-bg ve fa-link ikonu)
        logo_bg = ctk.CTkFrame(self.sidebar, width=40, height=40, fg_color="transparent", corner_radius=10)
        logo_bg.pack(pady=(20, 30), padx=12)

        # Gradient Logo Arka Planı (Canvas ile çizim)
        canvas = tk.Canvas(logo_bg, width=40, height=40, highlightthickness=0, bg=self.COLOR_SURFACE)
        canvas.pack()
        # CustomTkinter'da doğrudan gradient widget desteği yok, bu yüzden tek renk kullanacağız.
        # start.py'daki gradient'in ana rengini alalım.
        logo_bg.configure(fg_color=self.COLOR_GRADIENT_START)

        logo_icon = ctk.CTkLabel(logo_bg, text="🔗", font=(self.FONT_FAMILY, 20, "bold"), text_color=self.COLOR_SURFACE)
        logo_icon.place(relx=0.5, rely=0.5, anchor="center")

        # Navigasyon butonları için bir çerçeve (butonları gruplamak ve ortalamak için)
        self.nav_buttons_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_buttons_frame.pack(expand=False, pady=10)

        self.sidebar_buttons = {} # Butonları saklamak için
        self.sidebar_buttons["chat"] = self._create_sidebar_button(self.nav_buttons_frame, "💬", "Sohbet", self.show_chat_view) # fa-comment-dots
        self.sidebar_buttons["chain"] = self._create_sidebar_button(self.nav_buttons_frame, "⛓️", "Zincir Ayarları", self.show_chain_config_view_from_sidebar) # fa-link
        self.sidebar_buttons["history"] = self._create_sidebar_button(self.nav_buttons_frame, "🕒", "Geçmiş", self.show_history_view) # fa-history

        # Ayarlar butonu (altta)
        self.settings_btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.settings_btn_frame.pack(side="bottom", fill="x", pady=(0,20))
        self.sidebar_buttons["settings"] = self._create_sidebar_button(self.settings_btn_frame, "⚙️", "Ayarlar", self.show_settings_view) # fa-cog

    def _create_sidebar_button(self, parent, icon_text, tooltip_text, command):
        button = ctk.CTkButton(
            parent,
            text=icon_text,
            width=48,
            height=48,
            fg_color="transparent",
            text_color=self.COLOR_TEXT_TERTIARY, # text-gray-600
            hover_color=self.COLOR_BUTTON_HOVER, # hover:bg-gray-100
            font=ctk.CTkFont(family=self.FONT_FAMILY, size=22), # Daha büyük ikonlar
            corner_radius=10, # rounded-lg
            command=command
        )
        button.pack(pady=6, padx=8) # mb-3 benzeri
        self._create_tooltip(button, tooltip_text)
        return button

    def _update_sidebar_active_state(self):
        for key, button in self.sidebar_buttons.items():
            if key == self.current_view_name:
                button.configure(fg_color=self.COLOR_BUTTON_ACTIVE_BG, text_color=self.COLOR_TEXT_ACCENT)
            else:
                button.configure(fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY)

    def _create_tooltip(self, widget, text):
        # Mevcut tooltip oluşturma fonksiyonu iyi, sadece fontu güncelleyebiliriz.
        tooltip = None
        def enter(event):
            nonlocal tooltip
            x = y = 0
            x, y, _, _ = widget.bbox("insert") # widget.bbox("insert") daha iyi olabilir
            x += widget.winfo_rootx() + widget.winfo_width() + 5 # Sağına
            y += widget.winfo_rooty() + (widget.winfo_height() // 2) - 10 # Ortasına yakın

            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{int(x)}+{int(y)}")

            label = tk.Label(tooltip, text=text, background="#2D3748", foreground="white", # Koyu gri arkaplan
                           relief="solid", borderwidth=1, padx=6, pady=3, font=(self.FONT_FAMILY, 9)) # Biraz daha modern font
            label.pack()

        def leave(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def create_main_content_area(self):
        # Ana içerik çerçevesi (eskiden content_frame)
        self.main_content_frame = ctk.CTkFrame(self.main_container, fg_color=self.COLOR_BACKGROUND, corner_radius=0)
        self.main_content_frame.pack(side="right", fill="both", expand=True) # side="right" daha iyi olabilir

        # Header
        self.header_frame = ctk.CTkFrame(self.main_content_frame, height=65, fg_color=self.COLOR_SURFACE, corner_radius=0) # Yükseklik ve gölge için border
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.configure(border_width=(0,0,1,0), border_color=self.COLOR_BORDER) # shadow-sm

        # Uygulama başlığı (start.py'da NexusFlow, bizde Conference Room)
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Conference Room", # veya "NexusFlow"
            font=self.FONT_TITLE, # (self.FONT_FAMILY, 20, "bold")
            text_color=self.COLOR_TEXT_PRIMARY
        )
        self.title_label.pack(side="left", padx=24, pady=18) # px-6

        # Header sağ tarafı
        self.header_right_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent") # Eskiden header_right
        self.header_right_frame.pack(side="right", padx=24, pady=12) # space-x-4 ve padding

        # Yeni Oturum butonu
        self.new_session_btn = ctk.CTkButton(
            self.header_right_frame,
            text="Yeni Oturum  +",
            font=(self.FONT_FAMILY, 11, "normal"), # text-sm font-medium için
            text_color=self.COLOR_TEXT_SECONDARY, # text-gray-700
            fg_color=self.COLOR_BUTTON_HOVER,     # bg-gray-100
            hover_color="#E5E7EB",                # hover:bg-gray-200
            corner_radius=16, # rounded-full
            height=36,        # py-1.5 benzeri
            width=130,        # px-4 benzeri
            command=self.new_session
        )
        self.new_session_btn.pack(side="left", padx=(0,16)) # mr-4

        # Kullanıcı ikonu
        self.user_icon_bg = ctk.CTkFrame(self.header_right_frame, width=36, height=36, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=18) # rounded-full, biraz büyütüldü
        self.user_icon_bg.pack(side="left")
        self.user_icon_bg.pack_propagate(False)

        self.user_icon_label = ctk.CTkLabel(self.user_icon_bg, text="👤", font=(self.FONT_FAMILY, 18), text_color=self.COLOR_TEXT_ACCENT) # fa-user, biraz büyütüldü
        self.user_icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Dinamik içerik alanı - farklı görünümleri barındıracak (eskiden dynamic_content)
        self.view_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent") # Daha genel bir isim
        self.view_container.pack(fill="both", expand=True, padx=0, pady=0) # Kenar boşlukları kaldırıldı, gerekirse içten verilecek

        # Farklı görünümleri oluştur (önceden yükle, sonra göster/gizle)
        self._chat_view_frame = None
        self._settings_view_frame = None
        # Diğer görünümler için de placeholder'lar eklenebilir
        self._chain_view_frame = None
        self._history_view_frame = None

        self._build_chat_view()
        self._build_settings_view()
        self._build_placeholder_views() # Diğer görünümler için


    def _build_chat_view(self):
        self._chat_view_frame = ctk.CTkFrame(self.view_container, fg_color="transparent") # Arka planı parent'tan alır

        # Chat mesajları alanı
        self.chat_messages_scrollable = ctk.CTkScrollableFrame(self._chat_view_frame, fg_color="transparent", scrollbar_button_color=self.COLOR_GRADIENT_START, scrollbar_button_hover_color=self.COLOR_GRADIENT_END)
        self.chat_messages_scrollable.pack(fill="both", expand=True, padx=24, pady=(20,0)) # p-6, alt boşluk input alanına

        # Karşılama mesajı
        self.add_assistant_message("Conference Room'a hoş geldiniz! Ben sizin LLM zincir otomasyon asistanınızım. Fikrinizi veya sorunuzu aşağıya girerek başlayın, optimize edilmiş LLM işlem hattımızda size rehberlik edeceğim.")
        self.add_user_message("Temel bir ürün fikrini alıp özel LLM'ler zinciri kullanarak eksiksiz bir iş planına dönüştüren otomatik bir sistem oluşturmak istiyorum.")
        self.add_chain_response_message() # Eskiden add_chain_response

        # Giriş Alanı (Input Area)
        self.input_area_frame = ctk.CTkFrame(self._chat_view_frame, fg_color=self.COLOR_BACKGROUND, height=140) # border-t için ayrı bir frame
        self.input_area_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        self.input_area_frame.configure(border_width=(1,0,0,0), border_color=self.COLOR_BORDER)

        # Giriş alanı içindeki ana konteyner (max-w-4xl mx-auto benzeri)
        input_content_wrapper = ctk.CTkFrame(self.input_area_frame, fg_color="transparent")
        input_content_wrapper.pack(pady=15, padx=24, fill="x") # p-4


        # Text input ve send butonu içeren frame
        input_controls_frame = ctk.CTkFrame(input_content_wrapper, fg_color="transparent")
        input_controls_frame.pack(fill="x", expand=True)


        # Text input alanı (start.py'daki prompt-editor)
        self.textbox_frame = ctk.CTkFrame(input_controls_frame, fg_color=self.COLOR_INPUT_BG, corner_radius=12, border_width=1, border_color=self.COLOR_INPUT_BORDER) # rounded-lg shadow-sm border
        self.textbox_frame.pack(side="left", fill="x", expand=True, padx=(0, 10)) # mr-2

        self.input_textbox = ctk.CTkTextbox(
            self.textbox_frame,
            fg_color="transparent",
            text_color=self.COLOR_TEXT_SECONDARY,
            font=self.FONT_NORMAL,
            border_width=0,
            wrap="word",
            height=80 # min-height: 120px için (prompt-editor)
        )
        self.input_textbox.pack(fill="x", expand=True, padx=12, pady=(8,0)) # px-3 py-2
        self.input_textbox.bind("<Return>", self.on_enter_key_send) # Eskiden on_enter_key

        # Toolbar (metin kutusunun altında)
        toolbar_frame = ctk.CTkFrame(self.textbox_frame, fg_color="transparent", height=30) # border-t
        toolbar_frame.pack(fill="x", padx=12, pady=(2, 6)) # px-3 py-2
        toolbar_frame.configure(border_width=(1,0,0,0), border_color=self.COLOR_BORDER)


        attachment_btn = ctk.CTkButton(toolbar_frame, text="📎", width=28, height=28, fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY, hover_color=self.COLOR_BUTTON_HOVER, corner_radius=6, font=("Segoe UI Emoji", 14))
        attachment_btn.pack(side="left", padx=(0,4))
        self._create_tooltip(attachment_btn, "Dosya Ekle")

        magic_btn = ctk.CTkButton(toolbar_frame, text="✨", width=28, height=28, fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY, hover_color=self.COLOR_BUTTON_HOVER, corner_radius=6, font=("Segoe UI Emoji", 14))
        magic_btn.pack(side="left", padx=(0,4))
        self._create_tooltip(magic_btn, "Sihirli Araçlar")

        # Gelişmiş Butonu (sağda)
        advanced_settings_btn = ctk.CTkButton(toolbar_frame, text="⚙️ Gelişmiş", width=80, height=24,
                                         font=(self.FONT_FAMILY, 10),
                                         fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY,
                                         hover_color=self.COLOR_BUTTON_HOVER, corner_radius=6,
                                         command=self.show_settings_view) # Zincir ayarları daha mantıklı olabilir
        advanced_settings_btn.pack(side="right")
        self._create_tooltip(advanced_settings_btn, "Gelişmiş Ayarlar")


        # Gönder Butonu (start.py'daki gradient)
        self.send_message_btn = ctk.CTkButton( # Eskiden GradientButton
            input_controls_frame,
            text="➤", # fa-paper-plane yerine ok veya emoji
            font=(self.FONT_FAMILY, 20), # Daha büyük ikon
            width=52, # w-12 h-12
            height=52, # w-12 h-12
            corner_radius=10, # rounded-lg
            fg_color=self.COLOR_GRADIENT_START, # Gradient başlangıç
            hover_color=self.COLOR_GRADIENT_END,   # Gradient bitiş (hover için)
            text_color=self.COLOR_SURFACE,
            command=self.send_message_from_ui # Eskiden send_message
        )
        self.send_message_btn.pack(side="right", pady=(0,0)) # Metin kutusu ile aynı hizada

        # Yardım metni (start.py'dan)
        help_text_frame = ctk.CTkFrame(input_content_wrapper, fg_color="transparent")
        help_text_frame.pack(fill="x", pady=(6,0), padx=5)

        help_label_1 = ctk.CTkLabel(help_text_frame, text="NexusFlow girdinizi yapılandırılmış LLM zinciri üzerinden işleyecektir.", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY)
        help_label_1.pack(side="left")

        edit_chain_link_btn = ctk.CTkButton(
            help_text_frame,
            text="Zincir yapılandırmasını düzenle",
            font=self.FONT_SMALL_MEDIUM, # text-xs
            fg_color="transparent",
            text_color=self.COLOR_TEXT_ACCENT, # text-indigo-600
            hover_color="transparent", # hover:underline için efekt yok, altını çizmek için özel bir şey gerek
            command=self.show_chain_config_view_from_chat, # Ayarların zincir bölümüne gider
            height=15,
            anchor="w"
        )
        edit_chain_link_btn.pack(side="left", padx=4)


    def _build_settings_view(self):
        self._settings_view_frame = ctk.CTkFrame(self.view_container, fg_color=self.COLOR_SURFACE) # bg-white

        # Ayarlar başlığı (start.py'daki gibi)
        settings_header_bar = ctk.CTkFrame(self._settings_view_frame, fg_color="transparent", height=60)
        settings_header_bar.pack(fill="x", padx=24, pady=(18,10)) # px-6 py-4 border-b
        settings_header_bar.configure(border_width=(0,0,1,0), border_color=self.COLOR_BORDER)

        settings_main_title = ctk.CTkLabel(settings_header_bar, text="Ayarlar & Yapılandırma", font=self.FONT_H1, text_color=self.COLOR_TEXT_PRIMARY)
        settings_main_title.pack(anchor="w")

        settings_subtitle_label = ctk.CTkLabel(settings_header_bar, text="API anahtarlarınızı ve LLM zincir ayarlarınızı yönetin", font=(self.FONT_FAMILY, 11), text_color=self.COLOR_TEXT_TERTIARY) # text-sm
        settings_subtitle_label.pack(anchor="w", pady=(2,0))

        # Ayarlar içeriği için kaydırılabilir alan
        settings_scrollable_content = ctk.CTkScrollableFrame(self._settings_view_frame, fg_color=self.COLOR_BACKGROUND, scrollbar_button_color=self.COLOR_GRADIENT_START) # bg-gray-50
        settings_scrollable_content.pack(fill="both", expand=True, padx=0, pady=0) # p-6

        # İçerik sarmalayıcı (max-w-4xl mx-auto space-y-8)
        settings_content_wrapper = ctk.CTkFrame(settings_scrollable_content, fg_color="transparent")
        settings_content_wrapper.pack(pady=24, padx=24, fill="x") # Gerçek padding burada


        # API Keys Section
        self._create_api_keys_settings_section(settings_content_wrapper)

        # Chain Configuration Section
        self._create_chain_config_settings_section(settings_content_wrapper)

        # Save Settings Buttons (start.py'daki gibi)
        save_buttons_frame = ctk.CTkFrame(settings_content_wrapper, fg_color="transparent")
        save_buttons_frame.pack(fill="x", pady=(30,10), anchor="e") # justify-end

        reset_button = ctk.CTkButton(
            save_buttons_frame,
            text="Sıfırla",
            font=self.FONT_MEDIUM_WEIGHT, # text-sm font-medium
            text_color=self.COLOR_TEXT_SECONDARY,
            fg_color=self.COLOR_SURFACE, # bg-white
            border_width=1,
            border_color=self.COLOR_INPUT_BORDER, # border-gray-300
            hover_color=self.COLOR_BUTTON_HOVER, # hover:bg-gray-50
            height=36,
            width=100,
            corner_radius=8 # rounded-md
        )
        reset_button.pack(side="right", padx=(0, 12)) # space-x-3

        save_changes_button = ctk.CTkButton(
            save_buttons_frame,
            text="Değişiklikleri Kaydet",
            font=self.FONT_MEDIUM_WEIGHT,
            text_color=self.COLOR_SURFACE, # text-white
            fg_color=self.COLOR_TEXT_ACCENT, # bg-indigo-600
            hover_color="#4338CA", # hover:bg-indigo-700
            height=36,
            width=160,
            corner_radius=8
        )
        save_changes_button.pack(side="right")


    def _create_api_keys_settings_section(self, parent):
        # API Keys container (bg-white rounded-xl shadow-sm border)
        api_keys_card = ctk.CTkFrame(parent, fg_color=self.COLOR_SURFACE, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        api_keys_card.pack(fill="x", pady=(0,20)) # space-y-8 için alttan boşluk

        # Header (border-b px-5 py-4 bg-gray-50)
        api_keys_header_frame = ctk.CTkFrame(api_keys_card, fg_color=self.COLOR_BACKGROUND, corner_radius=0, height=60)
        api_keys_header_frame.pack(fill="x", padx=0, pady=0) # Kenarlığı takip etmesi için içten padding
        api_keys_header_frame.configure(border_width=(0,0,1,0), border_color=self.COLOR_BORDER)
        # Pack_propagate false ve iç frame ile padding kontrolü
        api_keys_header_content = ctk.CTkFrame(api_keys_header_frame, fg_color="transparent")
        api_keys_header_content.pack(padx=20, pady=12, fill="both", expand=True)


        api_keys_title_label = ctk.CTkLabel(api_keys_header_content, text="LLM Sağlayıcı API Anahtarları", font=self.FONT_H2, text_color=self.COLOR_TEXT_PRIMARY)
        api_keys_title_label.pack(anchor="w")
        api_keys_subtitle_label = ctk.CTkLabel(api_keys_header_content, text="Zincirinizdeki farklı LLM sağlayıcılarına erişimi yapılandırın", font=(self.FONT_FAMILY, 10), text_color=self.COLOR_TEXT_TERTIARY)
        api_keys_subtitle_label.pack(anchor="w", pady=(2,0))

        # Provider listesi için frame (divide-y divide-gray-200)
        providers_list_frame = ctk.CTkFrame(api_keys_card, fg_color="transparent")
        providers_list_frame.pack(fill="x", expand=True)


        # OpenAI section
        self._render_provider_settings_card(
            providers_list_frame, "OpenAI", "GPT-4, GPT-3.5 modelleri", "🤖", # Font Awesome'da fab fa-openai, emoji ile değiştirildi
            "Aktif", self.COLOR_STATUS_GREEN_TEXT, self.COLOR_STATUS_GREEN_BG,
            True, False,
            api_key_value="sk-********************", org_value="org-****************"
        )
        ctk.CTkFrame(providers_list_frame, height=1, fg_color=self.COLOR_BORDER).pack(fill="x", padx=20) # Ayırıcı

        # Anthropic section
        self._render_provider_settings_card(
            providers_list_frame, "Anthropic", "Claude modelleri", "🧠", # Font Awesome'da fas fa-brain, emoji ile değiştirildi
            "Yapılandırılmadı", self.COLOR_STATUS_YELLOW_TEXT, self.COLOR_STATUS_YELLOW_BG,
            False, False
        )
        ctk.CTkFrame(providers_list_frame, height=1, fg_color=self.COLOR_BORDER).pack(fill="x", padx=20) # Ayırıcı

        # Ollama section
        self._render_provider_settings_card(
            providers_list_frame, "Ollama", "Yerel LLM modelleri", "💻", # Font Awesome'da fas fa-server, emoji ile değiştirildi
            "Kendin Barındır", self.COLOR_STATUS_BLUE_TEXT, self.COLOR_STATUS_BLUE_BG,
            True, True,
            base_url_value="http://localhost:11434", model_value="Custom Model", custom_model_name_value="my-custom-model",
            ollama_connected=True
        )
        # ctk.CTkFrame(providers_list_frame, height=1, fg_color=self.COLOR_BORDER).pack(fill="x", padx=20) # Son eleman sonrası ayırıcıya gerek yok

        # Add new provider button (p-5)
        add_provider_wrapper = ctk.CTkFrame(api_keys_card, fg_color="transparent") # Pading için sarmalayıcı
        add_provider_wrapper.pack(fill="x", padx=20, pady=20)

        self.add_provider_btn = ctk.CTkButton(
            add_provider_wrapper,
            text="+ LLM Sağlayıcı Ekle",
            font=self.FONT_MEDIUM_WEIGHT, # text-sm
            fg_color="transparent", # bg-transparent
            text_color=self.COLOR_TEXT_ACCENT, # text-indigo-600
            hover_color=self.COLOR_BUTTON_ACTIVE_BG, # hover:bg-indigo-50
            border_width=2, # border-2
            border_color=self.COLOR_BORDER, # border-dashed border-gray-300 -> CTk'da dashed yok, solid
            corner_radius=8, # rounded-md
            height=40, # py-2
            # image=plus_icon # Font Awesome ikonu yerine metin
        )
        self.add_provider_btn.pack(fill="x")


    def _render_provider_settings_card(self, parent, name, description, icon, status_text, status_color, status_bg_color, has_key=False, is_local=False, **kwargs):
        # Provider container (p-5)
        provider_entry_frame = ctk.CTkFrame(parent, fg_color="transparent")
        provider_entry_frame.pack(fill="x", padx=20, pady=(15,10)) # İç padding

        # Provider header (flex items-center justify-between mb-3)
        provider_header = ctk.CTkFrame(provider_entry_frame, fg_color="transparent")
        provider_header.pack(fill="x", pady=(0,12))

        provider_header_left = ctk.CTkFrame(provider_header, fg_color="transparent")
        provider_header_left.pack(side="left", fill="x", expand=True)

        icon_bg = ctk.CTkFrame(provider_header_left, width=40, height=40, fg_color=self.COLOR_BUTTON_HOVER, corner_radius=8) # bg-gray-100
        icon_bg.pack(side="left", padx=(0,12)) # mr-3
        icon_label = ctk.CTkLabel(icon_bg, text=icon, font=(self.FONT_FAMILY, 18), text_color=self.COLOR_TEXT_SECONDARY)
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        info_texts_frame = ctk.CTkFrame(provider_header_left, fg_color="transparent")
        info_texts_frame.pack(side="left")
        name_label = ctk.CTkLabel(info_texts_frame, text=name, font=self.FONT_H3, text_color=self.COLOR_TEXT_PRIMARY)
        name_label.pack(anchor="w")
        desc_label = ctk.CTkLabel(info_texts_frame, text=description, font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY)
        desc_label.pack(anchor="w")

        provider_header_right = ctk.CTkFrame(provider_header, fg_color="transparent")
        provider_header_right.pack(side="right")

        status_badge = ctk.CTkLabel(provider_header_right, text=status_text, font=(self.FONT_FAMILY, 9, "bold"), text_color=status_color, fg_color=status_bg_color, corner_radius=6, padx=8, pady=3)
        status_badge.pack(side="left", padx=(0,8)) # space-x-2

        ellipsis_btn = ctk.CTkButton(provider_header_right, text="⋮", width=24, height=24, fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY, hover_color=self.COLOR_BUTTON_HOVER, font=(self.FONT_FAMILY, 16))
        ellipsis_btn.pack(side="left")
        self._create_tooltip(ellipsis_btn, "Daha Fazla Seçenek")


        # Form fields (pl-13 -> icon + margin kadar padding)
        form_fields_frame = ctk.CTkFrame(provider_entry_frame, fg_color="transparent")
        form_fields_frame.pack(fill="x", padx=(52, 0), pady=(0,10)) # 40px icon + 12px margin

        if is_local: # Ollama
            grid_frame = ctk.CTkFrame(form_fields_frame, fg_color="transparent")
            grid_frame.pack(fill="x")
            grid_frame.columnconfigure(0, weight=1)
            grid_frame.columnconfigure(1, weight=1)

            ctk.CTkLabel(grid_frame, text="Temel URL", anchor="w", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).grid(row=0, column=0, sticky="w", pady=(0,2))
            url_entry = ctk.CTkEntry(grid_frame, placeholder_text="http://localhost:11434", fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=36, font=self.FONT_NORMAL)
            url_entry.grid(row=1, column=0, sticky="ew", padx=(0,10)) # md:grid-cols-2 gap-4
            if kwargs.get("base_url_value"): url_entry.insert(0, kwargs["base_url_value"])

            ctk.CTkLabel(grid_frame, text="Model", anchor="w", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).grid(row=0, column=1, sticky="w", pady=(0,2))
            model_combo = ctk.CTkComboBox(grid_frame, values=["llama3", "mistral", "gemma", "phi3", "Custom Model"], fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, button_color=self.COLOR_INPUT_BORDER, height=36, font=self.FONT_NORMAL, dropdown_font=self.FONT_NORMAL)
            model_combo.grid(row=1, column=1, sticky="ew", padx=(10,0))
            model_combo.set(kwargs.get("model_value", "Custom Model"))

            ctk.CTkLabel(form_fields_frame, text="Özel Model Adı", anchor="w", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).pack(fill="x", pady=(8,2))
            custom_model_entry = ctk.CTkEntry(form_fields_frame, placeholder_text="my-custom-model", fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=36, font=self.FONT_NORMAL)
            custom_model_entry.pack(fill="x")
            if kwargs.get("custom_model_name_value"): custom_model_entry.insert(0, kwargs["custom_model_name_value"])

        else: # Cloud (OpenAI, Anthropic)
            grid_frame = ctk.CTkFrame(form_fields_frame, fg_color="transparent")
            grid_frame.pack(fill="x")
            grid_frame.columnconfigure(0, weight=1)
            if name == "OpenAI": grid_frame.columnconfigure(1, weight=1)


            ctk.CTkLabel(grid_frame, text="API Anahtarı", anchor="w", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).grid(row=0, column=0, sticky="w", pady=(0,2))
            api_key_entry_frame = ctk.CTkFrame(grid_frame, fg_color="transparent") # Göz ikonu için frame
            api_key_entry_frame.grid(row=1, column=0, sticky="ew", padx=(0, 10 if name == "OpenAI" else 0))

            api_key_entry = ctk.CTkEntry(api_key_entry_frame, placeholder_text="API anahtarınızı girin", show="*", fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=36, font=self.FONT_NORMAL)
            api_key_entry.pack(side="left", fill="x", expand=True)
            if kwargs.get("api_key_value"): api_key_entry.insert(0, kwargs["api_key_value"])

            # Göz ikonu (start.py'daki gibi)
            # eye_button = ctk.CTkButton(api_key_entry_frame, text="👁️", width=30, height=30, fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY, hover_color=self.COLOR_BUTTON_HOVER)
            # eye_button.pack(side="right", padx=(4,0))


            if name == "OpenAI":
                ctk.CTkLabel(grid_frame, text="Organizasyon", anchor="w", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_SECONDARY).grid(row=0, column=1, sticky="w", pady=(0,2))
                org_entry = ctk.CTkEntry(grid_frame, placeholder_text="org-****************", fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=36, font=self.FONT_NORMAL)
                org_entry.grid(row=1, column=1, sticky="ew", padx=(10,0))
                if kwargs.get("org_value"): org_entry.insert(0, kwargs["org_value"])

        # Status and test connection (mt-3 flex items-center justify-between)
        status_test_frame = ctk.CTkFrame(form_fields_frame, fg_color="transparent")
        status_test_frame.pack(fill="x", pady=(12,0))

        if has_key:
            last_used_frame = ctk.CTkFrame(status_test_frame, fg_color="transparent")
            last_used_frame.pack(side="left")
            if is_local and kwargs.get("ollama_connected"):
                 ctk.CTkFrame(last_used_frame, width=8, height=8, fg_color=self.COLOR_STATUS_GREEN_TEXT, corner_radius=4).pack(side="left", pady=(0,0), padx=(0,6)) # Yeşil nokta
                 ctk.CTkLabel(last_used_frame, text="Yerel Ollama örneğine bağlı", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(side="left")
            elif not is_local:
                 ctk.CTkFrame(last_used_frame, width=8, height=8, fg_color=self.COLOR_STATUS_GREEN_TEXT, corner_radius=4).pack(side="left", pady=(0,0), padx=(0,6))
                 ctk.CTkLabel(last_used_frame, text="Son kullanım: 5 dk önce", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(side="left")


        test_conn_btn = ctk.CTkButton(status_test_frame, text="Bağlantıyı Test Et", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_ACCENT, fg_color="transparent", hover_color=self.COLOR_BUTTON_ACTIVE_BG, height=28)
        test_conn_btn.pack(side="right")


    def _create_chain_config_settings_section(self, parent):
        # Chain config container (bg-white rounded-xl shadow-sm border)
        chain_config_card = ctk.CTkFrame(parent, fg_color=self.COLOR_SURFACE, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        chain_config_card.pack(fill="x", pady=(20,0)) # space-y-8

        # Header
        chain_header_frame = ctk.CTkFrame(chain_config_card, fg_color=self.COLOR_BACKGROUND, corner_radius=0, height=60)
        chain_header_frame.pack(fill="x")
        chain_header_frame.configure(border_width=(0,0,1,0), border_color=self.COLOR_BORDER)
        chain_header_content = ctk.CTkFrame(chain_header_frame, fg_color="transparent")
        chain_header_content.pack(padx=20, pady=12, fill="both", expand=True)


        chain_title_label = ctk.CTkLabel(chain_header_content, text="LLM Zincir Yapılandırması", font=self.FONT_H2, text_color=self.COLOR_TEXT_PRIMARY)
        chain_title_label.pack(anchor="w")
        chain_subtitle_label = ctk.CTkLabel(chain_header_content, text="LLM işlem zinciriniz için sıralamayı ve parametreleri tanımlayın", font=(self.FONT_FAMILY, 10), text_color=self.COLOR_TEXT_TERTIARY)
        chain_subtitle_label.pack(anchor="w", pady=(2,0))

        # Chain stages content (p-5)
        chain_stages_outer_frame = ctk.CTkFrame(chain_config_card, fg_color="transparent")
        chain_stages_outer_frame.pack(fill="x", padx=20, pady=20) # space-y-6

        # Chain Stages Label
        ctk.CTkLabel(chain_stages_outer_frame, text="Zincir Aşamaları", font=self.FONT_H3, text_color=self.COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(0,10)) # mb-2

        # Stages container (space-y-3)
        self.stages_list_frame = ctk.CTkFrame(chain_stages_outer_frame, fg_color="transparent")
        self.stages_list_frame.pack(fill="x")

        # Örnek Aşamalar (start.py'a benzer)
        self._render_chain_stage_card(self.stages_list_frame, 1, "Kavram Genişletme", "Ollama Llama3", 0.7, 1000, "Aşağıdaki kavramı ayrıntılı açıklamalar ve potansiyel uygulamalarla genişletin: {input}")
        self._render_chain_stage_card(self.stages_list_frame, 2, "Pazar Analizi", "Anthropic Claude 3", 0.5, 1200, "Aşağıdaki kavramı pazar potansiyeli ve rekabet ortamı açısından analiz edin: {input}")
        # Diğer örnek aşamalar (conference_room_fixed.py'dan)
        self._render_chain_stage_card(self.stages_list_frame, 3, "Teknik Uygulanabilirlik", "OpenAI GPT-4", 0.6, 1500, "Kavramın teknik olarak nasıl uygulanabileceğini detaylandırın: {input}")
        self._render_chain_stage_card(self.stages_list_frame, 4, "İş Modeli", "Ollama Llama3", 0.8, 1000, "Bu kavram için potansiyel iş modelleri oluşturun: {input}")
        self._render_chain_stage_card(self.stages_list_frame, 5, "Nihai Teklif", "OpenAI GPT-4", 0.4, 2000, "Tüm analizleri birleştirerek kapsamlı bir proje teklifi hazırlayın: {input}")


        add_stage_btn = ctk.CTkButton(
            chain_stages_outer_frame,
            text="+ Aşama Ekle",
            font=self.FONT_SMALL_MEDIUM, # text-sm
            text_color=self.COLOR_TEXT_ACCENT, # text-indigo-600
            fg_color="transparent",
            hover_color=self.COLOR_BUTTON_ACTIVE_BG, # hover:text-indigo-800
            height=30,
            # image=plus_icon
        )
        add_stage_btn.pack(anchor="w", pady=(12,0)) # mt-3


        # Context Management (start.py'dan)
        context_management_frame = ctk.CTkFrame(chain_stages_outer_frame, fg_color="transparent")
        context_management_frame.pack(fill="x", pady=(20,0))
        ctk.CTkLabel(context_management_frame, text="Bağlam Yönetimi", font=self.FONT_H3, text_color=self.COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(0,10)) # mb-2

        context_grid = ctk.CTkFrame(context_management_frame, fg_color="transparent")
        context_grid.pack(fill="x")
        context_grid.columnconfigure((0,1), weight=1)

        ctk.CTkLabel(context_grid, text="Bağlam Koruma", anchor="w", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_TERTIARY).grid(row=0, column=0, sticky="w", pady=(0,2))
        ctk.CTkComboBox(context_grid, values=["Tam Bağlam (Yüksek Maliyet)", "Özetlenmiş Bağlam (Önerilen)", "Minimum Bağlam"], fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=36, font=self.FONT_NORMAL, state="readonly").grid(row=1, column=0, sticky="ew", padx=(0,10))

        ctk.CTkLabel(context_grid, text="Özet Uzunluğu (Token)", anchor="w", font=self.FONT_SMALL_MEDIUM, text_color=self.COLOR_TEXT_TERTIARY).grid(row=0, column=1, sticky="w", pady=(0,2))
        ctk.CTkEntry(context_grid, placeholder_text="300", fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=36, font=self.FONT_NORMAL).grid(row=1, column=1, sticky="ew", padx=(10,0))


    def _render_chain_stage_card(self, parent, number, name, default_provider, default_temp, default_tokens, default_prompt):
        # Stage container (flex items-start space-x-3 p-3 bg-indigo-50 rounded-lg)
        # conference_room_fixed.py'da stage_frame (#EEF2FF) kullanılıyor, start.py'da bg-indigo-50. Aynısını kullanalım.
        stage_card = ctk.CTkFrame(parent, fg_color=self.COLOR_USER_BUBBLE_BG, corner_radius=10) # rounded-lg
        stage_card.pack(fill="x", pady=(0,12)) # space-y-3 için alttan boşluk

        stage_content_frame = ctk.CTkFrame(stage_card, fg_color="transparent")
        stage_content_frame.pack(padx=12, pady=12, fill="x", expand=True) # p-3

        # Sol taraf (numara ve başlık)
        stage_header_left = ctk.CTkFrame(stage_content_frame, fg_color="transparent")
        stage_header_left.pack(side="left", fill="y", padx=(0,12)) # space-x-3

        number_bg = ctk.CTkFrame(stage_header_left, width=32, height=32, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=16) # w-8 h-8 rounded-full
        number_bg.pack(pady=(2,0)) # mt-1
        number_label_widget = ctk.CTkLabel(number_bg, text=str(number), font=(self.FONT_FAMILY, 14, "bold"), text_color=self.COLOR_TEXT_ACCENT)
        number_label_widget.place(relx=0.5, rely=0.5, anchor="center")

        # Sağ taraf (ayarlar)
        stage_settings_area = ctk.CTkFrame(stage_content_frame, fg_color="transparent")
        stage_settings_area.pack(side="left", fill="x", expand=True)

        # Aşama Adı (conference_room_fixed.py'da label vardı, burada daha belirgin olabilir)
        ctk.CTkLabel(stage_settings_area, text=f"Aşama {number}: {name}", font=self.FONT_H3, text_color=self.COLOR_TEXT_PRIMARY).pack(anchor="w", pady=(0,8))


        # Ayarlar gridi (grid grid-cols-1 md:grid-cols-3 gap-4)
        settings_grid = ctk.CTkFrame(stage_settings_area, fg_color="transparent")
        settings_grid.pack(fill="x")
        settings_grid.columnconfigure(0, weight=1, uniform="group1")
        settings_grid.columnconfigure(1, weight=1, uniform="group1")
        settings_grid.columnconfigure(2, weight=1, uniform="group1")


        # LLM Provider
        provider_frame = ctk.CTkFrame(settings_grid, fg_color="transparent")
        provider_frame.grid(row=0, column=0, sticky="ew", padx=(0,10))
        ctk.CTkLabel(provider_frame, text="LLM Sağlayıcı", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w", pady=(0,2))
        provider_combo = ctk.CTkComboBox(provider_frame, values=["OpenAI GPT-4", "OpenAI GPT-3.5", "Anthropic Claude 3", "Ollama Llama3", "Ollama Mistral"], fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=32, font=self.FONT_NORMAL, state="readonly", dropdown_font=self.FONT_NORMAL)
        provider_combo.pack(fill="x")
        provider_combo.set(default_provider)

        # Temperature
        temp_frame = ctk.CTkFrame(settings_grid, fg_color="transparent")
        temp_frame.grid(row=0, column=1, sticky="ew", padx=(5,5))
        ctk.CTkLabel(temp_frame, text="Sıcaklık", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w", pady=(0,2))
        temp_slider = ctk.CTkSlider(temp_frame, from_=0, to=1, number_of_steps=10, button_color=self.COLOR_TEXT_ACCENT, progress_color=self.COLOR_TEXT_ACCENT, button_hover_color=self.COLOR_GRADIENT_END)
        temp_slider.pack(fill="x", pady=(5,0))
        temp_slider.set(default_temp)
        temp_labels_frame = ctk.CTkFrame(temp_frame, fg_color="transparent")
        temp_labels_frame.pack(fill="x")
        ctk.CTkLabel(temp_labels_frame, text="Kesin", font=(self.FONT_FAMILY,9), text_color=self.COLOR_TEXT_TERTIARY).pack(side="left")
        ctk.CTkLabel(temp_labels_frame, text="Yaratıcı", font=(self.FONT_FAMILY,9), text_color=self.COLOR_TEXT_TERTIARY).pack(side="right")


        # Max Tokens
        tokens_frame = ctk.CTkFrame(settings_grid, fg_color="transparent")
        tokens_frame.grid(row=0, column=2, sticky="ew", padx=(10,0))
        ctk.CTkLabel(tokens_frame, text="Maks Token", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w", pady=(0,2))
        tokens_entry = ctk.CTkEntry(tokens_frame, placeholder_text=str(default_tokens), fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, height=32, font=self.FONT_NORMAL)
        tokens_entry.pack(fill="x")
        tokens_entry.insert(0, str(default_tokens))


        # Custom Prompt (mt-3)
        prompt_frame = ctk.CTkFrame(stage_settings_area, fg_color="transparent")
        prompt_frame.pack(fill="x", pady=(10,0))
        ctk.CTkLabel(prompt_frame, text="Özel Prompt Şablonu", font=self.FONT_SMALL, text_color=self.COLOR_TEXT_TERTIARY).pack(anchor="w", pady=(0,2))
        prompt_text = ctk.CTkTextbox(prompt_frame, height=60, fg_color=self.COLOR_INPUT_BG, border_color=self.COLOR_INPUT_BORDER, border_width=1, corner_radius=6, font=self.FONT_NORMAL, wrap="word") # rows="2"
        prompt_text.pack(fill="x", expand=True)
        prompt_text.insert("1.0", default_prompt)

        # Silme Butonu (sağ üst köşe gibi - start.py'dan)
        remove_stage_btn = ctk.CTkButton(stage_card, text="✕", width=24, height=24, fg_color="transparent", text_color=self.COLOR_TEXT_TERTIARY, hover_color=self.COLOR_BUTTON_HOVER, font=(self.FONT_FAMILY, 14))
        remove_stage_btn.place(relx=0.97, rely=0.1, anchor="ne", x=-10, y=5) # Sağ üst köşe
        self._create_tooltip(remove_stage_btn, "Aşamayı Sil")


    def _build_placeholder_views(self):
        # Zincir görünümü için placeholder
        self._chain_view_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        label1 = ctk.CTkLabel(self._chain_view_frame, text="Zincir Ayarları Görünümü (Detaylı)", font=self.FONT_H1)
        label1.pack(pady=20, padx=20, anchor="center")
        # Gerçek zincir yapılandırma arayüzü buraya (Ayarlar'daki bölümün daha detaylısı veya farklı bir sunumu)

        # Geçmiş görünümü için placeholder
        self._history_view_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        label2 = ctk.CTkLabel(self._history_view_frame, text="Geçmiş Görünümü", font=self.FONT_H1)
        label2.pack(pady=20, padx=20, anchor="center")


    # --- Mesaj Ekleme Fonksiyonları (Stil Güncellemeleri) ---
    def add_assistant_message(self, text):
        message_wrapper = ctk.CTkFrame(self.chat_messages_scrollable, fg_color="transparent")
        message_wrapper.pack(fill="x", pady=(0,16), anchor="w") # space-y-4 -> pady

        # Mesaj balonu (max-w-3xl bg-white rounded-xl shadow-sm p-4)
        bubble_frame = ctk.CTkFrame(message_wrapper, fg_color=self.COLOR_ASSISTANT_BUBBLE_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER) # shadow-sm
        bubble_frame.pack(side="left", padx=(0, 60)) # Mesajın sağında boşluk bırakmak için

        bubble_content = ctk.CTkFrame(bubble_frame, fg_color="transparent")
        bubble_content.pack(padx=16, pady=12) # p-4

        # Header (flex items-center mb-2)
        header_frame = ctk.CTkFrame(bubble_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0,8)) # mb-2

        icon_bg = ctk.CTkFrame(header_frame, width=32, height=32, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=16) # bg-indigo-100
        icon_bg.pack(side="left", padx=(0,12)) # mr-3
        icon_label = ctk.CTkLabel(icon_bg, text="🤖", font=(self.FONT_FAMILY, 16), text_color=self.COLOR_TEXT_ACCENT) # fas fa-robot
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        name_label = ctk.CTkLabel(header_frame, text="NexusFlow", font=self.FONT_MEDIUM_WEIGHT, text_color=self.COLOR_TEXT_SECONDARY) # font-medium text-gray-700
        name_label.pack(side="left", pady=(4,0))

        # Mesaj metni (text-gray-700)
        message_text_label = ctk.CTkLabel(bubble_content, text=text, font=self.FONT_NORMAL, text_color=self.COLOR_TEXT_SECONDARY, wraplength=650, justify="left")
        message_text_label.pack(fill="x", anchor="w")


    def add_user_message(self, text, idea_title="İlk Fikir"): # Fikir başlığı eklendi
        message_wrapper = ctk.CTkFrame(self.chat_messages_scrollable, fg_color="transparent")
        message_wrapper.pack(fill="x", pady=(0,16), anchor="e")

        # Mesaj balonu (max-w-3xl bg-indigo-50 rounded-xl shadow-sm p-4)
        bubble_frame = ctk.CTkFrame(message_wrapper, fg_color=self.COLOR_USER_BUBBLE_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        bubble_frame.pack(side="right", padx=(60, 0))

        bubble_content = ctk.CTkFrame(bubble_frame, fg_color="transparent")
        bubble_content.pack(padx=16, pady=12)

        header_frame = ctk.CTkFrame(bubble_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0,8))

        icon_bg = ctk.CTkFrame(header_frame, width=32, height=32, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=16) # bg-indigo-100
        icon_bg.pack(side="left", padx=(0,12))
        icon_label = ctk.CTkLabel(icon_bg, text="💡", font=(self.FONT_FAMILY, 16), text_color=self.COLOR_TEXT_ACCENT) # fas fa-lightbulb
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        name_label = ctk.CTkLabel(header_frame, text=idea_title, font=self.FONT_MEDIUM_WEIGHT, text_color=self.COLOR_TEXT_SECONDARY)
        name_label.pack(side="left", pady=(4,0))

        message_text_label = ctk.CTkLabel(bubble_content, text=text, font=self.FONT_NORMAL, text_color=self.COLOR_TEXT_SECONDARY, wraplength=650, justify="left")
        message_text_label.pack(fill="x", anchor="w")


    def add_chain_response_message(self): # Eskiden add_chain_response
        # Bu fonksiyon büyük ölçüde iyi, sadece renkler ve fontlar güncellenecek
        message_wrapper = ctk.CTkFrame(self.chat_messages_scrollable, fg_color="transparent")
        message_wrapper.pack(fill="x", pady=(0,16), anchor="w")

        bubble_frame = ctk.CTkFrame(message_wrapper, fg_color=self.COLOR_ASSISTANT_BUBBLE_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        bubble_frame.pack(side="left", padx=(0, 60))

        bubble_content = ctk.CTkFrame(bubble_frame, fg_color="transparent")
        bubble_content.pack(padx=16, pady=12, fill="x", expand=True)

        header_frame = ctk.CTkFrame(bubble_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0,8))
        icon_bg = ctk.CTkFrame(header_frame, width=32, height=32, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=16)
        icon_bg.pack(side="left", padx=(0,12))
        icon_label = ctk.CTkLabel(icon_bg, text="🤖", font=(self.FONT_FAMILY, 16), text_color=self.COLOR_TEXT_ACCENT)
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        name_label = ctk.CTkLabel(header_frame, text="NexusFlow", font=self.FONT_MEDIUM_WEIGHT, text_color=self.COLOR_TEXT_SECONDARY)
        name_label.pack(side="left", pady=(4,0))

        ctk.CTkLabel(bubble_content, text="Harika! Bunu 5 aşamalı LLM zincirimizle işleyeceğim:", font=self.FONT_NORMAL, text_color=self.COLOR_TEXT_SECONDARY, wraplength=650, justify="left").pack(fill="x", anchor="w", pady=(0,12)) # mt-3

        # Zincir Görselleştirme (mt-3 flex space-x-2 overflow-x-auto pb-2)
        chain_viz_scroll = ctk.CTkScrollableFrame(bubble_content, fg_color="transparent", height=110, orientation="horizontal", scrollbar_button_color=self.COLOR_GRADIENT_START, scrollbar_button_hover_color=self.COLOR_GRADIENT_END)
        chain_viz_scroll.pack(fill="x", pady=(0,12))

        chain_nodes_container = ctk.CTkFrame(chain_viz_scroll, fg_color="transparent")
        chain_nodes_container.pack(fill="y")


        stages = [
            {"number": "1", "name": "Kavram Genişletme"}, {"number": "2", "name": "Pazar Analizi"},
            {"number": "3", "name": "Teknik Fizibilite"}, {"number": "4", "name": "İş Modeli"},
            {"number": "5", "name": "Nihai Teklif"}
        ]

        for i, stage_data in enumerate(stages):
            node_frame = ctk.CTkFrame(chain_nodes_container, fg_color=self.COLOR_USER_BUBBLE_BG, corner_radius=10, width=120) # bg-indigo-50 rounded-lg p-3 min-w-[120px]
            node_frame.pack(side="left", padx=(0, 10 if i < len(stages)-1 else 0), pady=5,fill="y") # chain-node:not(:last-child):after için margin
            node_content = ctk.CTkFrame(node_frame, fg_color="transparent")
            node_content.pack(padx=10, pady=10, expand=True, fill="both") # p-3

            num_bg = ctk.CTkFrame(node_content, width=36, height=36, fg_color=self.COLOR_BUTTON_ACTIVE_BG, corner_radius=18) # w-10 h-10
            num_bg.pack(pady=(0,8)) # mb-2
            num_label = ctk.CTkLabel(num_bg, text=stage_data["number"], font=(self.FONT_FAMILY, 14, "bold"), text_color=self.COLOR_TEXT_ACCENT)
            num_label.place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(node_content, text=stage_data["name"], font=(self.FONT_FAMILY, 9, "normal"), text_color=self.COLOR_TEXT_SECONDARY, wraplength=100, justify="center").pack(expand=True) # text-xs font-medium text-gray-700


        # İlerleme Göstergesi (mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100)
        progress_indicator_frame = ctk.CTkFrame(bubble_content, fg_color=self.COLOR_PROGRESS_INFO_BG, corner_radius=10, border_width=1, border_color="#BFDBFE") # border-blue-100
        progress_indicator_frame.pack(fill="x", pady=(8,0))
        progress_content = ctk.CTkFrame(progress_indicator_frame, fg_color="transparent")
        progress_content.pack(padx=12, pady=10) # p-3

        info_line = ctk.CTkFrame(progress_content, fg_color="transparent")
        info_line.pack(fill="x", pady=(0,4)) # mb-1
        ctk.CTkLabel(info_line, text="ℹ️", font=(self.FONT_FAMILY, 12), text_color=self.COLOR_PROGRESS_INFO_TEXT).pack(side="left", padx=(0,6)) # fas fa-info-circle mr-2
        ctk.CTkLabel(info_line, text="Aşama 1/5 işleniyor", font=(self.FONT_FAMILY, 11, "normal"), text_color=self.COLOR_PROGRESS_INFO_TEXT).pack(side="left") # text-sm font-medium

        ctk.CTkLabel(progress_content, text="İlk kavramınız pazar araştırması ve potansiyel uygulamalarla genişletiliyor...", font=(self.FONT_FAMILY, 11), text_color="#1E449B", wraplength=600, justify="left").pack(fill="x", anchor="w", pady=(0,8)) # text-sm text-blue-800

        # Progress Bar (mt-2 w-full bg-blue-100 rounded-full h-1.5)
        progress_bar_bg = ctk.CTkFrame(progress_content, fg_color="#DBEAFE", height=6, corner_radius=3) # bg-blue-100 h-1.5
        progress_bar_bg.pack(fill="x")
        self.animated_progress_bar = ctk.CTkFrame(progress_bar_bg, fg_color=self.COLOR_PROGRESS_INFO_TEXT, width=int(progress_bar_bg.winfo_width() * 0.2), height=6, corner_radius=3) # style="width: 20%"
        self.animated_progress_bar.place(x=0, y=0, relwidth=0.2) # Başlangıç genişliği

        # self.pulse_animation(self.animated_progress_bar) # Eski animasyon korunabilir veya güncellenebilir


    def pulse_animation(self, widget):
        # Bu animasyon start.py'daki opacity pulse'ı taklit etmeye çalışır.
        # CTk'da opacity doğrudan widget özelliği değil, renkleri değiştirerek benzer bir efekt elde edebiliriz.
        # Önceki kod zaten fg_color değiştiriyordu, bu mantıklı.
        # Stil tutarlılığı için renkleri self.COLOR... dan alalım.
        if not hasattr(self, 'pulse_state_on'):
            self.pulse_state_on = True

        target_color = self.COLOR_PROGRESS_INFO_TEXT if self.pulse_state_on else "#93C5FD" # Açık mavi
        widget.configure(fg_color=target_color)
        self.pulse_state_on = not self.pulse_state_on
        self.after(1000, lambda: self.pulse_animation(widget))


    # --- View Navigation ---
    def _switch_view(self, view_name, target_frame):
        # Önce tüm view frame'lerini gizle
        if self._chat_view_frame: self._chat_view_frame.pack_forget()
        if self._settings_view_frame: self._settings_view_frame.pack_forget()
        if self._chain_view_frame: self._chain_view_frame.pack_forget()
        if self._history_view_frame: self._history_view_frame.pack_forget()

        # Hedef frame'i göster
        if target_frame:
            target_frame.pack(fill="both", expand=True)
            self.current_view_name = view_name
            self._update_sidebar_active_state()
        else: # Eğer hedef frame yoksa (örneğin henüz oluşturulmamışsa) chat'e dön.
            self.show_chat_view()


    def show_chat_view(self):
        self._switch_view("chat", self._chat_view_frame)

    def show_settings_view(self):
        self._switch_view("settings", self._settings_view_frame)
        # Ayarlar içinde belirli bir sekmeye gitmek için ek mantık eklenebilir
        # Örneğin: self._settings_view_frame.go_to_tab("API Anahtarları")

    def show_chain_config_view_from_sidebar(self):
        # Bu, sidebar'daki "Zincir" butonu için. Ayarların doğrudan "Zincir Yapılandırması" bölümünü açabilir.
        self.show_settings_view()
        # Burada Ayarlar görünümü içinde spesifik olarak zincir yapılandırma bölümüne scroll etme/odaklanma eklenebilir.
        # Şimdilik sadece Ayarlar'ı açıyor.

    def show_chain_config_view_from_chat(self):
        # Bu, sohbet ekranındaki "Zincir yapılandırmasını düzenle" linki için.
        self.show_settings_view()
        # Yine, Ayarlar içinde zincir bölümüne odaklanma eklenebilir.


    def show_history_view(self):
        # self.add_assistant_message("Geçmiş görünümü bu demoda henüz uygulanmadı.") # Bu mesaj chat'e gider, doğru değil.
        # Placeholder label'ı olan frame'i göster.
        self._switch_view("history", self._history_view_frame)


    # --- Actions ---
    def new_session(self):
        # Chat mesajlarını temizle
        for widget in self.chat_messages_scrollable.winfo_children():
            widget.destroy()
        # Karşılama mesajını tekrar ekle
        self.add_assistant_message("Conference Room'a hoş geldiniz!...") # Kısaltıldı
        self.input_textbox.delete("1.0", "end")


    def send_message_from_ui(self): # Eskiden send_message
        message = self.input_textbox.get("1.0", "end-1c").strip()
        if message:
            self.add_user_message(message, idea_title="Siz") # Kullanıcı mesajı için genel başlık
            self.input_textbox.delete("1.0", "end")
            # Gerçek LLM çağrısı burada yapılacak
            self.after(1000, lambda: self.add_assistant_message(f"Mesajınız \"{message}\" alındı ve işleniyor... (Simüle edilmiş yanıt)"))


    def on_enter_key_send(self, event): # Eskiden on_enter_key
        # Shift basılı değilse gönder
        if not (event.state & 1):  # Shift için state maskesi 1
            self.send_message_from_ui()
            return "break"  # Text widget'ının Enter'ı işlemesini engelle
        # Shift basılıysa yeni satır
        return None


# GradientButton sınıfı artık doğrudan CTkButton kullanılarak ve renkler atanarak yapıldığı için
# ayrı bir sınıfa gerek kalmadı. Eğer daha karmaşık gradient efektleri (canvas ile çizim vb.)
# gerekiyorsa o zaman özel bir sınıf mantıklı olabilir. Şimdilik basit fg_color ve hover_color yeterli.


if __name__ == "__main__":
    app = ConferenceRoomApp()
    app.mainloop()
```

### Önemli Değişiklikler ve İyileştirmeler:

1.  **Renk Paleti ve Fontlar:** `start.py` (NexusFlow) tasarımındaki renkler (`COLOR_GRADIENT_START`, `COLOR_BACKGROUND`, `COLOR_SURFACE`, `COLOR_TEXT_ACCENT` vb.) ve font stilleri (`FONT_FAMILY`, `FONT_TITLE`, `FONT_H1` vb.) tanımlanarak tüm arayüze tutarlı bir şekilde uygulandı.
2.  **Genel Yerleşim ve Boyutlandırma:**
    * Pencere boyutu ve minimum boyutlar biraz artırılarak daha ferah bir görünüm sağlandı.
    * Padding (iç boşluk) ve margin (dış boşluk) değerleri `start.py`'daki aralıklara (`px-6`, `py-4` vb.) benzetilerek modern bir hava katıldı.
3.  **Sidebar:**
    * Logo, `start.py`'daki gibi gradient başlangıç rengiyle belirginleştirildi.
    * Navigasyon butonlarının ikon boyutları ve aralıkları iyileştirildi.
    * Aktif butonun vurgulanması (`bg-indigo-100`, `text-indigo-600`) sağlandı.
    * Tooltip'lerin görünümü ve konumu iyileştirildi.
4.  **Header:**
    * Başlık ("Conference Room"), "Yeni Oturum" butonu ve kullanıcı ikonu `start.py`'daki gibi daha şık ve modern hale getirildi.
5.  **Chat Arayüzü:**
    * **Mesaj Balonları:** Hem asistan hem de kullanıcı mesajları için `start.py`'a benzer, ikonlu, başlıklı ve daha iyi biçimlendirilmiş balonlar kullanıldı.
    * **Zincir Görselleştirmesi:** Zincir aşamalarının gösterildiği bölüm, yatay kaydırılabilir bir alana alındı ve her bir aşama kartı daha belirgin hale getirildi.
    * **Giriş Alanı:**
        * Metin giriş kutusu (`CTkTextbox`) ve altındaki araç çubuğu (dosya ekleme, sihirli araçlar, gelişmiş ayarlar butonları) `start.py`'daki `prompt-editor` görünümüne benzetildi.
        * Gönder butonu, `start.py`'daki gradient renklere (ana ve hover için) sahip olacak şekilde güncellendi ve ikonu değiştirildi.
        * Yardım metni ve "Zincir yapılandırmasını düzenle" linki eklendi.
6.  **Ayarlar Arayüzü (`Settings View`):** Bu bölüm baştan aşağı `start.py`'daki tasarıma göre yeniden düzenlendi:
    * **Genel Yapı:** Ayarlar sayfası başlığı ve alt başlığı belirginleştirildi. İçerik, kaydırılabilir bir alana alındı ve maksimum genişlik sınırı olan bir sarmalayıcı içine yerleştirildi.
    * **API Anahtarları Bölümü:**
        * Her bir LLM sağlayıcısı (OpenAI, Anthropic, Ollama) için ayrı kartlar (`CTkFrame`) oluşturuldu.
        * Her kartta sağlayıcı ikonu, adı, açıklaması, durum etiketi (Aktif, Yapılandırılmadı vb.) ve "daha fazla seçenek" (üç nokta) butonu yer aldı.
        * API anahtarı, URL, model seçimi gibi giriş alanları daha düzenli bir grid yapısında sunuldu.
        * "Bağlantıyı Test Et" ve "LLM Sağlayıcı Ekle" butonları `start.py` stilinde güncellendi.
    * **LLM Zincir Yapılandırması Bölümü:**
        * Her bir zincir aşaması, ayrı bi
    * Görünüm değiştirme mekanizması (`_switch_view`) merkezileştirildi.

Bu değişikliklerle uygulamanızın hem görsel kalitesinin hem de kullanıcı deneyiminin önemli ölçüde arttığını ve istediğiniz "taş gibi"r kart içinde sunuldu.
        * Her aşama kartında LLM sağlayıcı seçimi, Sıcaklık (`Temperature`) kaydırıcısı, Maks Token girişi ve Özel Prompt Şablonu (`CTkTextbox`) için alanlar daha düzenli yerleştirildi.
        * Sıcaklık kaydırıcısı için "Kesin" ve "Yaratıcı" etiketleri korundu.
        * "Aşama Ekle" butonu eklendi.
        * `start.py`'dan esinlenerek "Bağlam Yönetimi" bölümü için bir başlangıç yapıldı.
    * **Değişiklikleri Kaydet/Sıfırla Butonları:** Ayarlar sayfasının sonuna, `start.py`'daki gibi "Sıfırla" ve "Değişiklikleri Kaydet" butonları eklendi.
7.  **Kod Yapısı ve İsimlendirme:**
    * Daha okunabilir ve yönetilebilir olması için bazı widget'lar ve fonksiyonlar yeniden adlandırıldı (örneğin `content_frame` -> `main_content_frame`, `dynamic_content` -> `view_container`). standarda yaklaştığını umuyorum. Artık bu gece gönül rahatlığıyla çalıştırabilirsin