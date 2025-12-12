"""
Generate embeddings for all book content and upload to Qdrant

This script:
1. Scans docs/ directory for markdown files
2. Chunks content by sections (## headings)
3. Generates embeddings using OpenAI
4. Uploads to Qdrant with metadata

Run: python -m scripts.generate_embeddings
"""
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Any
import hashlib
import logging
import uuid

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from config import settings
from services.qdrant_service import qdrant_service
from services.embedding_service import embedding_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ContentChunker:
    """Chunk markdown content by sections"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_sections(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract sections from markdown file

        Returns list of sections with metadata:
        - section_id: unique identifier
        - title: section heading
        - content: section text
        - level: heading level (1-6)
        - file_path: source file
        """
        sections = []

        # Split by headings (## or ###)
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        lines = content.split('\n')

        current_section = None
        current_content = []

        for line in lines:
            heading_match = re.match(heading_pattern, line)

            if heading_match:
                # Save previous section
                if current_section:
                    current_section['content'] = '\n'.join(current_content).strip()
                    if current_section['content']:  # Only add non-empty sections
                        sections.append(current_section)

                # Start new section
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                current_section = {
                    'title': title,
                    'level': level,
                    'file_path': file_path,
                }
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            current_section['content'] = '\n'.join(current_content).strip()
            if current_section['content']:
                sections.append(current_section)

        # Generate section IDs
        for i, section in enumerate(sections):
            # Create section_id from file path and heading
            path_slug = file_path.replace('\\', '/').replace('docs/', '').replace('.md', '')
            title_slug = re.sub(r'[^\w\s-]', '', section['title'].lower())
            title_slug = re.sub(r'[-\s]+', '-', title_slug)
            section['section_id'] = f"{path_slug}#{title_slug}"

        return sections

    def chunk_section(self, section: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Break large sections into smaller chunks

        If section content > chunk_size, split into overlapping chunks
        """
        content = section['content']

        if len(content) <= self.chunk_size:
            # Section small enough - return as-is
            return [{
                'section_id': section['section_id'],
                'chunk_id': f"{section['section_id']}-0",
                'content': content,
                'metadata': {
                    'title': section['title'],
                    'level': section['level'],
                    'file_path': section['file_path'],
                    'chunk_index': 0,
                    'total_chunks': 1
                }
            }]

        # Split into chunks with overlap
        chunks = []
        words = content.split()

        chunk_words = []
        chunk_index = 0

        for i, word in enumerate(words):
            chunk_words.append(word)
            current_length = len(' '.join(chunk_words))

            # Check if we've reached chunk_size
            if current_length >= self.chunk_size or i == len(words) - 1:
                chunk_content = ' '.join(chunk_words)

                chunks.append({
                    'section_id': section['section_id'],
                    'chunk_id': f"{section['section_id']}-{chunk_index}",
                    'content': chunk_content,
                    'metadata': {
                        'title': section['title'],
                        'level': section['level'],
                        'file_path': section['file_path'],
                        'chunk_index': chunk_index,
                        'total_chunks': -1  # Will update after
                    }
                })

                # Start new chunk with overlap
                overlap_words = chunk_words[-int(self.chunk_overlap / 5):]  # Approximate word count
                chunk_words = overlap_words
                chunk_index += 1

        # Update total_chunks
        for chunk in chunks:
            chunk['metadata']['total_chunks'] = len(chunks)

        return chunks


def extract_metadata_from_path(file_path: str) -> Dict[str, Any]:
    """Extract metadata from file path"""
    # Parse path: docs/foundations/index.md -> module=foundations
    parts = file_path.replace('\\', '/').split('/')

    metadata = {
        'language': 'en',  # All source content is English
        'difficulty': 'intermediate',  # Default
    }

    if len(parts) >= 2:
        if parts[1] == 'foundations':
            metadata['module'] = 'foundations'
            metadata['difficulty'] = 'beginner'
        elif parts[1] == 'modules':
            if len(parts) >= 3:
                metadata['module'] = parts[2]  # ros2, digital-twin, isaac, vla
                metadata['difficulty'] = 'intermediate'
        elif parts[1] == 'hardware':
            metadata['module'] = 'hardware'
            metadata['difficulty'] = 'beginner'
        elif parts[1] == 'capstone':
            metadata['module'] = 'capstone'
            metadata['difficulty'] = 'advanced'
        elif parts[1] == 'ai-features':
            metadata['module'] = 'ai-features'
            metadata['difficulty'] = 'advanced'
        elif parts[1] == 'meta':
            metadata['module'] = 'meta'
            metadata['difficulty'] = 'beginner'

    return metadata


def scan_docs_directory(docs_path: Path) -> List[Path]:
    """Recursively find all markdown files in docs/"""
    markdown_files = []

    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                file_path = Path(root) / file
                markdown_files.append(file_path)

    logger.info(f"Found {len(markdown_files)} markdown files")
    return markdown_files


def process_file(file_path: Path, chunker: ContentChunker) -> List[Dict[str, Any]]:
    """Process a single markdown file into chunks"""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract relative path
        relative_path = str(file_path.relative_to(file_path.parent.parent.parent))

        # Extract sections
        sections = chunker.extract_sections(content, relative_path)

        # Chunk each section
        all_chunks = []
        for section in sections:
            chunks = chunker.chunk_section(section)
            all_chunks.extend(chunks)

        # Add file-level metadata to each chunk
        file_metadata = extract_metadata_from_path(relative_path)
        for chunk in all_chunks:
            chunk['metadata'].update(file_metadata)

        logger.info(f"Processed {file_path.name}: {len(sections)} sections → {len(all_chunks)} chunks")
        return all_chunks

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return []


def main():
    """Main entry point"""
    logger.info("=== Starting embedding generation ===")

    # Step 1: Scan docs directory
    docs_path = backend_dir.parent / 'docs'
    if not docs_path.exists():
        logger.error(f"Docs directory not found: {docs_path}")
        sys.exit(1)

    markdown_files = scan_docs_directory(docs_path)

    if not markdown_files:
        logger.error("No markdown files found")
        sys.exit(1)

    # Step 2: Initialize services
    logger.info("Initializing Qdrant and embedding services...")

    # Collection is created automatically when qdrant_service is imported
    try:
        collection_info = qdrant_service.get_collection_info()
        logger.info(f"Qdrant collection '{settings.qdrant_collection_name}' ready")
        logger.info(f"Current points count: {collection_info.get('points_count', 0)}")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant: {e}")
        sys.exit(1)

    # Step 3: Process all files
    chunker = ContentChunker(
        chunk_size=settings.rag_chunk_size,
        chunk_overlap=settings.rag_chunk_overlap
    )

    all_chunks = []
    for file_path in markdown_files:
        chunks = process_file(file_path, chunker)
        all_chunks.extend(chunks)

    logger.info(f"Total chunks: {len(all_chunks)}")

    if not all_chunks:
        logger.error("No chunks generated")
        sys.exit(1)

    # Step 4: Generate embeddings
    logger.info("Generating embeddings...")

    try:
        # Extract content for embedding
        texts = [chunk['content'] for chunk in all_chunks]

        # Generate embeddings in batch
        embeddings = embedding_service.generate_embeddings_batch(texts)

        logger.info(f"Generated {len(embeddings)} embeddings")

        # Attach embeddings to chunks
        for chunk, embedding in zip(all_chunks, embeddings):
            chunk['embedding'] = embedding

    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        sys.exit(1)

    # Step 5: Upload to Qdrant
    logger.info("Uploading to Qdrant...")

    try:
        # Prepare chunks for Qdrant
        qdrant_chunks = [
            {
                'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk['chunk_id'])),  # Generate proper UUID
                'embedding': chunk['embedding'],
                'metadata': {
                    'section_id': chunk['section_id'],
                    'chunk_id': chunk['chunk_id'],
                    'content': chunk['content'],
                    **chunk['metadata']
                }
            }
            for chunk in all_chunks
        ]

        # Upload in batches
        batch_size = 100
        for i in range(0, len(qdrant_chunks), batch_size):
            batch = qdrant_chunks[i:i + batch_size]
            qdrant_service.upsert_chunks(batch)
            logger.info(f"Uploaded batch {i // batch_size + 1}/{(len(qdrant_chunks) + batch_size - 1) // batch_size}")

        logger.info(f"Successfully uploaded {len(qdrant_chunks)} chunks to Qdrant")

    except Exception as e:
        logger.error(f"Failed to upload to Qdrant: {e}")
        sys.exit(1)

    # Step 6: Verify
    logger.info("Verifying upload...")

    try:
        # Test search
        test_query = "What is ROS 2?"
        test_embedding = embedding_service.embed_query(test_query)
        results = qdrant_service.search(test_embedding, top_k=3)

        logger.info(f"Test search for '{test_query}' returned {len(results)} results")
        if results:
            logger.info(f"Top result: {results[0]['section_id']} (score: {results[0]['score']:.3f})")

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        sys.exit(1)

    logger.info("=== Embedding generation complete ===")
    logger.info(f"📊 Statistics:")
    logger.info(f"  Files processed: {len(markdown_files)}")
    logger.info(f"  Chunks created: {len(all_chunks)}")
    logger.info(f"  Embeddings generated: {len(embeddings)}")
    logger.info(f"  Qdrant collection: {settings.qdrant_collection_name}")


if __name__ == "__main__":
    main()
