import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def validate_config() -> bool:
    """Checks if the GROQ API key is present."""
    return bool(GROQ_API_KEY)