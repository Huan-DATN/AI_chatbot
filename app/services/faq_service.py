import json
import os
from typing import List, Dict, Any, Optional
from app.models.faq import FAQItem, FAQCollection
from app.clients.vector_db_client import get_vector_db_client
from app.config import get_config

config = get_config()

# Path to store FAQ data
FAQ_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "faq")
FAQ_FILE_PATH = os.path.join(FAQ_DATA_PATH, "faq.json")

# Ensure the directory exists
os.makedirs(FAQ_DATA_PATH, exist_ok=True)


class FAQService:
    def __init__(self):
        self.vector_db_client = get_vector_db_client()
        self.faq_collection = self._load_faq_data()
        self._initialize_vector_db()

    def _load_faq_data(self) -> FAQCollection:
        """Load FAQ data from file."""
        try:
            if os.path.exists(FAQ_FILE_PATH):
                with open(FAQ_FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return FAQCollection.from_dict(data)
            return FAQCollection()
        except Exception as e:
            print(f"Error loading FAQ data: {e}")
            return FAQCollection()

    def _save_faq_data(self):
        """Save FAQ data to file."""
        try:
            with open(FAQ_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.faq_collection.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving FAQ data: {e}")
            return False

    def _initialize_vector_db(self):
        """Initialize the vector database."""
        if not self.faq_collection.items:
            return

        if not self.vector_db_client.load_local("faq_index"):
            texts = self.faq_collection.get_texts_for_embedding()
            metadatas = self.faq_collection.get_metadatas_for_embedding()
            self.vector_db_client.initialize_from_texts(texts, metadatas)
            self.vector_db_client.save_local("faq_index")

    def add_faq_item(self, item: FAQItem):
        """Add a FAQ item."""
        self.faq_collection.add_item(item)
        self._save_faq_data()

        self.vector_db_client.initialize_from_texts(
            self.faq_collection.get_texts_for_embedding(),
            self.faq_collection.get_metadatas_for_embedding()
        )
        self.vector_db_client.save_local("faq_index")

    def get_all_faq_items(self) -> List[FAQItem]:
        """Get all FAQ items."""
        return self.faq_collection.items

    def search_faq(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """Search FAQ items by query."""
        if k is None:
            k = config.FAQ_TOP_K

        results = self.vector_db_client.similarity_search_with_score(query, k=k)

        threshold = config.FAQ_SIMILARITY_THRESHOLD
        filtered_results = []

        for doc, score in results:
            similarity = 1 - score
            if similarity >= threshold:
                result = doc.metadata.copy()
                result["similarity"] = similarity
                filtered_results.append(result)

        return filtered_results

    def get_sample_faq_items(self) -> List[FAQItem]:
        """Get sample FAQ items."""
        return [
            FAQItem(
                question="Sản phẩm OCOP là gì?",
                answer="Sản phẩm OCOP (One Commune One Product) là các sản phẩm đặc trưng của mỗi địa phương được công nhận theo chương trình mỗi xã một sản phẩm của Chính phủ, nhằm phát triển kinh tế nông thôn theo hướng phát triển nội lực và gia tăng giá trị.",
                category="Thông tin chung",
                tags=["OCOP", "sản phẩm"]
            ),
            FAQItem(
                question="Làm thế nào để đánh giá chất lượng sản phẩm OCOP?",
                answer="Sản phẩm OCOP được đánh giá theo thang điểm từ 1-5 sao, với 5 sao là cao nhất. Tiêu chí đánh giá bao gồm: chất lượng sản phẩm, khả năng tiếp thị, quy trình sản xuất, và tác động đến cộng đồng.",
                category="Chất lượng",
                tags=["đánh giá", "chất lượng", "sao"]
            ),
            FAQItem(
                question="Tôi có thể mua sản phẩm OCOP ở đâu?",
                answer="Bạn có thể mua sản phẩm OCOP tại các cửa hàng OCOP chính thức, chợ đầu mối, siêu thị, hoặc các sàn thương mại điện tử được chứng nhận bán sản phẩm OCOP. Hệ thống của chúng tôi cũng cung cấp thông tin về các điểm bán hàng gần nhất.",
                category="Mua sắm",
                tags=["mua sắm", "cửa hàng"]
            ),
        ]

    def initialize_sample_data(self):
        """Initialize sample data if no data exists."""
        if not self.faq_collection.items:
            sample_items = self.get_sample_faq_items()
            for item in sample_items:
                self.faq_collection.add_item(item)
            self._save_faq_data()
            self._initialize_vector_db()




# Create a singleton instance
_faq_service = None

def get_faq_service():
    """Get the FAQ service singleton."""
    global _faq_service
    if _faq_service is None:
        _faq_service = FAQService()
        # Initialize with sample data if empty
        _faq_service.initialize_sample_data()
    return _faq_service
