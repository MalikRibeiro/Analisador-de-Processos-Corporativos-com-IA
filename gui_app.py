import customtkinter as ctk
import threading
import sys
import os
import time
import webbrowser
from datetime import datetime
from tkinter import messagebox

# Ensure the app module is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.screen_recorder import ScreenRecorder
from app.action_logger import ActionLogger
from app.process_miner import ProcessMiner
from app.process_analyst_agent import ProcessAnalystAgent
from app.automation_advisor import AutomationAdvisor

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CorporateProcessAnalyzerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analisador de Processos Corporativos com IA")
        self.geometry("800x600")
        self.resizable(False, False)

        # Create output directories
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # State variables
        self.is_recording = False
        self.start_time = None
        self.current_video_path = None
        self.last_report_path = None
        self.logs_visible = False

        # Initialize Modules
        self.recorder = None 
        self.logger = ActionLogger()
        self.miner = ProcessMiner()
        self.analyst = None
        self.advisor = AutomationAdvisor(output_dir=self.reports_dir)

        # UI Layout
        self.create_layout()
        
        # Initialize AI Agent in background
        threading.Thread(target=self.init_ai_agent, daemon=True).start()

    def create_layout(self):
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Main content area expands

        # --- 1. Header (Title + Settings) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Analisador de Processos Corporativos com IA", font=("Roboto", 20, "bold"))
        self.lbl_title.grid(row=0, column=0, sticky="w")

        self.btn_settings = ctk.CTkButton(self.header_frame, text="⚙️", width=40, height=40, 
                                          fg_color="transparent", hover_color="#444", 
                                          font=("Arial", 20), command=self.open_settings)
        self.btn_settings.grid(row=0, column=1, sticky="e")

        # --- 2. Stepper (Indicators) ---
        self.stepper_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stepper_frame.grid(row=1, column=0, pady=10)

        self.step_1 = self.create_step_indicator(self.stepper_frame, "1", "Gravação", active=True)
        self.step_1.grid(row=0, column=0, padx=15)
        
        self.step_2 = self.create_step_indicator(self.stepper_frame, "2", "Análise IA", active=False)
        self.step_2.grid(row=0, column=1, padx=15)
        
        self.step_3 = self.create_step_indicator(self.stepper_frame, "3", "Resultados", active=False)
        self.step_3.grid(row=0, column=2, padx=15)

        # --- 3. Main Content Area (Dynamic Stages) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Create the different stage frames (only one visible at a time)
        self.stage_start = self.create_stage_start()
        self.stage_recording = self.create_stage_recording()
        self.stage_analyzing = self.create_stage_analyzing()
        self.stage_results = self.create_stage_results()

        # --- 4. Footer (Status + Logs) ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", height=40, corner_radius=0)
        self.footer_frame.grid(row=3, column=0, sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(self.footer_frame, text="Status: Pronto", font=("Roboto", 12), text_color="#aaa")
        self.lbl_status.grid(row=0, column=0, sticky="w", padx=20, pady=5)

        self.btn_toggle_logs = ctk.CTkButton(self.footer_frame, text="Show Logs", width=80, height=25,
                                             fg_color="#333", hover_color="#444", font=("Roboto", 10),
                                             command=self.toggle_logs)
        self.btn_toggle_logs.grid(row=0, column=1, sticky="e", padx=20, pady=5)

        # Show initial stage (Must be called after footer is created)
        self.show_stage("start")

        # Hidden Log Window (Toplevel)
        self.log_window = None

    def create_step_indicator(self, parent, number, text, active=False):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        color = "#3498db" if active else "#555"
        text_color = "#fff" if active else "#888"
        
        lbl_circle = ctk.CTkLabel(frame, text=number, width=30, height=30, corner_radius=15,
                                  fg_color=color, text_color="white", font=("Roboto", 14, "bold"))
        lbl_circle.pack(side="left")
        
        lbl_text = ctk.CTkLabel(frame, text=text, font=("Roboto", 14, "bold" if active else "normal"), 
                                text_color=text_color)
        lbl_text.pack(side="left", padx=(10, 0))
        
        return frame

    def update_stepper(self, step):
        # Helper to update colors of the stepper
        def set_style(widget_frame, active):
            color = "#3498db" if active else "#555"
            text_color = "#fff" if active else "#888"
            font_weight = "bold" if active else "normal"
            
            # Access children: [Label(Circle), Label(Text)]
            children = widget_frame.winfo_children()
            children[0].configure(fg_color=color)
            children[1].configure(text_color=text_color, font=("Roboto", 14, font_weight))

        set_style(self.step_1, step == 1)
        set_style(self.step_2, step == 2)
        set_style(self.step_3, step == 3)

    # --- Stage Creation Helpers ---

    def create_stage_start(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        lbl_hint = ctk.CTkLabel(frame, text="Selecione o idioma e inicie a gravação", font=("Roboto", 16), text_color="#ccc")
        lbl_hint.pack(pady=(40, 20))

        self.cmb_language = ctk.CTkComboBox(frame, values=["Português", "English", "Español"], 
                                            width=200, height=35, font=("Roboto", 14), state="readonly")
        self.cmb_language.set("Português")
        self.cmb_language.pack(pady=10)

        btn_start = ctk.CTkButton(frame, text="🔴 Iniciar Gravação", font=("Roboto", 18, "bold"),
                                  fg_color="#2ecc71", hover_color="#27ae60", width=250, height=60, corner_radius=30,
                                  command=self.start_recording)
        btn_start.pack(pady=30)
        
        return frame

    def create_stage_recording(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        lbl_rec = ctk.CTkLabel(frame, text="GRAVANDO...", font=("Roboto", 16, "bold"), text_color="#e74c3c")
        lbl_rec.pack(pady=(40, 10))

        self.lbl_timer_big = ctk.CTkLabel(frame, text="00:00:00", font=("Consolas", 60, "bold"), text_color="#fff")
        self.lbl_timer_big.pack(pady=20)

        lbl_info = ctk.CTkLabel(frame, text="Minimize esta janela e realize o processo.", font=("Roboto", 14), text_color="#aaa")
        lbl_info.pack(pady=10)

        btn_stop = ctk.CTkButton(frame, text="⏹ Parar e Analisar", font=("Roboto", 18, "bold"),
                                 fg_color="#e74c3c", hover_color="#c0392b", width=250, height=60, corner_radius=30,
                                 command=self.stop_and_analyze)
        btn_stop.pack(pady=30)
        
        return frame

    def create_stage_analyzing(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        lbl_title = ctk.CTkLabel(frame, text="Analisando Processo", font=("Roboto", 20, "bold"))
        lbl_title.pack(pady=(50, 20))

        self.progress_bar = ctk.CTkProgressBar(frame, width=400, height=20, mode="indeterminate")
        self.progress_bar.pack(pady=20)
        self.progress_bar.start()

        lbl_desc = ctk.CTkLabel(frame, text="A IA está assistindo ao vídeo e identificando gargalos...\nIsso pode levar alguns minutos.", 
                                font=("Roboto", 14), text_color="#aaa")
        lbl_desc.pack(pady=10)
        
        return frame

    def create_stage_results(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        lbl_icon = ctk.CTkLabel(frame, text="✅", font=("Arial", 80))
        lbl_icon.pack(pady=(30, 10))

        lbl_success = ctk.CTkLabel(frame, text="Análise Concluída!", font=("Roboto", 24, "bold"), text_color="#2ecc71")
        lbl_success.pack(pady=10)

        btn_view = ctk.CTkButton(frame, text="✨ Visualizar Relatório", font=("Roboto", 18, "bold"),
                                 fg_color="#9b59b6", hover_color="#8e44ad", width=280, height=60, corner_radius=30,
                                 command=self.open_report_browser)
        btn_view.pack(pady=30)

        btn_back = ctk.CTkButton(frame, text="Voltar ao Início", font=("Roboto", 14),
                                 fg_color="transparent", border_width=1, border_color="#555", hover_color="#333",
                                 command=self.reset_to_start)
        btn_back.pack(pady=10)
        
        return frame

    def show_stage(self, stage_name):
        # Hide all stages
        self.stage_start.pack_forget()
        self.stage_recording.pack_forget()
        self.stage_analyzing.pack_forget()
        self.stage_results.pack_forget()

        # Show requested stage and update stepper
        if stage_name == "start":
            self.stage_start.pack(expand=True, fill="both")
            self.update_stepper(1)
            self.update_status("Pronto para gravar.")
        elif stage_name == "recording":
            self.stage_recording.pack(expand=True, fill="both")
            self.update_stepper(1)
            self.update_status("Gravando...")
        elif stage_name == "analyzing":
            self.stage_analyzing.pack(expand=True, fill="both")
            self.update_stepper(2)
            self.update_status("Processando vídeo...")
        elif stage_name == "results":
            self.stage_results.pack(expand=True, fill="both")
            self.update_stepper(3)
            self.update_status("Relatório gerado com sucesso.")

    # --- Logic & Actions ---

    def init_ai_agent(self):
        try:
            self.safe_log("Inicializando agente de IA...")
            self.analyst = ProcessAnalystAgent()
            self.safe_log("Agente de IA pronto.")
        except Exception as e:
            self.safe_log(f"Erro ao inicializar IA: {e}")
            self.update_status("Erro na API Key")

    def open_settings(self):
        api_key = ctk.CTkInputDialog(text="Insira sua Google API Key:", title="Configurações").get_input()
        if api_key:
            env_path = os.path.join(os.getcwd(), ".env")
            with open(env_path, "w") as f:
                f.write(f"GOOGLE_API_KEY={api_key}\n")
            self.safe_log("API Key salva. Reinicializando...")
            threading.Thread(target=self.init_ai_agent, daemon=True).start()

    def update_timer(self):
        if self.is_recording and self.start_time:
            elapsed = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.lbl_timer_big.configure(text=time_str)
            self.after(1000, self.update_timer)

    def start_recording(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.mp4"
        self.current_video_path = os.path.join(self.data_dir, filename)
        
        self.recorder = ScreenRecorder(output_file=self.current_video_path)
        
        self.is_recording = True
        self.start_time = time.time()
        self.show_stage("recording")
        self.update_timer()
        
        self.recorder.start_recording()
        self.logger.start_logging()
        self.miner.start_monitoring()
        
        self.safe_log(f"Gravação iniciada: {filename}")

    def stop_and_analyze(self):
        self.is_recording = False
        self.show_stage("analyzing")
        
        self.safe_log("Parando gravação...")
        self.recorder.stop_recording()
        self.action_logs = self.logger.stop_logging()
        self.window_logs = self.miner.stop_monitoring()
        
        self.safe_log(f"Vídeo salvo. Iniciando análise...")
        
        self.current_language = self.cmb_language.get()
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        if not self.analyst:
            self.safe_log("ERRO: Agente não inicializado.")
            self.after(0, lambda: messagebox.showerror("Erro", "Configure a API Key antes de continuar."))
            self.after(0, lambda: self.show_stage("start"))
            return

        try:
            all_logs = sorted(self.action_logs + self.window_logs)
            
            analysis_result = self.analyst.analyze_process(
                video_path=self.current_video_path,
                logs=all_logs,
                language=self.current_language
            )
            
            self.safe_log("Gerando HTML...")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_name = f"Relatorio_Processo_{timestamp}.html"
            self.last_report_path = self.advisor.generate_report(analysis_result, report_filename=report_name)
            
            self.safe_log(f"Relatório pronto: {report_name}")
            self.after(0, lambda: self.show_stage("results"))
            
        except Exception as e:
            self.safe_log(f"ERRO: {e}")
            self.after(0, lambda: messagebox.showerror("Erro na Análise", str(e)))
            self.after(0, lambda: self.show_stage("start"))

    def open_report_browser(self):
        if self.last_report_path and os.path.exists(self.last_report_path):
            webbrowser.open(f"file://{self.last_report_path}")

    def reset_to_start(self):
        self.show_stage("start")

    # --- Logging & Status ---

    def update_status(self, text):
        self.lbl_status.configure(text=f"Status: {text}")

    def safe_log(self, message):
        self.after(0, lambda: self._append_log(message))

    def _append_log(self, message):
        timestamp = time.strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        
        # If log window is open, update it
        if self.log_window and self.log_window.winfo_exists():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", log_msg + "\n")
            self.log_textbox.see("end")
            self.log_textbox.configure(state="disabled")
        
        # Also print to console for debugging
        print(log_msg)

    def toggle_logs(self):
        if self.log_window is None or not self.log_window.winfo_exists():
            self.log_window = ctk.CTkToplevel(self)
            self.log_window.title("Logs Detalhados")
            self.log_window.geometry("500x400")
            
            self.log_textbox = ctk.CTkTextbox(self.log_window, font=("Consolas", 12))
            self.log_textbox.pack(expand=True, fill="both", padx=10, pady=10)
            self.log_textbox.configure(state="disabled")
        else:
            self.log_window.focus()

if __name__ == "__main__":
    app = CorporateProcessAnalyzerGUI()
    app.mainloop()
