import sys
import os

# Ensure the src directory is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_window import MainWindow

if __name__ == "__main__":
    # Run cleanup
    from src.utils.file_utils import cleanup_files_by_count
    
    # Define directories to clean
    base_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(base_dir, "reports")
    recordings_dir = os.path.join(base_dir, "recordings")
    
    # Keep last 10 files in each directory
    cleanup_files_by_count([reports_dir, recordings_dir], max_files=10)

    app = MainWindow()
    app.mainloop()
