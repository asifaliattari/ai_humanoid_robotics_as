"""
Book-wide Q&A endpoint for RAG chatbot
Searches entire book content using vector similarity
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import time
import logging
import uuid
from openai import OpenAI

from config import settings
from services.qdrant_service import qdrant_service
from services.embedding_service import embedding_service

logger = logging.getLogger(__name__)
router = APIRouter()


# -------------------------------
# Request / Response Models
# -------------------------------

class BookQARequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    user_id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


class SourceChunk(BaseModel):
    section_id: str
    title: str
    relevance_score: float
    excerpt: str


class BookQAResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    query_id: str


# -------------------------------
# Main Endpoint
# -------------------------------

@router.post("/book-qa", response_model=BookQAResponse, tags=["RAG"])
async def book_wide_qa(request: BookQARequest):
    """
    Answer questions using entire book content via vector search
    """

    start_time = time.time()

    try:
        # Step 1: Embed query
        logger.info(f"Embedding query: {request.query[:100]}...")
        try:
            query_embedding = embedding_service.embed_query(request.query)
        except RuntimeError as e:
            logger.error(f"Embedding service error: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI service temporarily unavailable. Please check configuration."
            )

        # Step 2: Search Qdrant
        logger.info("Searching Qdrant for similar chunks")
        
        try:
            search_results = qdrant_service.search(
                query_vector=query_embedding,
                top_k=settings.rag_top_k_results,
                filters=request.filters
            )
        except RuntimeError as e:
            logger.error(f"Qdrant service error: {e}")
            raise HTTPException(
                status_code=503,
                detail="Search service temporarily unavailable. Please check configuration."
            )

        # ---- Friendly fallback: No results at all ----
        if not search_results:
            fallback_answer = (
                "I couldn't find any relevant information about this question in the textbook.\n\n"
                "This book covers Physical AI & Humanoid Robotics (ROS 2, Gazebo, Isaac Sim, VLA).\n"
                "Try asking something related to these topics."
            )
            return BookQAResponse(
                answer=fallback_answer,
                sources=[],
                query_id=str(uuid.uuid4())
            )

        # Step 2b: Filter by similarity threshold
        relevant_chunks = [
            chunk for chunk in search_results
            if chunk["score"] >= settings.rag_similarity_threshold
        ]

        if not relevant_chunks:
            fallback_answer = (
                "I found some text, but nothing confidently relevant enough to answer.\n\n"
                "Try rephrasing or asking something more directly related to the book content."
            )
            return BookQAResponse(
                answer=fallback_answer,
                sources=[],
                query_id=str(uuid.uuid4())
            )

        # Step 3: Build context
        context = "\n\n".join(
            f"[Source: {chunk['section_id']}]\n{chunk['content']}"
            for chunk in relevant_chunks
        )

        # Step 4: Generate LLM response
        try:
            client = OpenAI(api_key=settings.openai_api_key)
        except Exception as e:
            logger.error(f"OpenAI client error: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI service temporarily unavailable. Please check configuration."
            )

        system_prompt = """
You are an expert assistant for the Physical AI & Humanoid Robotics textbook.
Answer questions using ONLY the provided context from the book.

Important facts about this book:
- The book content is in English.
- The book covers: ROS 2, Digital Twin (Gazebo), NVIDIA Isaac, and Vision-Language-Action (VLA) systems.
- Users can create an account to save their progress.

Language handling:
- If the user asks in Roman Urdu (Urdu written in English letters like "yeh kya hai?"), respond in Roman Urdu.
- If the user asks in English, respond in English.
- Match the user's language style.

If the answer is not in the context, say:
"I don't have enough information in the book to answer that." (or in Roman Urdu if they asked in Roman Urdu)
"""

        user_prompt = f"""
Context from the book:

{context}

Question: {request.query}

Answer:
"""

        completion = client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=settings.openai_max_tokens,
            temperature=0.7,
        )

        answer = completion.choices[0].message.content

        # Step 5: Prepare sources
        sources = [
            SourceChunk(
                section_id=chunk["section_id"],
                title=chunk["metadata"].get("title", chunk["section_id"]),
                relevance_score=round(chunk["score"], 3),
                excerpt=(chunk["content"][:200] + "...")
                if len(chunk["content"]) > 200 else chunk["content"]
            )
            for chunk in relevant_chunks
        ]

        # Step 6: Send response
        logger.info(f"Book-wide Q&A completed in {int((time.time() - start_time) * 1000)}ms")

        return BookQAResponse(
            answer=answer,
            sources=sources,
            query_id=str(uuid.uuid4())
        )

    except Exception as e:
        logger.error(f"Error in book_wide_qa: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
