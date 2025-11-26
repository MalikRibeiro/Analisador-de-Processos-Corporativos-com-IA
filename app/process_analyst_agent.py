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
        except Exception as e:
            print(f"Initialization failed: {e}")