"""
User profile API for personalization engine
Manages hardware inventory, experience levels, and language preferences
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.orm import Session
import logging

from config import settings
from models import get_db
from models.user import UserProfile, JetsonModel, RobotType, ExperienceLevel, Language, Theme

logger = logging.getLogger(__name__)
router = APIRouter()


class HardwareProfile(BaseModel):
    """Hardware inventory"""
    has_rtx_gpu: bool = False
    has_jetson: bool = False
    jetson_model: Optional[str] = None
    robot_type: str = "none"
    has_realsense: bool = False
    has_lidar: bool = False


class ExperienceProfile(BaseModel):
    """Experience levels"""
    ros2: str = "none"
    ml: str = "none"
    robotics: str = "none"
    simulation: str = "none"


class PreferencesProfile(BaseModel):
    """User preferences"""
    language: str = "en"
    theme: str = "light"


class UserProfileCreate(BaseModel):
    """Request to create user profile"""
    email: EmailStr
    hardware: HardwareProfile
    experience: ExperienceProfile
    preferences: PreferencesProfile


class UserProfileUpdate(BaseModel):
    """Request to update user profile"""
    hardware: Optional[HardwareProfile] = None
    experience: Optional[ExperienceProfile] = None
    preferences: Optional[PreferencesProfile] = None


class UserProfileResponse(BaseModel):
    """User profile response"""
    id: str
    email: str
    hardware: HardwareProfile
    experience: ExperienceProfile
    preferences: PreferencesProfile
    created_at: str
    updated_at: str


@router.post("/profile", response_model=UserProfileResponse, tags=["Personalization"])
async def create_user_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    """
    Create new user profile

    Called during signup after Better-Auth creates the account
    """
    try:
        # Check if profile already exists
        existing_profile = db.query(UserProfile).filter(UserProfile.email == profile.email).first()
        if existing_profile:
            raise HTTPException(status_code=400, detail="Profile already exists")

        # Create new profile
        new_profile = UserProfile(
            email=profile.email,
            # Hardware
            has_rtx_gpu=profile.hardware.has_rtx_gpu,
            has_jetson=profile.hardware.has_jetson,
            jetson_model=JetsonModel(profile.hardware.jetson_model) if profile.hardware.jetson_model else None,
            robot_type=RobotType(profile.hardware.robot_type),
            has_realsense=profile.hardware.has_realsense,
            has_lidar=profile.hardware.has_lidar,
            # Experience
            ros2_experience=ExperienceLevel(profile.experience.ros2),
            ml_experience=ExperienceLevel(profile.experience.ml),
            robotics_experience=ExperienceLevel(profile.experience.robotics),
            simulation_experience=ExperienceLevel(profile.experience.simulation),
            # Preferences
            preferred_language=Language(profile.preferences.language),
            theme=Theme(profile.preferences.theme)
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        logger.info(f"Created profile for {profile.email}")

        return UserProfileResponse(
            id=str(new_profile.id),
            email=new_profile.email,
            hardware=HardwareProfile(**new_profile.to_dict()["hardware"]),
            experience=ExperienceProfile(**new_profile.to_dict()["experience"]),
            preferences=PreferencesProfile(**new_profile.to_dict()["preferences"]),
            created_at=new_profile.created_at.isoformat(),
            updated_at=new_profile.updated_at.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to create profile")


@router.get("/profile/{user_id}", response_model=UserProfileResponse, tags=["Personalization"])
async def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Get user profile by ID"""
    try:
        profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        return UserProfileResponse(
            id=str(profile.id),
            email=profile.email,
            hardware=HardwareProfile(**profile.to_dict()["hardware"]),
            experience=ExperienceProfile(**profile.to_dict()["experience"]),
            preferences=PreferencesProfile(**profile.to_dict()["preferences"]),
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to get profile")


@router.put("/profile/{user_id}", response_model=UserProfileResponse, tags=["Personalization"])
async def update_user_profile(user_id: str, updates: UserProfileUpdate, db: Session = Depends(get_db)):
    """Update user profile"""
    try:
        profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Update hardware if provided
        if updates.hardware:
            profile.has_rtx_gpu = updates.hardware.has_rtx_gpu
            profile.has_jetson = updates.hardware.has_jetson
            if updates.hardware.jetson_model:
                profile.jetson_model = JetsonModel(updates.hardware.jetson_model)
            profile.robot_type = RobotType(updates.hardware.robot_type)
            profile.has_realsense = updates.hardware.has_realsense
            profile.has_lidar = updates.hardware.has_lidar

        # Update experience if provided
        if updates.experience:
            profile.ros2_experience = ExperienceLevel(updates.experience.ros2)
            profile.ml_experience = ExperienceLevel(updates.experience.ml)
            profile.robotics_experience = ExperienceLevel(updates.experience.robotics)
            profile.simulation_experience = ExperienceLevel(updates.experience.simulation)

        # Update preferences if provided
        if updates.preferences:
            profile.preferred_language = Language(updates.preferences.language)
            profile.theme = Theme(updates.preferences.theme)

        db.commit()
        db.refresh(profile)

        logger.info(f"Updated profile for user {user_id}")

        return UserProfileResponse(
            id=str(profile.id),
            email=profile.email,
            hardware=HardwareProfile(**profile.to_dict()["hardware"]),
            experience=ExperienceProfile(**profile.to_dict()["experience"]),
            preferences=PreferencesProfile(**profile.to_dict()["preferences"]),
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to update profile")
