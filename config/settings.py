import os
import customtkinter as ctk

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# --- Appearance ---
THEME_MODE = "Dark"
COLOR_THEME = "blue"

# --- Colors ---
COLOR_PRIMARY = "#3498db"
COLOR_SUCCESS = "#2ecc71"
COLOR_SUCCESS_HOVER = "#27ae60"
COLOR_DANGER = "#e74c3c"
COLOR_DANGER_HOVER = "#c0392b"
COLOR_WARNING = "#f39c12"
COLOR_INFO = "#9b59b6"
COLOR_INFO_HOVER = "#8e44ad"

COLOR_BG_MAIN = "#2b2b2b"
COLOR_BG_FOOTER = "#1a1a1a"
COLOR_TEXT_WHITE = "#ffffff"
COLOR_TEXT_GRAY = "#aaaaaa"
COLOR_TEXT_LIGHT_GRAY = "#cccccc"

# --- Fonts ---
FONT_FAMILY = "Roboto"
FONT_HEADER_L = (FONT_FAMILY, 24, "bold")
FONT_HEADER_M = (FONT_FAMILY, 20, "bold")
FONT_HEADER_S = (FONT_FAMILY, 18, "bold")
FONT_BODY_L = (FONT_FAMILY, 16)
FONT_BODY_M = (FONT_FAMILY, 14)
FONT_BODY_S = (FONT_FAMILY, 12)
FONT_MONO = ("Consolas", 12)
FONT_TIMER = ("Consolas", 60, "bold")

# --- UI Constants ---
WINDOW_TITLE = "Analisador de Processos Corporativos com IA"
WINDOW_SIZE = "800x600"
WINDOW_RESIZABLE = False
