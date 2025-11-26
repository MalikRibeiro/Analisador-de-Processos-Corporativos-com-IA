import os
from config.settings import ENV_PATH

class SecretsManager:
    @staticmethod
    def get_api_key():
        """Retrieves the Google API Key from the .env file or environment variables."""
        # Try loading from file first if not in env
        if not os.environ.get("GOOGLE_API_KEY") and os.path.exists(ENV_PATH):
            with open(ENV_PATH, "r") as f:
                for line in f:
                    if line.startswith("GOOGLE_API_KEY="):
                        return line.strip().split("=", 1)[1]
        return os.environ.get("GOOGLE_API_KEY")

    @staticmethod
    def save_api_key(api_key):
        """Saves the Google API Key to the .env file."""
        with open(ENV_PATH, "w") as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")
        # Update current process env var as well
        os.environ["GOOGLE_API_KEY"] = api_key
