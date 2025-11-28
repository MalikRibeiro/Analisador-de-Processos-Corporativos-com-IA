import os
import time
import google.generativeai as genai
from config.secrets_manager import SecretsManager

class AIService:
    """
    Interacts with Google Gemini to analyze the recorded video and logs.
    """

    def __init__(self):
        self.api_key = SecretsManager.get_api_key()
        
        # Debug print for API Key
        if self.api_key:
            masked_key = self.api_key[:5] + "..." + self.api_key[-3:]
            print(f"DEBUG: Loaded API Key: {masked_key}")
            genai.configure(api_key=self.api_key)
            # Model selection logic with fallback
            self.model = self._initialize_model()
        else:
            print("DEBUG: API Key NOT found!")
            self.model = None
            # We don't raise error here to allow app to start, but analysis will fail later if not set.

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
        if not self.model:
             # Try to re-init if key was added later
             self.api_key = SecretsManager.get_api_key()
             if self.api_key:
                 genai.configure(api_key=self.api_key)
                 self.model = self._initialize_model()
             else:
                 raise ValueError("API Key not configured.")

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
        3. A structured list of steps for the process flow, provided as a JSON array.
           CRITICAL RULES FOR JSON FLOWCHART:
           - Return a raw JSON array of objects.
           - Each object must have:
             - "id": A unique identifier (e.g., "step1", "step2").
             - "label": A concise text description of the step (max 10 words).
             - "type": "process" (for actions) or "decision" (for questions/branches).
             - "next": The ID of the next step (or null if end).
           - Example format:
             [
               {"id": "s1", "label": "Start Process", "type": "process", "next": "s2"},
               {"id": "s2", "label": "Is data valid?", "type": "decision", "next": "s3"},
               ...
             ]
           - DO NOT include any Markdown formatting (like ```json) around the JSON. Just the raw array.
        4. Concrete suggestions for automation (e.g., using Python scripts, RPA tools, or API integrations).

        IMPORTANT: Please write the entire response in {language}.
        Format your response in Markdown, BUT keep the JSON array as raw text block labeled "### FLOWCHART_JSON" so I can extract it easily.
        Example of expected output structure:
        
        # Title
        ... text ...
        
        ### FLOWCHART_JSON
        [ ... json array ... ]
        
        ### Suggestions
        ... text ...
        """

        response = self.model.generate_content([video_file, prompt])
        
        return response.text
