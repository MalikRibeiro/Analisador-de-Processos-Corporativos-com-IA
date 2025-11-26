import threading
import time
import os
from datetime import datetime
from config.settings import DATA_DIR, REPORTS_DIR
from config.secrets_manager import SecretsManager
from src.services.recorder_service import RecorderService
from src.services.logger_service import LoggerService
from src.services.miner_service import MinerService
from src.services.ai_service import AIService
from src.services.report_service import ReportService

class MainController:
    def __init__(self):
        # Services
        self.recorder = None
        self.logger = LoggerService()
        self.miner = MinerService()
        self.ai_service = None
        self.report_service = ReportService(output_dir=REPORTS_DIR)

        # State
        self.is_recording = False
        self.start_time = None
        self.current_video_path = None
        self.last_report_path = None
        self.logs_visible = False
        self.current_language = "Português"

        # Callbacks (UI updates)
        self.on_status_change = None
        self.on_timer_update = None
        self.on_log_message = None
        self.on_stage_change = None
        self.on_error = None

        # Initialize AI in background
        threading.Thread(target=self._init_ai_service, daemon=True).start()

    def _init_ai_service(self):
        try:
            self.log("Inicializando serviço de IA...")
            self.ai_service = AIService()
            if self.ai_service.model:
                self.log("Serviço de IA pronto.")
            else:
                self.log("Serviço de IA aguardando API Key.")
        except Exception as e:
            self.log(f"Erro ao inicializar IA: {e}")
            if self.on_error:
                self.on_error("Erro na inicialização da IA")

    def set_callbacks(self, on_status_change=None, on_timer_update=None, on_log_message=None, on_stage_change=None, on_error=None):
        self.on_status_change = on_status_change
        self.on_timer_update = on_timer_update
        self.on_log_message = on_log_message
        self.on_stage_change = on_stage_change
        self.on_error = on_error

    def log(self, message):
        timestamp = time.strftime('%H:%M:%S')
        full_msg = f"[{timestamp}] {message}"
        print(full_msg)
        if self.on_log_message:
            self.on_log_message(full_msg)

    def update_status(self, message):
        if self.on_status_change:
            self.on_status_change(message)

    def save_api_key(self, api_key):
        SecretsManager.save_api_key(api_key)
        self.log("API Key salva. Reinicializando IA...")
        threading.Thread(target=self._init_ai_service, daemon=True).start()

    def start_recording(self, language):
        self.current_language = language
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.mp4"
        self.current_video_path = os.path.join(DATA_DIR, filename)
        
        self.recorder = RecorderService(output_file=self.current_video_path)
        
        self.is_recording = True
        self.start_time = time.time()
        
        self.recorder.start_recording()
        self.logger.start_logging()
        self.miner.start_monitoring()
        
        self.log(f"Gravação iniciada: {filename}")
        if self.on_stage_change:
            self.on_stage_change("recording")
        
        self.update_status("Gravando...")
        self._start_timer_thread()

    def _start_timer_thread(self):
        def _timer_loop():
            while self.is_recording:
                elapsed = int(time.time() - self.start_time)
                hours, remainder = divmod(elapsed, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                if self.on_timer_update:
                    self.on_timer_update(time_str)
                time.sleep(1)
        threading.Thread(target=_timer_loop, daemon=True).start()

    def stop_and_analyze(self):
        self.is_recording = False
        if self.on_stage_change:
            self.on_stage_change("analyzing")
        
        self.log("Parando gravação...")
        self.recorder.stop_recording()
        action_logs = self.logger.stop_logging()
        window_logs = self.miner.stop_monitoring()
        
        self.log("Vídeo salvo. Iniciando análise...")
        self.update_status("Processando vídeo...")
        
        threading.Thread(target=self._run_analysis, args=(action_logs, window_logs), daemon=True).start()

    def _run_analysis(self, action_logs, window_logs):
        if not self.ai_service or not self.ai_service.model:
            self.log("ERRO: Agente de IA não inicializado ou sem API Key.")
            if self.on_error:
                self.on_error("Configure a API Key antes de continuar.")
            if self.on_stage_change:
                self.on_stage_change("start")
            return

        try:
            all_logs = sorted(action_logs + window_logs)
            
            analysis_result = self.ai_service.analyze_process(
                video_path=self.current_video_path,
                logs=all_logs,
                language=self.current_language
            )
            
            self.log("Gerando HTML...")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_name = f"Relatorio_Processo_{timestamp}.html"
            self.last_report_path = self.report_service.generate_report(analysis_result, report_filename=report_name)
            
            self.log(f"Relatório pronto: {report_name}")
            self.update_status("Relatório gerado com sucesso.")
            if self.on_stage_change:
                self.on_stage_change("results")
            
        except Exception as e:
            self.log(f"ERRO na análise: {e}")
            if self.on_error:
                self.on_error(str(e))
            if self.on_stage_change:
                self.on_stage_change("start")

    def reset(self):
        self.is_recording = False
        self.current_video_path = None
        self.last_report_path = None
        if self.on_stage_change:
            self.on_stage_change("start")
        self.update_status("Pronto para gravar.")

    def get_last_report_path(self):
        return self.last_report_path
