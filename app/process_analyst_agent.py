import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

class ProcessAnalystAgent:
    """
    Interacts with Google Gemini to analyze the recorded video and logs.
    """

    def __init__(self):
        # Load .env from the project root (parent directory of 'app')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        env_path = os.path.join(project_root, '.env')
        
        load_dotenv(dotenv_path=env_path)
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # Debug print for API Key
        if self.api_key:
            masked_key = self.api_key[:5] + "..." + self.api_key[-3:]
            print(f"DEBUG: Loaded API Key: {masked_key}")
        else:
            print("DEBUG: API Key NOT found!")
            raise ValueError("GOOGLE_API_KEY not found in .env file.")
        
        genai.configure(api_key=self.api_key)
        
        # Model selection logic with fallback
        self.model = self._initialize_model()

    def _initialize_model(self):
        """Attempts to initialize the best available model."""
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-pro"
        ]
        
        for model_name in models_to_try:
            try:
                print(f"DEBUG: Attempting to initialize model '{model_name}'...")
                model = genai.GenerativeModel(model_name)
                # Simple check if model is valid (doesn't guarantee API access yet, but catches basic name errors)
                print(f"DEBUG: Successfully initialized model '{model_name}'")
                self.model_name = model_name
                return model
            except Exception as e:
                print(f"WARNING: Failed to initialize '{model_name}'. Error: {e}")
        
        # If all fail, try to list available models for debugging
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

class ProcessAnalystAgent:
    """
    Interacts with Google Gemini to analyze the recorded video and logs.
    """

    def __init__(self):
        # Load .env from the project root (parent directory of 'app')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        env_path = os.path.join(project_root, '.env')
        
        load_dotenv(dotenv_path=env_path)
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # Debug print for API Key
        if self.api_key:
            masked_key = self.api_key[:5] + "..." + self.api_key[-3:]
            print(f"DEBUG: Loaded API Key: {masked_key}")
        else:
            print("DEBUG: API Key NOT found!")
            raise ValueError("GOOGLE_API_KEY not found in .env file.")
        
        genai.configure(api_key=self.api_key)
        
        # Model selection logic with fallback
        self.model = self._initialize_model()

    def _initialize_model(self):
        """Attempts to initialize the best available model."""
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-pro"
        ]
        
        for model_name in models_to_try:
            try:
                print(f"DEBUG: Attempting to initialize model '{model_name}'...")
                model = genai.GenerativeModel(model_name)
                # Simple check if model is valid (doesn't guarantee API access yet, but catches basic name errors)
                print(f"DEBUG: Successfully initialized model '{model_name}'")
                self.model_name = model_name
                return model
            except Exception as e:
                print(f"WARNING: Failed to initialize '{model_name}'. Error: {e}")
        
        # If all fail, try to list available models for debugging
        print("ERROR: Could not initialize any preferred model. Listing available models...")
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"DEBUG: Found model '{m.name}' with generateContent support.")
                    return genai.GenerativeModel(m.name)
        except Exception as e:
            print(f"ERROR: Failed to list models. Error: {e}")
            raise
        
        # If we get here, none of the models are suitable
        raise ValueError("No suitable models found for initialization.")

    def analyze_process(self, video_path, logs, language="Português"):
        """
        Uploads the video and sends it along with logs to Gemini for analysis.

        Args:
            video_path (str): Path to the recorded MP4 file.
            logs (list): List of log strings (actions and window contexts).
            language (str): Language for the analysis report.

        Returns:
            str: The raw analysis text from Gemini.
        """
        print(f"Uploading video {video_path} to Gemini...")
        
        if not os.path.exists(video_path):
             raise FileNotFoundError(f"Video file not found at: {video_path}")

        video_file = genai.upload_file(path=video_path)
        
        # Wait for processing
        print(f"Video uploaded. State: {video_file.state.name}")
        while video_file.state.name == "PROCESSING":
            print("Waiting for video processing...")
            time.sleep(2)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError("Video processing failed.")

        print("Video processed. Generating analysis...")

        # Construct the prompt
        logs_text = "\n".join(logs)
        prompt = f"""
        You are an expert Process Analyst and Automation Engineer.
        I have recorded a user's screen performing a business process.
        Attached is the video recording.
        Below are the logs of their actions and active windows during the recording:

        --- LOGS START ---
        {logs_text}
        --- LOGS END ---

        Please analyze this process and provide:
        1. A detailed step-by-step description of the workflow observed.
        2. Identification of bottlenecks, inefficiencies, or repetitive tasks.
        3. A Mermaid flowchart diagram representing the process.
        4. Concrete suggestions for automation (e.g., using Python scripts, RPA tools, or API integrations).

        IMPORTANT: Please write the entire response in {language}.
        Format your response in Markdown.
        """

        response = self.model.generate_content([video_file, prompt])
        
        return response.text

if __name__ == "__main__":
    # Test the agent
    try:
        agent = ProcessAnalystAgent()
        print("Agent initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")