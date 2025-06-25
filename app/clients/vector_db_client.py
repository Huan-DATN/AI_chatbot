from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import get_config
import os

config = get_config()

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Path to store the vector database
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "vector_db")

# Ensure the directory exists
os.makedirs(VECTOR_DB_PATH, exist_ok=True)


class VectorDBClient:
    def __init__(self):
        self.embeddings = embedding_model
        self.vector_db = None

    def initialize_from_texts(self, texts, metadatas=None):
        self.vector_db = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        return self.vector_db

    def load_local(self, index_name="faiss_index"):
        try:
            path = os.path.join(VECTOR_DB_PATH, index_name)
            if os.path.exists(path):
                self.vector_db = FAISS.load_local(path, self.embeddings)
                return self.vector_db
            return None
        except Exception as e:
            print(f"Error loading vector database: {e}")
            return None

    def save_local(self, index_name="faiss_index"):
        """Save the vector database locally."""
        if self.vector_db:
            path = os.path.join(VECTOR_DB_PATH, index_name)
            self.vector_db.save_local(path)
            return True
        return False

    def similarity_search(self, query, k=5):
        if not self.vector_db:
            return []
        return self.vector_db.similarity_search(query, k=k)

    def similarity_search_with_score(self, query, k=5):
        if not self.vector_db:
            return []
        return self.vector_db.similarity_search_with_score(query, k=k)



vector_db_client = VectorDBClient()

def get_vector_db_client():
    """Get the vector database client."""
    return vector_db_client
