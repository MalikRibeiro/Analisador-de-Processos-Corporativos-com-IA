import pygetwindow as gw
import time
import threading
from datetime import datetime

class ProcessMiner:
    """
    Monitors the active window to identify the context of the user's work.
    """

    def __init__(self, interval=1.0):
        """
        Args:
            interval (float): How often to check the active window (in seconds).
        """
        self.interval = interval
        self.monitoring = False
        self.logs = []
        self.thread = None
        self._stop_event = threading.Event()

    def start_monitoring(self):
        """Starts monitoring the active window in a separate thread."""
        if not self.monitoring:
            self.monitoring = True
            self.logs = []
            self._stop_event.clear()
            self.thread = threading.Thread(target=self._monitor)
            self.thread.start()
            print("Process monitoring started...")

    def stop_monitoring(self):
        """Stops monitoring."""
        if self.monitoring:
            self.monitoring = False
            self._stop_event.set()
            if self.thread:
                self.thread.join()
            print("Process monitoring stopped.")
            return self.logs
        return []

    def get_logs(self):
        return self.logs

    def _monitor(self):
        """Internal method to loop and check active window."""
        last_window_title = ""
        while not self._stop_event.is_set():
            try:
                window = gw.getActiveWindow()
                if window:
                    title = window.title
                    # Only log if the window changed or periodically?
                    # The requirement says "a cada segundo", so we log every second.
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    log_entry = f"[{timestamp}] Active Window: {title}"
                    
                    # Optional: Deduplicate consecutive identical logs to save space
                    # if title != last_window_title:
                    self.logs.append(log_entry)
                    last_window_title = title
                else:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.logs.append(f"[{timestamp}] Active Window: None")

            except Exception as e:
                print(f"Error getting active window: {e}")
            
            time.sleep(self.interval)

if __name__ == "__main__":
    # Test the miner
    miner = ProcessMiner()
    miner.start_monitoring()
    time.sleep(5)
    logs = miner.stop_monitoring()
    for log in logs:
        print(log)
