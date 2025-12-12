"""
Simple FastAPI app - NO DATABASE REQUIRED
Just RAG chatbot with OpenAI + Qdrant
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from contextlib import asynccontextmanager

from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-native backend for Physical AI & Humanoid Robotics textbook (Simple Version)",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {process_time:.2f}s "
        f"with status {response.status_code}"
    )
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Physical AI & Humanoid Robotics Book API (Simple Version)",
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "Documentation disabled in production",
        "endpoints": {
            "health": "/health",
            "rag": {
                "book_qa": "/api/rag/book-qa",
            },
        },
    }


# Simple RAG endpoint (no database)
from pydantic import BaseModel
from typing import List, Optional
from services.qdrant_service import qdrant_service
from services.embedding_service import embedding_service
from openai import OpenAI

client = OpenAI(api_key=settings.openai_api_key)


class BookQARequest(BaseModel):
    query: str
    user_id: Optional[str] = None


class Source(BaseModel):
    section_id: str
    score: float


class BookQAResponse(BaseModel):
    answer: str
    sources: List[Source]
    response_time_ms: int


@app.post("/api/rag/book-qa", response_model=BookQAResponse, tags=["RAG"])
async def book_wide_qa(request: BookQARequest):
    """
    Ask questions about the entire book using RAG
    """
    import time as time_module
    start_time = time_module.time()

    try:
        # 1. Embed the query
        query_embedding = embedding_service.embed_query(request.query)

        # 2. Search Qdrant for relevant chunks
        search_results = qdrant_service.search(
            query_vector=query_embedding,
            top_k=settings.rag_top_k_results,
        )

        if not search_results:
            return BookQAResponse(
                answer="I couldn't find relevant information in the book to answer your question. Try rephrasing or ask about a different topic.",
                sources=[],
                response_time_ms=int((time_module.time() - start_time) * 1000)
            )

        # 3. Build context from retrieved chunks
        context_parts = []
        sources = []

        for i, chunk in enumerate(search_results[:5], 1):
            context_parts.append(f"[Source {i}: {chunk['section_id']}]\n{chunk['content']}")
            sources.append(Source(
                section_id=chunk['section_id'],
                score=chunk['score']
            ))

        context = "\n\n".join(context_parts)

        # 4. Generate answer using OpenAI
        system_prompt = """You are an AI teaching assistant for a Physical AI & Humanoid Robotics textbook.

Your role:
- Answer questions based ONLY on the provided context from the book
- Be clear, accurate, and educational
- If the context doesn't contain the answer, say so
- Cite sources by mentioning the section names

Style:
- Use simple language
- Provide examples when helpful
- Be encouraging and supportive"""

        user_prompt = f"""Based on the following excerpts from the textbook, please answer this question:

Question: {request.query}

Context from the book:
{context}

Answer:"""

        completion = client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=settings.openai_max_tokens,
        )

        answer = completion.choices[0].message.content

        response_time = int((time_module.time() - start_time) * 1000)

        return BookQAResponse(
            answer=answer,
            sources=sources,
            response_time_ms=response_time
        )

    except Exception as e:
        logger.error(f"Error in book_wide_qa: {e}")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main-simple:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
