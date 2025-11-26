import customtkinter as ctk
from config.settings import COLOR_SUCCESS, COLOR_SUCCESS_HOVER
from config.secrets_manager import SecretsManager

class StartView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._create_widgets()

    def _create_widgets(self):
        lbl_hint = ctk.CTkLabel(self, text="Selecione o idioma e inicie a gravação", font=("Roboto", 16), text_color="#ccc")
        lbl_hint.pack(pady=(40, 20))

        self.cmb_language = ctk.CTkComboBox(self, values=["Português", "English", "Español"], 
                                            width=200, height=35, font=("Roboto", 14), state="readonly")
        self.cmb_language.set("Português")
        self.cmb_language.pack(pady=10)

        self.btn_start = ctk.CTkButton(self, text="🔴 Iniciar Gravação", font=("Roboto", 18, "bold"),
                                  fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER, width=250, height=60, corner_radius=30,
                                  command=self._on_start)
        self.btn_start.pack(pady=30)
        
        self.check_api_key()

    def check_api_key(self):
        if not SecretsManager.get_api_key():
            self.btn_start.configure(state="disabled", fg_color="#555", text="⚠️ Configure API Key")
        else:
            self.btn_start.configure(state="normal", fg_color=COLOR_SUCCESS, text="🔴 Iniciar Gravação")

    def _on_start(self):
        language = self.cmb_language.get()
        self.controller.start_recording(language)
