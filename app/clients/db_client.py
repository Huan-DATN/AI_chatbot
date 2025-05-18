from langchain_community.utilities import SQLDatabase
from app.config import get_config

config = get_config()

db = SQLDatabase.from_uri(config.DB_URL)
