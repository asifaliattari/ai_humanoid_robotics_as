"""Database models for Physical AI & Humanoid Robotics Book"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from config import settings

# Base class for models (defined before engine to avoid circular imports)
Base = declarative_base()

# Database engine - handle SQLite differently from other databases
if settings.database_url.startswith("sqlite"):
    # SQLite doesn't support pool_size/max_overflow, use StaticPool
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.debug,
    )
else:
    # PostgreSQL or other databases support connection pooling
    engine = create_engine(
        settings.database_url,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        echo=settings.debug,
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Import all models to ensure they are registered with Base
from .user import UserProfile  # noqa: F401, E402
from .auth import User  # noqa: F401, E402


def init_db():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
