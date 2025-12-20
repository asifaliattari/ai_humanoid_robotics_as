"""
Selection-based Q&A endpoint for RAG chatbot
Answers questions about user-highlighted text (no vector search)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time
import logging
import uuid
from openai import OpenAI

from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class SelectionQARequest(BaseModel):
    """Request body for selection-based Q&A"""
    selected_text: str = Field(..., min_length=1, max_length=5000, description="Text highlighted by user")
    query: str = Field(..., min_length=1, max_length=500, description="Question about selected text")
    user_id: Optional[str] = Field(None, description="Optional user ID")


class SelectionQAResponse(BaseModel):
    """Response for selection-based Q&A"""
    answer: str
    query_id: str


@router.post("/selection-qa", response_model=SelectionQAResponse, tags=["RAG"])
async def selection_based_qa(request: SelectionQARequest):
    """
    Answer questions about user-highlighted text

    Process:
    1. Use selected_text as direct context (no vector search)
    2. Generate answer using LLM

    Use cases:
    - "Explain this in simpler terms"
    - "Can you give an example?"
    - "What does this mean?"
    """
    start_time = time.time()

    try:
        # Generate answer using OpenAI
        logger.info(f"Answering question about selected text (length: {len(request.selected_text)})")

        try:
            client = OpenAI(api_key=settings.openai_api_key)
        except Exception as e:
            logger.error(f"OpenAI client error: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI service temporarily unavailable. Please check configuration."
            )

        system_prompt = """You are a helpful teaching assistant for the Physical AI & Humanoid Robotics textbook.
Answer questions about the provided text excerpt.
Provide clear, simple explanations suitable for students.
Use analogies and examples when helpful.
Keep your answers concise but informative."""

        user_prompt = f"""Text excerpt:
\"\"\"
{request.selected_text}
\"\"\"

Student question: {request.query}

Answer:"""

        completion = client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=min(settings.openai_max_tokens, 1000),
            temperature=0.7,
        )

        answer = completion.choices[0].message.content

        response_time = int((time.time() - start_time) * 1000)
        logger.info(f"Selection-based Q&A completed in {response_time}ms")

        return SelectionQAResponse(
            answer=answer,
            query_id=str(uuid.uuid4())
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in selection_based_qa: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
