"""
Check if embeddings exist in Qdrant
"""
import sys
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from services.qdrant_service import qdrant_service

try:
    # Get collection info
    collection_info = qdrant_service.client.get_collection(qdrant_service.collection_name)

    print("=" * 60)
    print("QDRANT COLLECTION STATUS")
    print("=" * 60)
    print(f"Collection name: {collection_info.config.params.vectors.size}")
    print(f"Total points (embeddings): {collection_info.points_count}")
    print()

    if collection_info.points_count == 0:
        print("❌ NO EMBEDDINGS FOUND!")
        print()
        print("You need to generate embeddings:")
        print("  python -m scripts.generate_embeddings")
        print()
    else:
        print(f"✅ {collection_info.points_count} embeddings found!")
        print()

        # Test search
        from services.embedding_service import embedding_service
        test_query = "What is ROS 2?"
        print(f"Testing search with: '{test_query}'")
        query_embedding = embedding_service.embed_query(test_query)
        results = qdrant_service.search(query_embedding, top_k=3)

        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Section: {result['section_id']}")
            print(f"   Score: {result['score']:.3f}")
            print(f"   Preview: {result['content'][:100]}...")

    print()
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Make sure:")
    print("1. QDRANT_URL is correct in .env")
    print("2. QDRANT_API_KEY is correct in .env")
    print("3. Collection exists (run generate_embeddings.py)")
