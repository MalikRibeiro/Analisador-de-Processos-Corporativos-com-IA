import customtkinter as ctk
import threading
import sys
import os
import time
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

        self.title("Corporate Process Analyzer")
        self.geometry("700x600")

        # Create output directories
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        self.video_path = os.path.join(self.data_dir, "process_recording.mp4")
        self.report_path = os.path.join(self.reports_dir, "relatorio_processo.md")

        # Initialize Modules
        self.recorder = ScreenRecorder(output_file=self.video_path)
        self.logger = ActionLogger()
        self.miner = ProcessMiner()
        self.analyst = None
        self.advisor = AutomationAdvisor(output_dir=self.reports_dir)

        # UI Elements
        self.create_widgets()
        
        # Initialize AI Agent in background
        threading.Thread(target=self.init_ai_agent, daemon=True).start()

    def create_widgets(self):
        # Grid Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Log area expands

        # Header
        self.header_label = ctk.CTkLabel(self, text="Corporate Process Analyzer AI", font=("Roboto", 24, "bold"))
        self.header_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")

        # Settings Frame (Language)
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.grid(row=1, column=0, pady=(0, 10))

        self.lbl_lang = ctk.CTkLabel(self.settings_frame, text="Idioma do Relatório:", font=("Roboto", 12))
        self.lbl_lang.grid(row=0, column=0, padx=5)

        self.cmb_language = ctk.CTkComboBox(self.settings_frame, values=["Português", "English", "Español"], state="readonly")
        self.cmb_language.set("Português")
        self.cmb_language.grid(row=0, column=1, padx=5)

        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, pady=10)

        self.btn_record = ctk.CTkButton(self.btn_frame, text="Iniciar Gravação", font=("Roboto", 14, "bold"), 
                                        fg_color="#2ecc71", hover_color="#27ae60", width=200, height=40,
                                        command=self.start_recording)
        self.btn_record.grid(row=0, column=0, padx=10)

        self.btn_stop = ctk.CTkButton(self.btn_frame, text="Parar e Analisar", font=("Roboto", 14, "bold"), 
                                      fg_color="#e74c3c", hover_color="#c0392b", width=200, height=40,
                                      command=self.stop_and_analyze, state="disabled")
        self.btn_stop.grid(row=0, column=1, padx=10)

        # Progress Bar (Initially hidden or stopped)
        self.progress_bar = ctk.CTkProgressBar(self, width=400, mode="indeterminate")
        self.progress_bar.grid(row=3, column=0, pady=(10, 0))
        self.progress_bar.set(0)
        self.progress_bar.grid_remove() # Hide initially

        # Log Area
        self.log_label = ctk.CTkLabel(self, text="Log de Atividades:", font=("Roboto", 12))
        self.log_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 0))

        self.log_area = ctk.CTkTextbox(self, width=660, height=200, font=("Consolas", 12))
        self.log_area.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.log_area.configure(state="disabled")

        # Footer Button
        self.btn_open_reports = ctk.CTkButton(self, text="Abrir Pasta de Relatórios", font=("Roboto", 12), 
                                              fg_color="#3498db", hover_color="#2980b9",
                                              command=self.open_reports_folder)
        self.btn_open_reports.grid(row=6, column=0, pady=20)

    # --- Thread-Safe UI Updates ---
    def safe_log(self, message):
        """Updates the log area from the main thread."""
        self.after(0, lambda: self._update_log(message))

    def _update_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def safe_toggle_buttons(self, recording=False, analyzing=False):
        """Updates button states from the main thread."""
        self.after(0, lambda: self._update_buttons(recording, analyzing))

    def _update_buttons(self, recording, analyzing):
        if recording:
            self.btn_record.configure(state="disabled")
            self.btn_stop.configure(state="normal")
        elif analyzing:
            self.btn_record.configure(state="disabled")
            self.btn_stop.configure(state="disabled")
            self.progress_bar.grid() # Show progress bar
            self.progress_bar.start()
        else: # Reset / Idle
            self.btn_record.configure(state="normal")
            self.btn_stop.configure(state="disabled")
            self.progress_bar.stop()
            self.progress_bar.grid_remove() # Hide progress bar

    # --- Logic ---

    def init_ai_agent(self):
        try:
            self.safe_log("Inicializando agente de IA...")
            self.analyst = ProcessAnalystAgent()
            self.safe_log("Agente de IA pronto.")
        except Exception as e:
            self.safe_log(f"Erro ao inicializar IA: {e}")

    def start_recording(self):
        self.safe_toggle_buttons(recording=True)
        
        self.recorder.start_recording()
        self.logger.start_logging()
        self.miner.start_monitoring()
        
        self.safe_log("Gravação INICIADA.")
        self.safe_log("Minimize esta janela e realize o processo.")
        self.safe_log("Uma janela de preview da gravação deve aparecer.")

    def stop_and_analyze(self):
        self.safe_toggle_buttons(analyzing=True)
        
        self.safe_log("Parando gravação...")
        self.recorder.stop_recording()
        self.action_logs = self.logger.stop_logging()
        self.window_logs = self.miner.stop_monitoring()
        
        self.safe_log(f"Gravação parada. Capturados {len(self.action_logs)} eventos de ação.")
        
        # Capture language selection from UI before starting thread
        self.current_language = self.cmb_language.get()
        self.safe_log(f"Idioma selecionado para análise: {self.current_language}")

        # Start analysis in a separate thread
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        if not self.analyst:
            self.safe_log("ERRO: Agente de IA não foi inicializado corretamente.")
            self.safe_toggle_buttons(recording=False, analyzing=False)
            return

        self.safe_log("Enviando vídeo para o Gemini (isso pode demorar)...")
        
        try:
            all_logs = sorted(self.action_logs + self.window_logs)
            
            # Get selected language from GUI (must be accessed in main thread or via variable if thread-safe)
            # Since we are in a thread, accessing self.cmb_language.get() might be unsafe in some toolkits,
            # but usually reading values is fine. To be 100% safe, we should have passed it as an arg.
            # However, let's try reading it. If it fails, we default.
            try:
                # We need to schedule this on main thread to be safe
                # But for simplicity in this quick refactor, we can pass it when starting the thread.
                # Let's fix this by getting the value BEFORE starting the thread.
                pass 
            except:
                pass

            # Actually, let's just use the value passed to this function.
            # I will update the start_thread call to pass the language.
            pass
            
            # Wait, I can't easily change the signature in the middle of this replace block without changing the caller.
            # Let's assume reading is okay or use a safer way.
            # Better approach: The caller `stop_and_analyze` should capture the value.
            
            # Let's use a class attribute set by stop_and_analyze
            selected_language = getattr(self, 'current_language', "Português")

            analysis_result = self.analyst.analyze_process(
                video_path=self.video_path,
                logs=all_logs,
                language=selected_language
            )
            
            self.safe_log("Análise recebida. Gerando relatório...")
            self.advisor.generate_report(analysis_result, report_filename="relatorio_processo.md")
            
            self.safe_log(f"Análise concluída! Arquivo salvo em: {self.report_path}")
            # Optional: Show a popup (must be done in main thread if using tkinter messagebox, 
            # but customtkinter doesn't have a native message box yet, usually falls back to tkinter's)
            self.after(0, lambda: messagebox.showinfo("Sucesso", "Análise concluída com sucesso!"))
            
        except Exception as e:
            self.safe_log(f"ERRO durante a análise: {e}")
            # Ensure the error is shown and UI is reset
            self.after(0, lambda: messagebox.showerror("Erro de Análise", f"Ocorreu um erro durante a análise:\n{str(e)}"))
        
        finally:
            # Always reset buttons to allow retrying
            self.safe_toggle_buttons(recording=False, analyzing=False)
            self.safe_log("Pronto para nova gravação.")

    def open_reports_folder(self):
        try:
            os.startfile(self.reports_dir)
        except Exception as e:
            self.safe_log(f"Erro ao abrir pasta: {e}")

if __name__ == "__main__":
    app = CorporateProcessAnalyzerGUI()
    app.mainloop()
