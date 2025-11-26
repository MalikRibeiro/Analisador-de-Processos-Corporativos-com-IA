import customtkinter as ctk
import webbrowser
import os
from config.settings import COLOR_INFO, COLOR_INFO_HOVER, COLOR_SUCCESS

class ResultView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._create_widgets()

    def _create_widgets(self):
        lbl_icon = ctk.CTkLabel(self, text="✅", font=("Arial", 80))
        lbl_icon.pack(pady=(30, 10))

        lbl_success = ctk.CTkLabel(self, text="Análise Concluída!", font=("Roboto", 24, "bold"), text_color=COLOR_SUCCESS)
        lbl_success.pack(pady=10)

        btn_view = ctk.CTkButton(self, text="✨ Visualizar Relatório", font=("Roboto", 18, "bold"),
                                 fg_color=COLOR_INFO, hover_color=COLOR_INFO_HOVER, width=280, height=60, corner_radius=30,
                                 command=self._open_report)
        btn_view.pack(pady=30)

        btn_back = ctk.CTkButton(self, text="Voltar ao Início", font=("Roboto", 14),
                                 fg_color="transparent", border_width=1, border_color="#555", hover_color="#333",
                                 command=self.controller.reset)
        btn_back.pack(pady=10)

    def _open_report(self):
        path = self.controller.get_last_report_path()
        if path and os.path.exists(path):
            webbrowser.open(f"file://{path}")
