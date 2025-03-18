import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_anthropic_api_key():
    """Get the Anthropic API key from environment variables"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in environment variables. "
            "Please create a .env file with your API key or set it manually."
        )
    return api_key