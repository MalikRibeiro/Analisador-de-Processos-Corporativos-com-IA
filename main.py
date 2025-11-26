import time
import threading
import sys
import os

# Ensure the app module is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.screen_recorder import ScreenRecorder
from app.action_logger import ActionLogger
from app.process_miner import ProcessMiner
from app.process_analyst_agent import ProcessAnalystAgent
from app.automation_advisor import AutomationAdvisor

def main():
    print("=== Corporate Process Analyzer ===")
    print("Initializing modules...")

    # Create output directories if they don't exist
    data_dir = os.path.join(os.getcwd(), "data")
    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    video_path = os.path.join(data_dir, "process_recording.mp4")
    report_path = os.path.join(reports_dir, "relatorio_processo.md")

    # Initialize modules
    recorder = ScreenRecorder(output_file=video_path)
    logger = ActionLogger()
    miner = ProcessMiner()
    
    try:
        analyst = ProcessAnalystAgent()
        advisor = AutomationAdvisor(output_dir=reports_dir)
    except Exception as e:
        print(f"Error initializing AI agents: {e}")
        print("Please check your .env file and API Key.")
        return

    input("Press Enter to START recording the process...")

    # Start collection threads
    recorder.start_recording()
    logger.start_logging()
    miner.start_monitoring()

    print("\nRecording in progress... Perform the business process now.")
    print("Check the 'Gravando Processo' window to see what is being captured.")
    input("Press Enter to STOP recording and start analysis...\n")

    # Stop collection
    print("Stopping recording and saving data...")
    recorder.stop_recording()
    action_logs = logger.stop_logging()
    window_logs = miner.stop_monitoring()

    # Aggregate logs
    print(f"Captured {len(action_logs)} action events and {len(window_logs)} window context events.")
    
    all_logs = sorted(action_logs + window_logs)
    
    print("Starting AI Analysis...")
    try:
        analysis_result = analyst.analyze_process(
            video_path=video_path,
            logs=all_logs
        )
        
        print("Analysis complete. Generating report...")
        advisor.generate_report(analysis_result, report_filename="relatorio_processo.md")
        
        print(f"\nSuccess! Report saved to '{report_path}'.")
        print(f"Check the '{reports_dir}' folder for diagrams as well.")

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
