import customtkinter as ctk
import threading
import time

class AnalyzingView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._create_widgets()
        self.tips = [
            "Lendo logs de teclado...",
            "Processando vídeo...",
            "Identificando janelas ativas...",
            "Gerando fluxograma...",
            "Buscando gargalos...",
            "Escrevendo relatório..."
        ]
        self.running_tips = False

    def _create_widgets(self):
        lbl_title = ctk.CTkLabel(self, text="Analisando Processo", font=("Roboto", 20, "bold"))
        lbl_title.pack(pady=(50, 20))

        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=20, mode="indeterminate")
        self.progress_bar.pack(pady=20)
        self.progress_bar.start()

        self.lbl_desc = ctk.CTkLabel(self, text="A IA está assistindo ao vídeo...", font=("Roboto", 14), text_color="#aaa")
        self.lbl_desc.pack(pady=10)

    def start_tips(self):
        self.running_tips = True
        threading.Thread(target=self._rotate_tips, daemon=True).start()

    def stop_tips(self):
        self.running_tips = False

    def _rotate_tips(self):
        idx = 0
        while self.running_tips:
            if self.winfo_exists():
                self.lbl_desc.configure(text=self.tips[idx % len(self.tips)])
                idx += 1
            time.sleep(3)
