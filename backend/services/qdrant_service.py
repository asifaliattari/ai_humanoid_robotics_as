"""
Qdrant vector database service for RAG embeddings
Handles collection creation, embedding storage, and similarity search
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Any, Optional
import logging

from config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database"""

    def __init__(self):
        """Initialize Qdrant client and ensure collection exists"""
        self._client = None
        self.collection_name = settings.qdrant_collection_name
        self.embedding_dimension = 1536  # OpenAI text-embedding-3-small
        self._initialized = False
        self._initialization_error = None

    def _ensure_initialized(self):
        """Lazy initialization - only connect when first used"""
        if self._initialized:
            return
        
        if self._initialization_error:
            raise RuntimeError(f"Qdrant service initialization failed: {self._initialization_error}")
        
        try:
            self._client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )
            # Ensure collection exists
            self._ensure_collection()
            self._initialized = True
            logger.info("Qdrant service initialized successfully")
        except Exception as e:
            self._initialization_error = str(e)
            logger.error(f"Failed to initialize Qdrant service: {e}")
            raise RuntimeError(f"Qdrant service not available: {e}")

    @property
    def client(self):
        """Get Qdrant client, initializing if necessary"""
        self._ensure_initialized()
        return self._client

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self._client.get_collections().collections
            collection_exists = any(c.name == self.collection_name for c in collections)

            if not collection_exists:
                logger.info(f"Creating Qdrant collection: {self.collection_name}")
                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dimension,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")

        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise

    def upsert_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Upsert document chunks with embeddings into Qdrant

        Args:
            chunks: List of dicts with keys:
                - id: str (unique chunk ID)
                - embedding: List[float] (1536-dimensional vector)
                - metadata: Dict with module, section, difficulty, language, etc.

        Returns:
            bool: Success status
        """
        try:
            points = [
                PointStruct(
                    id=chunk["id"],
                    vector=chunk["embedding"],
                    payload=chunk["metadata"]
                )
                for chunk in chunks
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Upserted {len(chunks)} chunks to Qdrant")
            return True

        except Exception as e:
            logger.error(f"Error upserting chunks: {e}")
            return False

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity

        Args:
            query_vector: Query embedding (1536-dimensional)
            top_k: Number of results to return
            filters: Optional filters on metadata (e.g., {"module": "ros2", "language": "en"})

        Returns:
            List of search results with scores and metadata
        """
        try:
            # Build filter conditions
            query_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
                if conditions:
                    query_filter = Filter(must=conditions)

            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=query_filter,
            )

            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "metadata": hit.payload,
                    "section_id": hit.payload.get("section_id"),
                    "content": hit.payload.get("content"),
                    "module": hit.payload.get("module"),
                    "difficulty": hit.payload.get("difficulty"),
                    "language": hit.payload.get("language"),
                })

            logger.info(f"Found {len(results)} similar chunks")
            return results

        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            return []

    def delete_by_section(self, section_id: str) -> bool:
        """
        Delete all chunks for a specific section
        Useful when content is updated

        Args:
            section_id: Section identifier (e.g., "modules/ros2/index")

        Returns:
            bool: Success status
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="section_id",
                            match=MatchValue(value=section_id)
                        )
                    ]
                )
            )
            logger.info(f"Deleted chunks for section: {section_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting chunks: {e}")
            return False

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": info.status,
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}


# Global instance
qdrant_service = QdrantService()
