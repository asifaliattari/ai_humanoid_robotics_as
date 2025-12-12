"""Personalization API endpoints"""
from .user_profile import router as user_profile_router
from .content_adapter import router as content_adapter_router

__all__ = ["user_profile_router", "content_adapter_router"]
