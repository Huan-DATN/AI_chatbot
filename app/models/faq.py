from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class FAQItem(BaseModel):
    """Model for a FAQ item."""
    id: Optional[int] = None
    question: str
    answer: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(**data)

    @classmethod
    def from_db_row(cls, row):
        """Create from database row."""
        if not row:
            return None

        # Convert tags from string to list if needed
        tags = row.get("tags")
        if isinstance(tags, str):
            try:
                import json
                tags = json.loads(tags)
            except:
                tags = tags.split(",") if tags else []

        # Convert metadata from string to dict if needed
        metadata = row.get("metadata")
        if isinstance(metadata, str):
            try:
                import json
                metadata = json.loads(metadata)
            except:
                metadata = {}

        return cls(
            id=row.get("id"),
            question=row.get("question"),
            answer=row.get("answer"),
            category=row.get("category"),
            tags=tags,
            metadata=metadata,
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )


class FAQCollection(BaseModel):
    """Collection of FAQ items."""
    items: List[FAQItem] = []

    def add_item(self, item: FAQItem):
        """Add an item to the collection."""
        self.items.append(item)

    def get_questions(self) -> List[str]:
        """Get all questions."""
        return [item.question for item in self.items]

    def get_texts_for_embedding(self) -> List[str]:
        """Get texts for embedding."""
        return self.get_questions()

    def get_metadatas_for_embedding(self) -> List[Dict[str, Any]]:
        """Get metadata for embedding."""
        return [item.to_dict() for item in self.items]

    def to_dict(self):
        """Convert to dictionary."""
        return {"items": [item.to_dict() for item in self.items]}

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(items=[FAQItem.from_dict(item) for item in data["items"]])

    @classmethod
    def from_db_rows(cls, rows):
        """Create from database rows."""
        return cls(items=[FAQItem.from_db_row(row) for row in rows if row])
