from app.config import get_config

config = get_config()


def get_api_key():
    """Get the API key from the environment variable."""
    return config.GEMINI_API_KEY


def get_model():
    """Get the model name from the environment variable."""
    return config.GEMINI_MODEL
