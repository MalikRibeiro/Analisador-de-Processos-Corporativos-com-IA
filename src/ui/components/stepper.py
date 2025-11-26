import customtkinter as ctk
from config.settings import COLOR_PRIMARY, COLOR_TEXT_WHITE

class Stepper(ctk.CTkFrame):
    def __init__(self, master, steps):
        super().__init__(master, fg_color="transparent")
        self.steps = steps
        self.indicators = []
        self._create_widgets()

    def _create_widgets(self):
        for i, step_name in enumerate(self.steps):
            step_num = str(i + 1)
            
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(side="left", padx=15)
            
            lbl_circle = ctk.CTkLabel(frame, text=step_num, width=30, height=30, corner_radius=15,
                                      fg_color="#555", text_color="white", font=("Roboto", 14, "bold"))
            lbl_circle.pack(side="left")
            
            lbl_text = ctk.CTkLabel(frame, text=step_name, font=("Roboto", 14), text_color="#888")
            lbl_text.pack(side="left", padx=(10, 0))
            
            self.indicators.append((lbl_circle, lbl_text))

    def update_step(self, current_step_index):
        for i, (lbl_circle, lbl_text) in enumerate(self.indicators):
            active = (i == current_step_index)
            
            color = COLOR_PRIMARY if active else "#555"
            text_color = COLOR_TEXT_WHITE if active else "#888"
            font_weight = "bold" if active else "normal"
            
            lbl_circle.configure(fg_color=color)
            lbl_text.configure(text_color=text_color, font=("Roboto", 14, font_weight))
