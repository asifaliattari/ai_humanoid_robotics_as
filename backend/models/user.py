"""
User profile model matching data-model.md specification
Stores hardware inventory, experience levels, and preferences
"""
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
import uuid
from datetime import datetime
import enum

from models import Base


class JetsonModel(str, enum.Enum):
    """Jetson Orin model options"""
    ORIN_NANO_4GB = "orin-nano-4gb"
    ORIN_NANO_8GB = "orin-nano-8gb"
    ORIN_NX_8GB = "orin-nx-8gb"
    ORIN_NX_16GB = "orin-nx-16gb"
    NONE = "none"


class RobotType(str, enum.Enum):
    """Robot platform options"""
    NONE = "none"
    PROXY = "proxy"
    GO2 = "go2"
    OP3 = "op3"
    G1 = "g1"


class ExperienceLevel(str, enum.Enum):
    """Experience level options"""
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Language(str, enum.Enum):
    """Supported language options"""
    EN = "en"
    UR = "ur"
    FR = "fr"
    AR = "ar"
    DE = "de"


class Theme(str, enum.Enum):
    """UI theme options"""
    LIGHT = "light"
    DARK = "dark"


class UserProfile(Base):
    """User profile with hardware inventory and experience levels"""
    __tablename__ = "user_profiles"

    # Primary key - using String for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Hardware Inventory
    has_rtx_gpu = Column(Boolean, default=False, nullable=False)
    has_jetson = Column(Boolean, default=False, nullable=False)
    jetson_model = Column(SQLEnum(JetsonModel), default=JetsonModel.NONE, nullable=True)
    robot_type = Column(SQLEnum(RobotType), default=RobotType.NONE, nullable=False)
    has_realsense = Column(Boolean, default=False, nullable=False)
    has_lidar = Column(Boolean, default=False, nullable=False)

    # Experience Levels
    ros2_experience = Column(SQLEnum(ExperienceLevel), default=ExperienceLevel.NONE, nullable=False)
    ml_experience = Column(SQLEnum(ExperienceLevel), default=ExperienceLevel.NONE, nullable=False)
    robotics_experience = Column(SQLEnum(ExperienceLevel), default=ExperienceLevel.NONE, nullable=False)
    simulation_experience = Column(SQLEnum(ExperienceLevel), default=ExperienceLevel.NONE, nullable=False)

    # Preferences
    preferred_language = Column(SQLEnum(Language), default=Language.EN, nullable=False)
    theme = Column(SQLEnum(Theme), default=Theme.LIGHT, nullable=False)

    def __repr__(self):
        return f"<UserProfile(email={self.email}, id={self.id})>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "hardware": {
                "has_rtx_gpu": self.has_rtx_gpu,
                "has_jetson": self.has_jetson,
                "jetson_model": self.jetson_model.value if self.jetson_model else None,
                "robot_type": self.robot_type.value,
                "has_realsense": self.has_realsense,
                "has_lidar": self.has_lidar,
            },
            "experience": {
                "ros2": self.ros2_experience.value,
                "ml": self.ml_experience.value,
                "robotics": self.robotics_experience.value,
                "simulation": self.simulation_experience.value,
            },
            "preferences": {
                "language": self.preferred_language.value,
                "theme": self.theme.value,
            },
        }
