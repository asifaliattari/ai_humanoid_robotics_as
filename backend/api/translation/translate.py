"""
Translation API for multi-language support (EN/UR/FR/AR/DE)
Translates book content with caching to reduce API costs
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
import time
import logging
from openai import OpenAI

from config import settings
from models import get_db
from models.content import TranslationCache
from services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)
router = APIRouter()


class TranslateRequest(BaseModel):
    """Request body for translation"""
    section_id: str = Field(..., description="Section to translate (e.g., 'modules/ros2/index')")
    target_language: str = Field(..., pattern="^(ur|fr|ar|de)$", description="Target language: ur, fr, ar, de")
    user_id: Optional[str] = Field(None, description="Optional user ID")


class TranslateResponse(BaseModel):
    """Response for translation"""
    translated_content: str = Field(..., description="Translated markdown with code blocks unchanged")
    cache_hit: bool = Field(..., description="Whether result was from cache")
    translation_time_ms: int = Field(..., description="Time taken for translation")


LANGUAGE_NAMES = {
    "ur": "Urdu",
    "fr": "French",
    "ar": "Arabic",
    "de": "German"
}


@router.post("/translate", response_model=TranslateResponse, tags=["Translation"])
async def translate_content(request: TranslateRequest, db: Session = Depends(get_db)):
    """
    Translate section content to target language

    Process:
    1. Compute content hash
    2. Check cache for existing translation
    3. If cache miss, use GPT-4 to translate
    4. Store in cache
    5. Return translated content

    Translation rules:
    - Code blocks remain in English
    - Commands, file paths, URLs unchanged
    - Technical terms (ROS 2, Isaac Sim, URDF) unchanged
    """
    start_time = time.time()

    try:
        # TODO: Load original content from section_id
        # For now, using placeholder
        original_content = f"# Sample content for {request.section_id}"

        # Step 1: Compute content hash
        content_hash = EmbeddingService.compute_content_hash(original_content)

        # Step 2: Check cache
        cached_translation = db.query(TranslationCache).filter(
            TranslationCache.section_id == request.section_id,
            TranslationCache.target_language == request.target_language,
            TranslationCache.content_hash == content_hash
        ).first()

        if cached_translation:
            # Cache hit - update access stats
            cached_translation.access_count += 1
            from datetime import datetime
            cached_translation.last_accessed_at = datetime.utcnow()
            db.commit()

            translation_time = int((time.time() - start_time) * 1000)
            logger.info(f"Cache hit for {request.section_id} -> {request.target_language}")

            return TranslateResponse(
                translated_content=cached_translation.translated_content,
                cache_hit=True,
                translation_time_ms=translation_time
            )

        # Step 3: Cache miss - translate using GPT-4
        logger.info(f"Cache miss - translating {request.section_id} to {request.target_language}")

        target_lang_name = LANGUAGE_NAMES[request.target_language]

        system_prompt = f"""You are a professional technical translator for a robotics textbook.
Translate the following Markdown content from English to {target_lang_name}.

CRITICAL RULES:
1. DO NOT translate code blocks (text between ``` markers)
2. DO NOT translate commands, file paths, or URLs
3. DO NOT translate technical terms: ROS 2, Isaac Sim, URDF, Gazebo, Unity, Jetson, NVIDIA
4. DO translate headings, paragraphs, list items, and table text
5. Preserve all Markdown formatting (**, ##, -, |, etc.)
6. Maintain the exact structure of the document

If translating to Urdu or Arabic:
- Use proper right-to-left script
- Keep technical terms in English/Latin script
- Ensure proper grammar and natural phrasing"""

        user_prompt = f"""Translate this content to {target_lang_name}:

{original_content}

Remember: Keep code blocks, commands, and technical terms in English."""

        client = OpenAI(api_key=settings.openai_api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # GPT-4 for better translation quality
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent translation
        )

        translated_content = completion.choices[0].message.content

        # Step 4: Store in cache
        translation_cache = TranslationCache(
            section_id=request.section_id,
            target_language=request.target_language,
            content_hash=content_hash,
            original_content=original_content,
            translated_content=translated_content,
            access_count=1
        )
        db.add(translation_cache)
        db.commit()

        translation_time = int((time.time() - start_time) * 1000)
        logger.info(f"Translation completed in {translation_time}ms")

        return TranslateResponse(
            translated_content=translated_content,
            cache_hit=False,
            translation_time_ms=translation_time
        )

    except Exception as e:
        logger.error(f"Error in translate_content: {e}")
        raise HTTPException(status_code=500, detail="Translation failed")


@router.get("/supported-languages", tags=["Translation"])
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "en", "name": "English", "direction": "ltr"},
            {"code": "ur", "name": "Urdu", "direction": "rtl"},
            {"code": "fr", "name": "French", "direction": "ltr"},
            {"code": "ar", "name": "Arabic", "direction": "rtl"},
            {"code": "de", "name": "German", "direction": "ltr"}
        ]
    }
