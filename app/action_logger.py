from pynput import mouse, keyboard
import time
import threading
from datetime import datetime

class ActionLogger:
    """
    Logs user input events (mouse clicks and keyboard activity) without recording specific keystrokes.
    """

    def __init__(self):
        self.logs = []
        self.logging = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.start_time = None

    def start_logging(self):
        """Starts logging mouse and keyboard events."""
        if not self.logging:
            self.logging = True
            self.logs = []
            self.start_time = time.time()
            
            # Setup listeners
            self.mouse_listener = mouse.Listener(on_click=self._on_click)
            self.keyboard_listener = keyboard.Listener(on_press=self._on_press)
            
            self.mouse_listener.start()
            self.keyboard_listener.start()
            print("Action logging started...")

    def stop_logging(self):
        """Stops logging events and returns the log list."""
        if self.logging:
            self.logging = False
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            print("Action logging stopped.")
            return self.logs
        return []

    def get_logs(self):
        """Returns the current logs."""
        return self.logs

    def _on_click(self, x, y, button, pressed):
        """Callback for mouse clicks."""
        if pressed and self.logging:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] Mouse Click at ({x}, {y})"
            self.logs.append(log_entry)

    def _on_press(self, key):
        """Callback for key presses. Does not record the key itself."""
        if self.logging:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] Keyboard Activity Detected"
            # Avoid spamming logs with every single key press if typing fast
            # We could add a small debounce here if needed, but for now we log all.
            # To reduce noise, we might only log unique events per second in a real app.
            if not self.logs or self.logs[-1] != log_entry:
                 self.logs.append(log_entry)

if __name__ == "__main__":
    # Test the logger
    logger = ActionLogger()
    logger.start_logging()
    print("Type something or click around...")
    time.sleep(5)
    logs = logger.stop_logging()
    for log in logs:
        print(log)
