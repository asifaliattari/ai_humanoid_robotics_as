# Backend - Physical AI & Humanoid Robotics Book

FastAPI backend providing RAG chatbot and authentication services for the AI-native textbook.

## Features

- **RAG Chatbot**: Q&A system powered by vector search
- **User Authentication**: JWT-based login and registration
- **Vector Search**: Qdrant for semantic search
- **Database**: SQLite (local) / Neon Postgres (production)
- **LLM Integration**: OpenAI GPT-4

## Architecture

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration and settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── models/                # SQLAlchemy models
│   ├── __init__.py
│   ├── auth.py            # User authentication model
│   └── user.py            # User profiles
├── services/              # Business logic
│   ├── qdrant_service.py  # Vector database operations
│   └── embedding_service.py # OpenAI embeddings
├── api/                   # API endpoints
│   ├── auth/
│   │   └── auth.py        # Login, register, JWT
│   └── rag/
│       ├── book_qa.py     # Book-wide Q&A
│       └── selection_qa.py # Selection-based Q&A
└── scripts/
    └── generate_embeddings.py # Embed docs and upload to Qdrant
```

## Setup

### 1. Prerequisites

- Python 3.11+
- Qdrant Cloud account (or local instance)
- OpenAI API key

### 2. Install Dependencies

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:

```env
# Database
DATABASE_URL=sqlite:///./database.db

# Authentication
AUTH_SECRET=your-secret-key-min-32-characters

# Qdrant Vector Database
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key

# OpenAI API
OPENAI_API_KEY=sk-...
```

### 4. Generate Embeddings

Embed all markdown files and upload to Qdrant:

```bash
python -m scripts.generate_embeddings
```

### 5. Run Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: http://localhost:8000

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Endpoints

### Authentication

#### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "User Name"
}
```

#### Login
```bash
POST /api/auth/login-json
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

Response:
```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer",
  "user_id": "uuid",
  "email": "user@example.com"
}
```

#### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer <token>
```

### RAG Chatbot

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
    {"section_id": "modules/ros2/index", "score": 0.92}
  ],
  "query_id": "uuid"
}
```

## Deployment

### Hugging Face Spaces (Current)

The backend is deployed to Hugging Face Spaces:
- URL: https://asifaliastolixgen-physical-ai-book-api.hf.space

To update:
```bash
cd hf-deploy
git add .
git commit -m "Update"
git push
```

### Environment Variables (HF Secrets)

Set these in Space Settings → Repository secrets:
- `OPENAI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `AUTH_SECRET`

## Development

### Re-generate Embeddings

After updating content:
```bash
python -m scripts.generate_embeddings
```

## License

MIT License
