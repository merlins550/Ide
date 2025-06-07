import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import io
import base64
import webbrowser
from datetime import datetime

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ConferenceRoomApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Conference Room")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Set icon if available
        # self.iconbitmap("path/to/icon.ico")  # For Windows
        
        # Initialize UI components
        self.setup_ui()
        
        # Set default view
        self.show_chat_view()
        
    def setup_ui(self):
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color="#F9FAFB")
        self.main_container.pack(fill="both", expand=True)
        
        # Create sidebar and main content area
        self.create_sidebar()
        self.create_main_content()
        
    def create_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.main_container, width=60, fg_color="white", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        # Logo at the top
        self.logo_frame = ctk.CTkFrame(self.sidebar, width=50, height=50, fg_color="#6e8efb", corner_radius=8)
        self.logo_frame.pack(pady=(20, 30), padx=5)
        
        # Logo icon
        self.logo_label = ctk.CTkLabel(self.logo_frame, text="🔗", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Navigation buttons
        self.chat_btn = self.create_sidebar_button(self.sidebar, "💬", "Chat", True, self.show_chat_view)
        self.chain_btn = self.create_sidebar_button(self.sidebar, "🔗", "Chain", False, self.show_chain_view)
        self.history_btn = self.create_sidebar_button(self.sidebar, "🕒", "History", False, self.show_history_view)
        
        # Settings button at the bottom
        self.settings_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.settings_frame.pack(side="bottom", pady=(0, 20))
        self.settings_btn = self.create_sidebar_button(self.settings_frame, "⚙️", "Settings", False, self.show_settings_view)
        
    def create_sidebar_button(self, parent, icon, tooltip, active, command):
        btn_color = "#EEF2FF" if active else "transparent"
        text_color = "#4F46E5" if active else "#6B7280"
        
        btn = ctk.CTkButton(
            parent, 
            text=icon, 
            width=48, 
            height=48, 
            fg_color=btn_color,
            text_color=text_color,
            hover_color="#F3F4F6",
            font=ctk.CTkFont(size=20),
            corner_radius=8,
            command=command
        )
        btn.pack(pady=5)
        
        # Create tooltip
        self.create_tooltip(btn, tooltip)
        
        return btn
    
    def create_tooltip(self, widget, text):
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Create tooltip window
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=text, background="#333", foreground="white",
                           relief="solid", borderwidth=1, padx=5, pady=2, font=("Segoe UI", 10))
            label.pack()
            
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def create_main_content(self):
        # Main content frame
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="#F9FAFB", corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.content_frame, height=60, fg_color="white", corner_radius=0)
        self.header_frame.pack(fill="x")
        
        # App title
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Conference Room", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1F2937"
        )
        self.title_label.pack(side="left", padx=20, pady=15)
        
        # Right side of header
        self.header_right = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_right.pack(side="right", padx=20)
        
        # New session button
        self.new_session_btn = ctk.CTkButton(
            self.header_right,
            text="New Session",
            font=ctk.CTkFont(size=12),
            fg_color="#F3F4F6",
            text_color="#4B5563",
            hover_color="#E5E7EB",
            corner_radius=15,
            width=120,
            height=30,
            command=self.new_session
        )
        self.new_session_btn.pack(side="left", padx=(0, 15))
        
        # User icon
        self.user_frame = ctk.CTkFrame(self.header_right, width=32, height=32, fg_color="#EEF2FF", corner_radius=16)
        self.user_frame.pack(side="left")
        self.user_frame.pack_propagate(False)
        
        self.user_label = ctk.CTkLabel(self.user_frame, text="👤", font=ctk.CTkFont(size=16), text_color="#4F46E5")
        self.user_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Dynamic content area - will contain different views
        self.dynamic_content = ctk.CTkFrame(self.content_frame, fg_color="#F9FAFB")
        self.dynamic_content.pack(fill="both", expand=True)
        
        # Create different views
        self.create_chat_view()
        self.create_settings_view()
        
    def create_chat_view(self):
        # Chat view container
        self.chat_view = ctk.CTkFrame(self.dynamic_content, fg_color="#F9FAFB")
        
        # Chat messages area
        self.chat_messages = ctk.CTkScrollableFrame(self.chat_view, fg_color="#F9FAFB")
        self.chat_messages.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        self.add_assistant_message("Welcome to Conference Room! I'm your LLM chain automation assistant. Start by entering your idea or question below, and I'll guide it through our optimized LLM processing pipeline.")
        
        # Example user message
        self.add_user_message("I want to create an automated system that takes a basic product idea and develops it into a complete business plan using a chain of specialized LLMs.")
        
        # Response with chain visualization
        self.add_chain_response()
        
        # Input area at the bottom
        self.input_frame = ctk.CTkFrame(self.chat_view, height=150, fg_color="#F9FAFB")
        self.input_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        
        # Input container
        self.input_container = ctk.CTkFrame(self.input_frame, fg_color="#F9FAFB")
        self.input_container.pack(fill="x", pady=10)
        
        # Text input and send button
        self.input_box_frame = ctk.CTkFrame(self.input_container, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
        self.input_box_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.input_box = ctk.CTkTextbox(self.input_box_frame, height=100, fg_color="white", activate_scrollbars=True)
        self.input_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.input_box.bind("<Return>", self.on_enter_key)
        
        # Toolbar under text input
        self.toolbar = ctk.CTkFrame(self.input_box_frame, height=40, fg_color="white")
        self.toolbar.pack(fill="x", padx=10, pady=(0, 5))
        
        # Attachment and magic buttons
        self.attachment_btn = ctk.CTkButton(
            self.toolbar, 
            text="📎", 
            width=30, 
            height=30, 
            fg_color="transparent",
            text_color="#6B7280",
            hover_color="#F3F4F6",
            corner_radius=4
        )
        self.attachment_btn.pack(side="left", padx=2)
        
        self.magic_btn = ctk.CTkButton(
            self.toolbar, 
            text="✨", 
            width=30, 
            height=30, 
            fg_color="transparent",
            text_color="#6B7280",
            hover_color="#F3F4F6",
            corner_radius=4
        )
        self.magic_btn.pack(side="left", padx=2)
        
        # Advanced button
        self.advanced_btn = ctk.CTkButton(
            self.toolbar, 
            text="⚙️ Advanced", 
            width=80, 
            height=25, 
            fg_color="transparent",
            text_color="#6B7280",
            hover_color="#F3F4F6",
            corner_radius=4,
            font=ctk.CTkFont(size=12)
        )
        self.advanced_btn.pack(side="right")
        
        # Send button with gradient
        self.send_btn = GradientButton(
            self.input_container, 
            text="📤", 
            width=48, 
            height=48, 
            corner_radius=8,
            command=self.send_message
        )
        self.send_btn.pack(side="right")
        
        # Help text
        self.help_text = ctk.CTkLabel(
            self.input_frame, 
            text="Conference Room will process your input through the configured LLM chain.",
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        )
        self.help_text.pack(side="left", padx=5, pady=(5, 0))
        
        # Edit chain configuration link
        self.edit_chain_link = ctk.CTkButton(
            self.input_frame, 
            text="Edit chain configuration", 
            font=ctk.CTkFont(size=10),
            fg_color="transparent",
            text_color="#4F46E5",
            hover_color="transparent",
            hover=True,
            width=30,
            height=15,
            command=self.show_settings_view
        )
        self.edit_chain_link.pack(side="left", pady=(5, 0))
        
    def create_settings_view(self):
        # Settings view container
        self.settings_view = ctk.CTkFrame(self.dynamic_content, fg_color="white")
        
        # Settings header
        self.settings_header = ctk.CTkFrame(self.settings_view, height=60, fg_color="white", corner_radius=0)
        self.settings_header.pack(fill="x", padx=20, pady=15)
        
        self.settings_title = ctk.CTkLabel(
            self.settings_header, 
            text="Settings & Configuration", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1F2937"
        )
        self.settings_title.pack(anchor="w")
        
        self.settings_subtitle = ctk.CTkLabel(
            self.settings_header, 
            text="Manage your API keys and LLM chain settings", 
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )
        self.settings_subtitle.pack(anchor="w")
        
        # Settings content
        self.settings_content = ctk.CTkScrollableFrame(self.settings_view, fg_color="white")
        self.settings_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # API Keys Section
        self.create_api_keys_section()
        
        # Chain Configuration Section
        self.create_chain_config_section()
        
    def create_api_keys_section(self):
        # API Keys container
        self.api_keys_container = ctk.CTkFrame(self.settings_content, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
        self.api_keys_container.pack(fill="x", pady=10)
        
        # Header
        self.api_keys_header = ctk.CTkFrame(self.api_keys_container, height=50, fg_color="#F9FAFB", corner_radius=0)
        self.api_keys_header.pack(fill="x")
        
        self.api_keys_title = ctk.CTkLabel(
            self.api_keys_header, 
            text="LLM Provider API Keys", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1F2937"
        )
        self.api_keys_title.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.api_keys_subtitle = ctk.CTkLabel(
            self.api_keys_header, 
            text="Configure access to different LLM providers in your chain", 
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )
        self.api_keys_subtitle.pack(anchor="w", padx=15, pady=(0, 10))
        
        # OpenAI section
        self.create_provider_section(
            "OpenAI", 
            "GPT-4, GPT-3.5 models", 
            "🤖", 
            "Active", 
            "#10B981", 
            "#ECFDF5",
            True
        )
        
        # Anthropic section
        self.create_provider_section(
            "Anthropic", 
            "Claude models", 
            "🧠", 
            "Not Configured", 
            "#FBBF24", 
            "#FFFBEB",
            False
        )
        
        # Ollama section
        self.create_provider_section(
            "Ollama", 
            "Local LLM models", 
            "💻", 
            "Self-Hosted", 
            "#3B82F6", 
            "#EFF6FF",
            True,
            True
        )
        
        # Add new provider button
        self.add_provider_frame = ctk.CTkFrame(self.api_keys_container, fg_color="white", height=60)
        self.add_provider_frame.pack(fill="x", padx=15, pady=15)
        
        self.add_provider_btn = ctk.CTkButton(
            self.add_provider_frame,
            text="+ Add LLM Provider",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color="#4F46E5",
            hover_color="#EEF2FF",
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=6,
            height=40
        )
        self.add_provider_btn.pack(fill="x")
        
    def create_provider_section(self, name, description, icon, status, status_color, status_bg, has_key=False, is_local=False):
        # Provider container
        provider_frame = ctk.CTkFrame(self.api_keys_container, fg_color="white", height=120)
        provider_frame.pack(fill="x", padx=15, pady=10)
        
        # Provider header with icon and status
        header_frame = ctk.CTkFrame(provider_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(5, 10))
        
        # Icon container
        icon_frame = ctk.CTkFrame(header_frame, width=40, height=40, fg_color="#F3F4F6", corner_radius=8)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text=icon, font=ctk.CTkFont(size=16), text_color="#4B5563")
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Provider info
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", padx=10)
        
        name_label = ctk.CTkLabel(
            info_frame, 
            text=name, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1F2937"
        )
        name_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            info_frame, 
            text=description, 
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        )
        desc_label.pack(anchor="w")
        
        # Status badge
        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        status_badge = ctk.CTkLabel(
            status_frame,
            text=status,
            font=ctk.CTkFont(size=10),
            text_color=status_color,
            fg_color=status_bg,
            corner_radius=4,
            width=30,
            height=20
        )
        status_badge.pack(side="left", padx=(0, 10))
        
        # Settings button
        settings_btn = ctk.CTkButton(
            status_frame,
            text="⋮",
            width=20,
            height=20,
            fg_color="transparent",
            text_color="#9CA3AF",
            hover_color="#F3F4F6",
            corner_radius=4
        )
        settings_btn.pack(side="right")
        
        # Form fields
        form_frame = ctk.CTkFrame(provider_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=(50, 0))
        
        # Different fields based on provider type
        if is_local:
            # Local provider (Ollama)
            form_grid = ctk.CTkFrame(form_frame, fg_color="transparent")
            form_grid.pack(fill="x")
            
            # URL field
            url_label = ctk.CTkLabel(
                form_grid, 
                text="Base URL", 
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4B5563"
            )
            url_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
            
            url_entry = ctk.CTkEntry(
                form_grid,
                placeholder_text="http://localhost:11434",
                width=250,
                height=30,
                border_color="#E5E7EB"
            )
            url_entry.grid(row=1, column=0, sticky="w", padx=(0, 20))
            if has_key:
                url_entry.insert(0, "http://localhost:11434")
            
            # Model field
            model_label = ctk.CTkLabel(
                form_grid, 
                text="Model", 
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4B5563"
            )
            model_label.grid(row=0, column=1, sticky="w", pady=(0, 5))
            
            model_combobox = ctk.CTkComboBox(
                form_grid,
                values=["llama3", "mistral", "gemma", "phi3", "Custom Model"],
                width=250,
                height=30,
                border_color="#E5E7EB"
            )
            model_combobox.grid(row=1, column=1, sticky="w")
            model_combobox.set("Custom Model")
            
            # Custom model name
            custom_label = ctk.CTkLabel(
                form_grid, 
                text="Custom Model Name", 
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4B5563"
            )
            custom_label.grid(row=2, column=0, sticky="w", pady=(10, 5))
            
            custom_entry = ctk.CTkEntry(
                form_grid,
                placeholder_text="my-custom-model",
                width=520,
                height=30,
                border_color="#E5E7EB"
            )
            custom_entry.grid(row=3, column=0, columnspan=2, sticky="w")
            
        else:
            # Cloud provider (OpenAI, Anthropic)
            form_grid = ctk.CTkFrame(form_frame, fg_color="transparent")
            form_grid.pack(fill="x")
            
            # API Key field
            key_label = ctk.CTkLabel(
                form_grid, 
                text="API Key", 
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4B5563"
            )
            key_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
            
            key_entry = ctk.CTkEntry(
                form_grid,
                placeholder_text="Enter your API key",
                width=250,
                height=30,
                border_color="#E5E7EB",
                show="*"
            )
            key_entry.grid(row=1, column=0, sticky="w", padx=(0, 20))
            if has_key:
                key_entry.insert(0, "sk-********************")
            
            # Organization field (for OpenAI)
            if name == "OpenAI":
                org_label = ctk.CTkLabel(
                    form_grid, 
                    text="Organization", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#4B5563"
                )
                org_label.grid(row=0, column=1, sticky="w", pady=(0, 5))
                
                org_entry = ctk.CTkEntry(
                    form_grid,
                    placeholder_text="org-****************",
                    width=250,
                    height=30,
                    border_color="#E5E7EB"
                )
                org_entry.grid(row=1, column=1, sticky="w")
                if has_key:
                    org_entry.insert(0, "org-****************")
        
        # Status and test connection
        status_bar = ctk.CTkFrame(form_frame, fg_color="transparent", height=30)
        status_bar.pack(fill="x", pady=(10, 0))
        
        if has_key:
            status_indicator = ctk.CTkFrame(status_bar, width=8, height=8, fg_color="#10B981", corner_radius=4)
            status_indicator.pack(side="left")
            
            if is_local:
                status_text = ctk.CTkLabel(
                    status_bar, 
                    text="Connected to local Ollama instance", 
                    font=ctk.CTkFont(size=10),
                    text_color="#6B7280"
                )
            else:
                status_text = ctk.CTkLabel(
                    status_bar, 
                    text="Last used: 5 min ago", 
                    font=ctk.CTkFont(size=10),
                    text_color="#6B7280"
                )
            status_text.pack(side="left", padx=5)
        
        test_btn = ctk.CTkButton(
            status_bar,
            text="Test Connection",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color="#4F46E5",
            hover_color="transparent",
            width=30,
            height=20
        )
        test_btn.pack(side="right")
        
    def create_chain_config_section(self):
        # Chain config container
        self.chain_config_container = ctk.CTkFrame(self.settings_content, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
        self.chain_config_container.pack(fill="x", pady=10)
        
        # Header
        self.chain_config_header = ctk.CTkFrame(self.chain_config_container, height=50, fg_color="#F9FAFB", corner_radius=0)
        self.chain_config_header.pack(fill="x")
        
        self.chain_config_title = ctk.CTkLabel(
            self.chain_config_header, 
            text="LLM Chain Configuration", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1F2937"
        )
        self.chain_config_title.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.chain_config_subtitle = ctk.CTkLabel(
            self.chain_config_header, 
            text="Define the sequence and parameters for your LLM processing chain", 
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        )
        self.chain_config_subtitle.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Chain stages
        self.chain_stages_frame = ctk.CTkFrame(self.chain_config_container, fg_color="white")
        self.chain_stages_frame.pack(fill="x", padx=15, pady=15)
        
        self.chain_stages_label = ctk.CTkLabel(
            self.chain_stages_frame, 
            text="Chain Stages", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4B5563"
        )
        self.chain_stages_label.pack(anchor="w", pady=(0, 10))
        
        # Stage 1
        self.create_chain_stage(1, "Concept Expansion")
        
        # Stage 2
        self.create_chain_stage(2, "Market Analysis")
        
        # Stage 3
        self.create_chain_stage(3, "Technical Feasibility")
        
        # Stage 4
        self.create_chain_stage(4, "Business Model")
        
        # Stage 5
        self.create_chain_stage(5, "Final Proposal")
        
        # Add stage button
        self.add_stage_btn = ctk.CTkButton(
            self.chain_stages_frame,
            text="+ Add Stage",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color="#4F46E5",
            hover_color="#EEF2FF",
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=6,
            height=40
        )
        self.add_stage_btn.pack(fill="x", pady=(10, 0))
        
    def create_chain_stage(self, number, name):
        # Stage container
        stage_frame = ctk.CTkFrame(self.chain_stages_frame, fg_color="#EEF2FF", corner_radius=8)
        stage_frame.pack(fill="x", pady=5)
        
        # Stage header
        header_frame = ctk.CTkFrame(stage_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Number badge
        number_frame = ctk.CTkFrame(header_frame, width=30, height=30, fg_color="#E0E7FF", corner_radius=15)
        number_frame.pack(side="left")
        number_frame.pack_propagate(False)
        
        number_label = ctk.CTkLabel(number_frame, text=str(number), font=ctk.CTkFont(size=14, weight="bold"), text_color="#4F46E5")
        number_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Stage name
        name_label = ctk.CTkLabel(
            header_frame, 
            text=name, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4B5563"
        )
        name_label.pack(side="left", padx=10)
        
        # Settings
        settings_frame = ctk.CTkFrame(stage_frame, fg_color="transparent")
        settings_frame.pack(fill="x", padx=50, pady=(0, 10))
        
        # Provider selection
        provider_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        provider_frame.pack(fill="x", pady=5)
        
        provider_label = ctk.CTkLabel(
            provider_frame, 
            text="LLM Provider", 
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        )
        provider_label.pack(anchor="w")
        
        provider_combobox = ctk.CTkComboBox(
            provider_frame,
            values=["OpenAI GPT-4", "OpenAI GPT-3.5", "Anthropic Claude 3", "Ollama Llama3"],
            width=200,
            height=30,
            border_color="#E5E7EB"
        )
        provider_combobox.pack(anchor="w", pady=(5, 0))
        provider_combobox.set("Ollama Llama3")
        
        # Temperature slider
        temp_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        temp_frame.pack(fill="x", pady=5)
        
        temp_label = ctk.CTkLabel(
            temp_frame, 
            text="Temperature", 
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        )
        temp_label.pack(anchor="w")
        
        temp_slider = ctk.CTkSlider(
            temp_frame,
            from_=0,
            to=1,
            number_of_steps=10,
            width=200
        )
        temp_slider.pack(anchor="w", pady=(5, 0))
        temp_slider.set(0.7)
        
        # Labels for slider
        labels_frame = ctk.CTkFrame(temp_frame, fg_color="transparent")
        labels_frame.pack(fill="x", pady=(5, 0))
        
        precise_label = ctk.CTkLabel(
            labels_frame, 
            text="Precise", 
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        )
        precise_label.pack(side="left")
        
        creative_label = ctk.CTkLabel(
            labels_frame, 
            text="Creative", 
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        )
        creative_label.pack(side="right")
        
    def add_assistant_message(self, text):
        # Message container
        message_frame = ctk.CTkFrame(self.chat_messages, fg_color="transparent")
        message_frame.pack(fill="x", pady=5, anchor="w")
        
        # Message bubble
        bubble = ctk.CTkFrame(message_frame, fg_color="white", corner_radius=12)
        bubble.pack(side="left", fill="x", padx=(0, 100))
        
        # Header with icon
        header = ctk.CTkFrame(bubble, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        # Icon
        icon_frame = ctk.CTkFrame(header, width=32, height=32, fg_color="#EEF2FF", corner_radius=16)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text="🤖", font=ctk.CTkFont(size=16), text_color="#4F46E5")
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Name
        name_label = ctk.CTkLabel(
            header, 
            text="Conference Room", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4B5563"
        )
        name_label.pack(side="left", padx=10)
        
        # Message text
        message_label = ctk.CTkLabel(
            bubble, 
            text=text, 
            font=ctk.CTkFont(size=12),
            text_color="#4B5563",
            wraplength=600,
            justify="left"
        )
        message_label.pack(fill="x", padx=10, pady=(0, 10), anchor="w")
        
    def add_user_message(self, text):
        # Message container
        message_frame = ctk.CTkFrame(self.chat_messages, fg_color="transparent")
        message_frame.pack(fill="x", pady=5, anchor="e")
        
        # Message bubble
        bubble = ctk.CTkFrame(message_frame, fg_color="#EEF2FF", corner_radius=12)
        bubble.pack(side="right", fill="x", padx=(100, 0))
        
        # Header with icon
        header = ctk.CTkFrame(bubble, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        # Icon
        icon_frame = ctk.CTkFrame(header, width=32, height=32, fg_color="#E0E7FF", corner_radius=16)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text="💡", font=ctk.CTkFont(size=16), text_color="#4F46E5")
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Name
        name_label = ctk.CTkLabel(
            header, 
            text="Initial Idea", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4B5563"
        )
        name_label.pack(side="left", padx=10)
        
        # Message text
        message_label = ctk.CTkLabel(
            bubble, 
            text=text, 
            font=ctk.CTkFont(size=12),
            text_color="#4B5563",
            wraplength=600,
            justify="left"
        )
        message_label.pack(fill="x", padx=10, pady=(0, 10), anchor="w")
        
    def add_chain_response(self):
        # Message container
        message_frame = ctk.CTkFrame(self.chat_messages, fg_color="transparent")
        message_frame.pack(fill="x", pady=5, anchor="w")
        
        # Message bubble
        bubble = ctk.CTkFrame(message_frame, fg_color="white", corner_radius=12)
        bubble.pack(side="left", fill="x", padx=(0, 100))
        
        # Header with icon
        header = ctk.CTkFrame(bubble, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        # Icon
        icon_frame = ctk.CTkFrame(header, width=32, height=32, fg_color="#EEF2FF", corner_radius=16)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text="🤖", font=ctk.CTkFont(size=16), text_color="#4F46E5")
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Name
        name_label = ctk.CTkLabel(
            header, 
            text="Conference Room", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4B5563"
        )
        name_label.pack(side="left", padx=10)
        
        # Message text
        message_label = ctk.CTkLabel(
            bubble, 
            text="Excellent! I'll process this through our 5-stage LLM chain:", 
            font=ctk.CTkFont(size=12),
            text_color="#4B5563",
            wraplength=600,
            justify="left"
        )
        message_label.pack(fill="x", padx=10, pady=(0, 10), anchor="w")
        
        # Chain visualization
        chain_frame = ctk.CTkFrame(bubble, fg_color="transparent")
        chain_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Create chain nodes
        stages = [
            {"number": "1", "name": "Concept Expansion"},
            {"number": "2", "name": "Market Analysis"},
            {"number": "3", "name": "Technical Feasibility"},
            {"number": "4", "name": "Business Model"},
            {"number": "5", "name": "Final Proposal"}
        ]
        
        for i, stage in enumerate(stages):
            node = ctk.CTkFrame(chain_frame, fg_color="#EEF2FF", width=120, height=80, corner_radius=8)
            node.pack(side="left", padx=(0, 20))
            node.pack_propagate(False)
            
            # Number badge
            number_frame = ctk.CTkFrame(node, width=40, height=40, fg_color="#E0E7FF", corner_radius=20)
            number_frame.pack(pady=(10, 5))
            number_frame.pack_propagate(False)
            
            number_label = ctk.CTkLabel(number_frame, text=stage["number"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#4F46E5")
            number_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Stage name
            name_label = ctk.CTkLabel(
                node, 
                text=stage["name"], 
                font=ctk.CTkFont(size=10),
                text_color="#4B5563"
            )
            name_label.pack()
        
        # Progress indicator
        progress_frame = ctk.CTkFrame(bubble, fg_color="#EFF6FF", corner_radius=8, border_width=1, border_color="#DBEAFE")
        progress_frame.pack(fill="x", padx=10, pady=(10, 10))
        
        # Progress header
        progress_header = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_header.pack(fill="x", padx=10, pady=(10, 5))
        
        info_label = ctk.CTkLabel(
            progress_header, 
            text="ℹ️ Processing Stage 1/5", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2563EB"
        )
        info_label.pack(anchor="w")
        
        # Progress description
        progress_desc = ctk.CTkLabel(
            progress_frame, 
            text="Expanding your initial concept with market research and potential applications...", 
            font=ctk.CTkFont(size=12),
            text_color="#1E40AF",
            wraplength=600,
            justify="left"
        )
        progress_desc.pack(fill="x", padx=10, anchor="w")
        
        # Progress bar
        progress_bar_bg = ctk.CTkFrame(progress_frame, fg_color="#DBEAFE", height=6, corner_radius=3)
        progress_bar_bg.pack(fill="x", padx=10, pady=(5, 10))
        
        progress_bar = ctk.CTkFrame(progress_bar_bg, fg_color="#2563EB", width=100, height=6, corner_radius=3)
        progress_bar.place(x=0, y=0)
        
        # Start pulse animation
        self.pulse_animation(progress_bar)
        
    def pulse_animation(self, widget):
        # Simulate pulse animation
        current_opacity = 1.0
        
        def update_opacity():
            nonlocal current_opacity
            current_opacity = 0.5 if current_opacity == 1.0 else 1.0
            widget.configure(fg_color=("#2563EB" if current_opacity == 1.0 else "#93C5FD"))
            self.after(1000, update_opacity)
            
        update_opacity()
        
    def show_chat_view(self):
        # Update button states
        self.chat_btn.configure(fg_color="#EEF2FF", text_color="#4F46E5")
        self.chain_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.history_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.settings_btn.configure(fg_color="transparent", text_color="#6B7280")
        
        # Hide all views
        for widget in self.dynamic_content.winfo_children():
            widget.pack_forget()
        
        # Show chat view
        self.chat_view.pack(fill="both", expand=True)
        
    def show_chain_view(self):
        # Update button states
        self.chat_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.chain_btn.configure(fg_color="#EEF2FF", text_color="#4F46E5")
        self.history_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.settings_btn.configure(fg_color="transparent", text_color="#6B7280")
        
        # Hide all views
        for widget in self.dynamic_content.winfo_children():
            widget.pack_forget()
        
        # Show chain view (not implemented yet)
        self.add_assistant_message("Chain view is not implemented in this demo.")
        self.show_chat_view()
        
    def show_history_view(self):
        # Update button states
        self.chat_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.chain_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.history_btn.configure(fg_color="#EEF2FF", text_color="#4F46E5")
        self.settings_btn.configure(fg_color="transparent", text_color="#6B7280")
        
        # Hide all views
        for widget in self.dynamic_content.winfo_children():
            widget.pack_forget()
        
        # Show history view (not implemented yet)
        self.add_assistant_message("History view is not implemented in this demo.")
        self.show_chat_view()
        
    def show_settings_view(self):
        # Update button states
        self.chat_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.chain_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.history_btn.configure(fg_color="transparent", text_color="#6B7280")
        self.settings_btn.configure(fg_color="#EEF2FF", text_color="#4F46E5")
        
        # Hide all views
        for widget in self.dynamic_content.winfo_children():
            widget.pack_forget()
        
        # Show settings view
        self.settings_view.pack(fill="both", expand=True)
        
    def new_session(self):
        # Clear chat messages
        for widget in self.chat_messages.winfo_children():
            widget.destroy()
        
        # Add welcome message
        self.add_assistant_message("Welcome to Conference Room! I'm your LLM chain automation assistant. Start by entering your idea or question below, and I'll guide it through our optimized LLM processing pipeline.")
        
    def send_message(self):
        # Get message text
        message = self.input_box.get("1.0", "end-1c").strip()
        
        if message:
            # Add user message
            self.add_user_message(message)
            
            # Clear input box
            self.input_box.delete("1.0", "end")
            
            # Simulate response (in a real app, this would call the LLM)
            self.after(1000, lambda: self.add_chain_response())
            
    def on_enter_key(self, event):
        # Send message on Enter key (without shift)
        if not event.state & 0x1:  # Check if shift is not pressed
            self.send_message()
            return "break"  # Prevent default behavior (newline)
        return None  # Allow default behavior (newline) when shift is pressed


class GradientButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Override default colors with gradient
        self.configure(
            fg_color=("#6e8efb", "#6e8efb"),
            hover_color=("#5a7af0", "#5a7af0"),
            text_color="white"
        )


if __name__ == "__main__":
    app = ConferenceRoomApp()
    app.mainloop()
