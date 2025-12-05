"""
Main FastAPI application for Physical AI & Humanoid Robotics Book
Provides RAG chatbot, personalization, and translation services
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from contextlib import asynccontextmanager

from config import settings

# Import routers (will create these files next)
# from api.rag import book_qa, selection_qa
# from api.personalization import user_profile, content_adapter
# from api.translation import translate

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")

    # Initialize connections
    # TODO: Initialize Qdrant client
    # TODO: Initialize Neon Postgres connection pool
    # TODO: Verify OpenAI API key

    yield

    # Shutdown
    logger.info("Shutting down application")
    # TODO: Close database connections
    # TODO: Close Qdrant client


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-native backend for Physical AI & Humanoid Robotics textbook",
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
        "message": "Physical AI & Humanoid Robotics Book API",
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "Documentation disabled in production",
        "endpoints": {
            "health": "/health",
            "rag": {
                "book_qa": "/api/rag/book-qa",
                "selection_qa": "/api/rag/selection-qa",
            },
            "personalization": {
                "profile": "/api/personalization/profile",
                "adapt_content": "/api/personalization/adapt-content",
            },
            "translation": {
                "translate": "/api/translation/translate",
                "supported_languages": "/api/translation/supported-languages",
            },
        },
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include routers (uncomment after creating router files)
# app.include_router(book_qa.router, prefix="/api/rag", tags=["RAG"])
# app.include_router(selection_qa.router, prefix="/api/rag", tags=["RAG"])
# app.include_router(user_profile.router, prefix="/api/personalization", tags=["Personalization"])
# app.include_router(content_adapter.router, prefix="/api/personalization", tags=["Personalization"])
# app.include_router(translate.router, prefix="/api/translation", tags=["Translation"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
