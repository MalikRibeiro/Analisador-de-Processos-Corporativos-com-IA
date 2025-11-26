import customtkinter as ctk
from config.settings import COLOR_DANGER, COLOR_DANGER_HOVER, FONT_TIMER

class RecordingView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._create_widgets()

    def _create_widgets(self):
        lbl_rec = ctk.CTkLabel(self, text="GRAVANDO...", font=("Roboto", 16, "bold"), text_color=COLOR_DANGER)
        lbl_rec.pack(pady=(40, 10))

        self.lbl_timer = ctk.CTkLabel(self, text="00:00:00", font=FONT_TIMER, text_color="#fff")
        self.lbl_timer.pack(pady=20)

        lbl_info = ctk.CTkLabel(self, text="Minimize esta janela e realize o processo.", font=("Roboto", 14), text_color="#aaa")
        lbl_info.pack(pady=10)

        btn_stop = ctk.CTkButton(self, text="⏹ Parar e Analisar", font=("Roboto", 18, "bold"),
                                 fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, width=250, height=60, corner_radius=30,
                                 command=self.controller.stop_and_analyze)
        btn_stop.pack(pady=30)

    def update_timer(self, time_str):
        self.lbl_timer.configure(text=time_str)
