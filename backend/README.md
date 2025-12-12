# Backend - Physical AI & Humanoid Robotics Book

FastAPI backend providing RAG chatbot, personalization, and translation services for the AI-native textbook.

## Features

- **RAG Chatbot**: Two-mode Q&A system (book-wide and selection-based)
- **Personalization**: Content adaptation based on user hardware and experience
- **Translation**: Multi-language support (EN, UR, FR, AR, DE) with caching
- **Vector Search**: Qdrant for semantic search
- **Database**: Neon Serverless Postgres for user data
- **LLM Integration**: OpenAI GPT-4 and embeddings

## Architecture

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration and settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── alembic/               # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 20250101_0000_001_initial_schema.py
├── models/                # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py            # User profiles
│   └── content.py         # Reading progress, RAG logs, translation cache
├── services/              # Business logic
│   ├── qdrant_service.py  # Vector database operations
│   └── embedding_service.py # OpenAI embeddings
├── api/                   # API endpoints
│   ├── rag/
│   │   ├── book_qa.py     # Book-wide Q&A
│   │   └── selection_qa.py # Selection-based Q&A
│   ├── personalization/
│   │   ├── user_profile.py # User profile CRUD
│   │   └── content_adapter.py # Content adaptation
│   └── translation/
│       └── translate.py   # Translation with caching
└── scripts/
    └── generate_embeddings.py # Embed docs and upload to Qdrant
```

## Setup

### 1. Prerequisites

- Python 3.11+
- PostgreSQL (Neon Serverless or local)
- Qdrant Cloud account (or local instance)
- OpenAI API key

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:

```env
# Qdrant Vector Database
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=physical-ai-book

# Neon Serverless Postgres
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb

# OpenAI API
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4-turbo-preview

# App Settings
APP_NAME="Physical AI Book API"
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.github.io"]
```

### 4. Initialize Database

Run Alembic migrations to create tables:

```bash
alembic upgrade head
```

This creates:
- `user_profiles` - User hardware, experience, preferences
- `reading_progress` - Chapter completion tracking
- `rag_query_logs` - Chatbot analytics
- `translation_cache` - Cached translations

### 5. Generate Embeddings

Embed all markdown files and upload to Qdrant:

```bash
python -m scripts.generate_embeddings
```

This will:
1. Scan `docs/` directory for markdown files
2. Chunk content by sections
3. Generate embeddings using OpenAI
4. Upload to Qdrant with metadata

### 6. Run Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: http://localhost:8000

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Endpoints

### RAG (Retrieval-Augmented Generation)

#### Book-wide Q&A
```bash
POST /api/rag/book-qa
Content-Type: application/json

{
  "query": "What is ROS 2?",
  "user_id": "uuid-optional"
}
```

Response:
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is...",
  "sources": [
    {"section_id": "modules/ros2/index", "score": 0.92},
    {"section_id": "foundations/index", "score": 0.85}
  ],
  "response_time_ms": 1243
}
```

#### Selection-based Q&A
```bash
POST /api/rag/selection-qa
Content-Type: application/json

{
  "query": "What does this mean?",
  "selected_text": "Quality of Service (QoS) policies...",
  "user_id": "uuid-optional"
}
```

### Translation

#### Translate Section
```bash
POST /api/translation/translate
Content-Type: application/json

{
  "section_id": "modules/ros2/index",
  "target_language": "ur"
}
```

Response:
```json
{
  "translated_content": "# ROS 2: روبوٹک اعصابی نظام\n\n...",
  "cache_hit": false,
  "translation_time_ms": 3456
}
```

#### Supported Languages
```bash
GET /api/translation/supported-languages
```

Response:
```json
{
  "languages": [
    {"code": "en", "name": "English", "direction": "ltr"},
    {"code": "ur", "name": "Urdu", "direction": "rtl"},
    {"code": "fr", "name": "French", "direction": "ltr"},
    {"code": "ar", "name": "Arabic", "direction": "rtl"},
    {"code": "de", "name": "German", "direction": "ltr"}
  ]
}
```

### Personalization

#### Create User Profile
```bash
POST /api/personalization/profile
Content-Type: application/json

{
  "email": "user@example.com",
  "hardware": {
    "has_rtx_gpu": true,
    "has_jetson": false,
    "jetson_model": "none",
    "robot_type": "none",
    "has_realsense": false,
    "has_lidar": false
  },
  "experience": {
    "ros2": "beginner",
    "ml": "intermediate",
    "robotics": "beginner",
    "simulation": "none"
  },
  "preferences": {
    "language": "en",
    "theme": "dark"
  }
}
```

#### Adapt Content
```bash
POST /api/personalization/adapt-content
Content-Type: application/json

{
  "section_id": "modules/isaac/index",
  "user_id": "uuid"
}
```

Response:
```json
{
  "section_id": "modules/isaac/index",
  "original_length": 5432,
  "adapted_length": 6789,
  "adaptations": [
    {
      "position": "after",
      "target_heading": "Hardware Requirements",
      "content": "### ☁️ Cloud GPU Alternative...",
      "reason": "User has no RTX GPU"
    },
    {
      "position": "before",
      "target_heading": null,
      "content": "> 📚 New to ROS 2?...",
      "reason": "User is ROS 2 beginner"
    }
  ],
  "adapted_content": "..."
}
```

## Database Schema

### user_profiles

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | String | Unique email |
| has_rtx_gpu | Boolean | RTX GPU availability |
| has_jetson | Boolean | Jetson device |
| jetson_model | Enum | nano/xavier_nx/agx_xavier/orin_nano/agx_orin |
| robot_type | Enum | turtlebot3/kobuki/jetbot/etc. |
| has_realsense | Boolean | RealSense camera |
| has_lidar | Boolean | LiDAR sensor |
| ros2_experience | Enum | none/beginner/intermediate/advanced/expert |
| ml_experience | Enum | Experience level |
| robotics_experience | Enum | Experience level |
| simulation_experience | Enum | Experience level |
| preferred_language | Enum | en/ur/fr/ar/de |
| theme | Enum | light/dark/auto |

### reading_progress

Tracks user progress through chapters.

### rag_query_logs

Logs all chatbot queries for analytics.

### translation_cache

Caches translations using SHA-256 content hash for automatic invalidation.

## Services

### Qdrant Service

Vector database operations:
- `create_collection_if_not_exists()` - Initialize collection
- `upsert_chunks(chunks)` - Upload embeddings
- `search(query_vector, top_k, filters)` - Semantic search

### Embedding Service

OpenAI embedding generation:
- `embed_query(text)` - Single query embedding
- `generate_embeddings_batch(texts)` - Batch embeddings
- `compute_content_hash(content)` - SHA-256 hash

## Personalization Rules

Content adaptations based on user profile:

| Condition | Adaptation |
|-----------|------------|
| No RTX GPU | Cloud GPU alternatives (Colab, Paperspace, AWS) |
| No Jetson | Simulation-first workflow |
| Has Jetson | Jetson optimization tips (nvpmodel, TensorRT) |
| No Robot | Simulation testing strategies |
| Has Robot | Robot-specific integration guide |
| ROS 2 Beginner | Prerequisites and basic tutorials |
| ROS 2 Expert | Research papers and advanced topics |
| ML Beginner | Simplified ML concepts |
| ML Expert | Optimization techniques (quantization, pruning) |

## Development

### Run Tests
```bash
pytest tests/
```

### Linting
```bash
ruff check .
black .
```

### Type Checking
```bash
mypy .
```

### Update Database Schema

After modifying models:
```bash
# Auto-generate migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

### Re-generate Embeddings

After updating content:
```bash
python -m scripts.generate_embeddings
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=false` in `.env`
- [ ] Set `ENVIRONMENT=production`
- [ ] Update `CORS_ORIGINS` to production domain
- [ ] Use production database URL
- [ ] Rotate API keys
- [ ] Enable HTTPS
- [ ] Set up monitoring (health check endpoint)
- [ ] Configure rate limiting
- [ ] Set up logging aggregation

### Deploy to Cloud

Example with Google Cloud Run:
```bash
# Build container
docker build -t physical-ai-book-api .

# Push to registry
docker tag physical-ai-book-api gcr.io/PROJECT_ID/physical-ai-book-api
docker push gcr.io/PROJECT_ID/physical-ai-book-api

# Deploy
gcloud run deploy physical-ai-book-api \
  --image gcr.io/PROJECT_ID/physical-ai-book-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "DATABASE_URL=...,OPENAI_API_KEY=..."
```

## Cost Estimates

### Free Tier Limits

- **Qdrant Cloud**: 1GB storage (free)
- **Neon Postgres**: 512MB storage (free)
- **OpenAI**:
  - Embeddings: ~$0.13 per 1M tokens
  - GPT-4 Turbo: ~$10 per 1M input tokens
  - Translation cache reduces costs by 80-90%

### Monthly Costs (Estimate)

Assuming 1,000 users, 10,000 queries/month:

- Qdrant: $0 (free tier)
- Neon: $0 (free tier)
- OpenAI Embeddings (one-time): ~$5
- OpenAI Chat: ~$20-50/month
- **Total: $20-50/month**

## Troubleshooting

### Qdrant Connection Failed
- Check `QDRANT_URL` and `QDRANT_API_KEY`
- Verify cluster is running
- Check firewall rules

### Database Connection Error
- Verify `DATABASE_URL` format
- Check Neon instance is active
- Run `alembic upgrade head`

### OpenAI Rate Limit
- Implement request queuing
- Use batch endpoints
- Consider caching responses

### Slow Embeddings
- Use batch processing (done in script)
- Consider pre-generating embeddings
- Cache frequently accessed embeddings

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/yourusername/ai-humanoid-robotics-as/issues
- Documentation: https://yourdomain.github.io/ai-humanoid-robotics-as/
