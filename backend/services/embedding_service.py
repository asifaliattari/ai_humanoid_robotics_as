"""
OpenAI embedding service for generating vector embeddings
Used by RAG system to embed both documents and queries
"""
from openai import OpenAI
from typing import List, Union
import logging
import hashlib

from config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating OpenAI embeddings"""

    def __init__(self):
        """Initialize OpenAI client"""
        self._client = None
        self.model = settings.openai_embedding_model
        self.embedding_dimension = 1536  # text-embedding-3-small
        self._initialized = False
        self._initialization_error = None

    def _ensure_initialized(self):
        """Lazy initialization - only connect when first used"""
        if self._initialized:
            return
        
        if self._initialization_error:
            raise RuntimeError(f"Embedding service initialization failed: {self._initialization_error}")
        
        try:
            self._client = OpenAI(api_key=settings.openai_api_key)
            self._initialized = True
            logger.info("Embedding service initialized successfully")
        except Exception as e:
            self._initialization_error = str(e)
            logger.error(f"Failed to initialize Embedding service: {e}")
            raise RuntimeError(f"Embedding service not available: {e}")

    @property
    def client(self):
        """Get OpenAI client, initializing if necessary"""
        self._ensure_initialized()
        return self._client

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Input text to embed

        Returns:
            List of floats (1536-dimensional vector)
        """
        try:
            self._ensure_initialized()
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding for text of length {len(text)}")
            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch
        More efficient than calling generate_embedding multiple times

        Args:
            texts: List of input texts

        Returns:
            List of embeddings (each is 1536-dimensional vector)
        """
        try:
            # OpenAI allows up to 2048 inputs per batch
            # If we have more, we need to split
            batch_size = 2048
            all_embeddings = []

            self._ensure_initialized()
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )
                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)

            logger.info(f"Generated {len(all_embeddings)} embeddings in batch")
            return all_embeddings

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

    @staticmethod
    def compute_content_hash(text: str) -> str:
        """
        Compute SHA-256 hash of content for caching

        Args:
            text: Input text

        Returns:
            Hex string of SHA-256 hash
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a search query
        Convenience method that adds query-specific preprocessing if needed

        Args:
            query: Search query text

        Returns:
            Query embedding vector
        """
        # Could add query-specific preprocessing here
        # For now, just use standard embedding
        return self.generate_embedding(query)


# Global instance
embedding_service = EmbeddingService()
