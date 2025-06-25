import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv(
        "DB_URL", "postgresql+psycopg2://postgres:postgres@localhost:5444/wedding"
    )
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = os.getenv("REDIS_DB", 0)
    REDIS_USERNAME = os.getenv("REDIS_USERNAME", "default")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "password")
    # Embedding model configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    # FAQ configuration
    FAQ_SIMILARITY_THRESHOLD = float(os.getenv("FAQ_SIMILARITY_THRESHOLD", "0.7"))
    FAQ_TOP_K = int(os.getenv("FAQ_TOP_K", "3"))


def get_config():
    """Get the configuration object."""
    return Config()
