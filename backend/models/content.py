"""
Content tracking models: ReadingProgress, RAGQueryLog, TranslationCache
Matches data-model.md specification
"""
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from models import Base


class ReadingProgress(Base):
    """Track which sections users have viewed and completed"""
    __tablename__ = "reading_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    section_id = Column(String(255), nullable=False, index=True)  # e.g., "modules/ros2/index"

    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    time_spent_seconds = Column(Integer, default=0, nullable=False)
    scroll_percentage = Column(Float, default=0.0, nullable=False)  # 0.0 to 1.0

    def __repr__(self):
        return f"<ReadingProgress(user={self.user_id}, section={self.section_id})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "section_id": self.section_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "time_spent_seconds": self.time_spent_seconds,
            "scroll_percentage": self.scroll_percentage,
            "is_completed": self.scroll_percentage >= 0.9,
        }


class RAGQueryLog(Base):
    """Track chatbot interactions for quality improvement and analytics"""
    __tablename__ = "rag_query_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id", ondelete="SET NULL"), nullable=True, index=True)

    query_text = Column(Text, nullable=False)
    query_mode = Column(String(50), nullable=False)  # 'book-wide' or 'selection-based'
    selected_text = Column(Text, nullable=True)  # Only for selection-based queries

    # RAG retrieval metadata
    retrieved_chunks = Column(JSON, nullable=True)  # Array of {section_id, score, excerpt}
    response_text = Column(Text, nullable=False)

    # User feedback
    user_feedback = Column(String(20), nullable=True)  # 'helpful', 'not-helpful', null
    feedback_comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    response_time_ms = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<RAGQueryLog(id={self.id}, mode={self.query_mode})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "query_text": self.query_text,
            "query_mode": self.query_mode,
            "selected_text": self.selected_text,
            "retrieved_chunks": self.retrieved_chunks,
            "response_text": self.response_text,
            "user_feedback": self.user_feedback,
            "feedback_comment": self.feedback_comment,
            "created_at": self.created_at.isoformat(),
            "response_time_ms": self.response_time_ms,
        }


class TranslationCache(Base):
    """Cache translated content to reduce API costs and improve performance"""
    __tablename__ = "translation_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    section_id = Column(String(255), nullable=False, index=True)
    target_language = Column(String(10), nullable=False, index=True)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA-256 of original content

    original_content = Column(Text, nullable=False)
    translated_content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    access_count = Column(Integer, default=0, nullable=False)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<TranslationCache(section={self.section_id}, lang={self.target_language})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "section_id": self.section_id,
            "target_language": self.target_language,
            "content_hash": self.content_hash,
            "translated_content": self.translated_content,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed_at": self.last_accessed_at.isoformat(),
        }
