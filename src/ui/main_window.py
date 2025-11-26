import customtkinter as ctk
from config.settings import (
    THEME_MODE, COLOR_THEME, WINDOW_TITLE, WINDOW_SIZE, WINDOW_RESIZABLE,
    COLOR_BG_MAIN, COLOR_BG_FOOTER, FONT_HEADER_M, FONT_BODY_S
)
from src.controllers.main_controller import MainController
from src.ui.components.stepper import Stepper
from src.ui.views.start_view import StartView
from src.ui.views.recording_view import RecordingView
from src.ui.views.analyzing_view import AnalyzingView
from src.ui.views.result_view import ResultView

ctk.set_appearance_mode(THEME_MODE)
ctk.set_default_color_theme(COLOR_THEME)

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)

        self.controller = MainController()
        
        # UI Layout
        self._create_layout()
        
        # Subscribe to controller events
        self.controller.set_callbacks(
            on_status_change=self.update_status,
            on_timer_update=self.update_timer,
            on_log_message=self.append_log,
            on_stage_change=self.show_stage,
            on_error=self.show_error
        )
        
        # Initial State
        self.show_stage("start")

    def _create_layout(self):
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Main content area expands

        # --- 1. Header (Title + Settings) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(self.header_frame, text=WINDOW_TITLE, font=FONT_HEADER_M)
        self.lbl_title.grid(row=0, column=0, sticky="w")

        self.btn_settings = ctk.CTkButton(self.header_frame, text="⚙️", width=40, height=40, 
                                          fg_color="transparent", hover_color="#444", 
                                          font=("Arial", 20), command=self.open_settings)
        self.btn_settings.grid(row=0, column=1, sticky="e")

        # --- 2. Stepper (Indicators) ---
        self.stepper_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stepper_frame.grid(row=1, column=0, pady=10)
        
        self.stepper = Stepper(self.stepper_frame, ["Gravação", "Análise IA", "Resultados"])
        self.stepper.pack()

        # --- 3. Main Content Area (Dynamic Stages) ---
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BG_MAIN, corner_radius=15)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Views
        self.view_start = StartView(self.main_frame, self.controller)
        self.view_recording = RecordingView(self.main_frame, self.controller)
        self.view_analyzing = AnalyzingView(self.main_frame, self.controller)
        self.view_result = ResultView(self.main_frame, self.controller)

        # --- 4. Footer (Status + Logs) ---
        self.footer_frame = ctk.CTkFrame(self, fg_color=COLOR_BG_FOOTER, height=40, corner_radius=0)
        self.footer_frame.grid(row=3, column=0, sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(self.footer_frame, text="Status: Pronto", font=FONT_BODY_S, text_color="#aaa")
        self.lbl_status.grid(row=0, column=0, sticky="w", padx=20, pady=5)

        self.btn_toggle_logs = ctk.CTkButton(self.footer_frame, text="Show Logs", width=80, height=25,
                                             fg_color="#333", hover_color="#444", font=("Roboto", 10),
                                             command=self.toggle_logs)
        self.btn_toggle_logs.grid(row=0, column=1, sticky="e", padx=20, pady=5)

        # Log Window
        self.log_window = None

    def show_stage(self, stage_name):
        # Hide all
        self.view_start.pack_forget()
        self.view_recording.pack_forget()
        self.view_analyzing.pack_forget()
        self.view_result.pack_forget()
        
        # Stop tips if leaving analyzing
        if stage_name != "analyzing":
            self.view_analyzing.stop_tips()

        if stage_name == "start":
            self.view_start.pack(expand=True, fill="both")
            self.stepper.update_step(0)
            self.view_start.check_api_key() # Re-check in case it was just set
        elif stage_name == "recording":
            self.view_recording.pack(expand=True, fill="both")
            self.stepper.update_step(0)
        elif stage_name == "analyzing":
            self.view_analyzing.pack(expand=True, fill="both")
            self.stepper.update_step(1)
            self.view_analyzing.start_tips()
        elif stage_name == "results":
            self.view_result.pack(expand=True, fill="both")
            self.stepper.update_step(2)

    def update_status(self, message):
        self.lbl_status.configure(text=f"Status: {message}")

    def update_timer(self, time_str):
        self.view_recording.update_timer(time_str)

    def append_log(self, message):
        if self.log_window and self.log_window.winfo_exists():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", message + "\n")
            self.log_textbox.see("end")
            self.log_textbox.configure(state="disabled")

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

    def open_settings(self):
        api_key = ctk.CTkInputDialog(text="Insira sua Google API Key:", title="Configurações").get_input()
        if api_key:
            self.controller.save_api_key(api_key)
            self.view_start.check_api_key()

    def show_error(self, message):
        from tkinter import messagebox
        messagebox.showerror("Erro", message)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
