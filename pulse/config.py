import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def validate_config() -> bool:
    """Checks if the OpenAI API key is present."""
    return bool(OPENAI_API_KEY)