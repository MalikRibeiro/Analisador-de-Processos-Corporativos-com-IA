import cv2
import numpy as np
import mss
import threading
import time
from datetime import datetime

class ScreenRecorder:
    """
    Records the screen activity to an MP4 video file.
    Runs in a separate thread to avoid blocking the main application.
    """

    def __init__(self, output_file="output.mp4", fps=10.0):
        """
        Initialize the ScreenRecorder.

        Args:
            output_file (str): Path to save the video file.
            fps (float): Frames per second for the recording.
        """
        self.output_file = output_file
        self.fps = fps
        self.recording = False
        self.thread = None
        self.width = 1920
        self.height = 1080
        self._stop_event = threading.Event()

    def start_recording(self):
        """Starts the screen recording in a separate thread."""
        if not self.recording:
            self.recording = True
            self._stop_event.clear()
            self.thread = threading.Thread(target=self._record)
            self.thread.start()
            print(f"Started recording to {self.output_file}...")

    def stop_recording(self):
        """Stops the screen recording."""
        if self.recording:
            self.recording = False
            self._stop_event.set()
            if self.thread:
                self.thread.join()
            print("Recording stopped.")

    def _record(self):
        """Internal method to capture screen and write to video file."""
        with mss.mss() as sct:
            # Get the primary monitor dimensions
            monitor = sct.monitors[1]
            self.width = monitor["width"]
            self.height = monitor["height"]

            # Define the codec and create VideoWriter object
            # mp4v is a good option for MP4 files
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.output_file, fourcc, self.fps, (self.width, self.height))

            frame_duration = 1.0 / self.fps

            while not self._stop_event.is_set():
                start_time = time.time()

                # Capture the screen
                img = sct.grab(monitor)
                
                # Convert to numpy array and then to BGR (OpenCV format)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Write the frame
                out.write(frame)

                # Visual Feedback
                # Resize for preview to avoid taking up too much screen
                preview_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                cv2.imshow("Gravando Processo (Pressione 'q' para minimizar)", preview_frame)
                
                # Check for 'q' key to close the preview window (but continue recording)
                # waitKey(1) is required for imshow to work
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()

                # Control FPS
                elapsed = time.time() - start_time
                wait_time = max(0, frame_duration - elapsed)
                time.sleep(wait_time)

            out.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test the recorder
    recorder = ScreenRecorder()
    recorder.start_recording()
    time.sleep(5)  # Record for 5 seconds
    recorder.stop_recording()
