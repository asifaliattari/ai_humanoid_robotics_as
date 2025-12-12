"""
Authentication model for user accounts
Separate from UserProfile to handle login credentials
"""
from sqlalchemy import Column, String, Boolean, DateTime
import uuid
from datetime import datetime

from models import Base


class User(Base):
    """User account for authentication"""
    __tablename__ = "users"

    # Primary key - using String for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # Hashed password

    # User info
    name = Column(String(255), nullable=True)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(email={self.email}, id={self.id})>"
