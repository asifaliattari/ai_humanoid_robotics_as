# Setup Guide - Physical AI & Humanoid Robotics Textbook

Complete setup guide for the AI-native textbook platform with RAG chatbot, personalization, and multi-language translation.

## Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai_humanoid_robotics_as.git
cd ai_humanoid_robotics_as

# 2. Configure backend
cd backend
cp .env.example .env
# Edit .env with your API keys (see below)

# 3. Install and run with Docker Compose
docker-compose up -d

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

## Prerequisites

### Required Accounts (All Free Tier Available)

1. **Qdrant Cloud** (Vector Database)
   - Sign up: https://cloud.qdrant.io/
   - Free tier: 1GB storage
   - Get: Cluster URL + API Key

2. **Neon** (Serverless Postgres)
   - Sign up: https://neon.tech/
   - Free tier: 512MB storage
   - Get: Database URL

3. **OpenAI** (LLM & Embeddings)
   - Sign up: https://platform.openai.com/
   - Get: API Key
   - Cost: ~$20-50/month for 1,000 users

### Required Software

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Docker** (optional, recommended)
- **Git**

## Step 1: Get API Keys

### Qdrant Cloud Setup

1. Go to https://cloud.qdrant.io/ and sign up
2. Create a new cluster (free tier)
3. Copy **Cluster URL** (e.g., `https://xxx.qdrant.tech`)
4. Create API key → Copy it

### Neon Postgres Setup

1. Go to https://neon.tech/ and sign up
2. Create a new project
3. Click "Connection string"
4. Copy the **PostgreSQL connection string**
   ```
   postgresql://user:password@ep-xxx.aws.neon.tech/neondb?sslmode=require
   ```

### OpenAI API Setup

1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy key (starts with `sk-`)
4. Add $5-10 credit to your account

## Step 2: Backend Setup

### Option A: Docker (Recommended)

```bash
cd backend

# 1. Configure environment
cp .env.example .env
nano .env  # Or use any text editor

# Fill in:
# QDRANT_URL=https://your-cluster.qdrant.tech
# QDRANT_API_KEY=your-qdrant-key
# DATABASE_URL=postgresql://...
# OPENAI_API_KEY=sk-...

# 2. Build and run
docker build -t physical-ai-backend .
docker run -p 8000:8000 --env-file .env physical-ai-backend

# API will be available at http://localhost:8000
```

### Option B: Manual Setup

```bash
cd backend

# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Initialize database
alembic upgrade head

# 5. Generate embeddings
python -m scripts.generate_embeddings

# 6. Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verify backend is running:
- Open http://localhost:8000/docs
- Try the `/health` endpoint
- Should return: `{"status": "healthy", ...}`

## Step 3: Frontend Setup

### Option A: Docker Compose (Easiest)

```bash
# From project root
docker-compose up -d

# This starts both backend and frontend
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Option B: Manual Setup

```bash
# From project root

# 1. Install dependencies
npm install

# 2. Configure backend URL (optional)
# Create .env in project root:
echo "BACKEND_URL=http://localhost:8000" > .env

# 3. Run development server
npm start

# Site will open at http://localhost:3000
```

## Step 4: Verify Everything Works

### Test Backend APIs

```bash
# Health check
curl http://localhost:8000/health

# Get supported languages
curl http://localhost:8000/api/translation/supported-languages

# Test RAG (requires embeddings generated)
curl -X POST http://localhost:8000/api/rag/book-qa \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

### Test Frontend

1. Open http://localhost:3000
2. Navigate to any module (e.g., **Modules > ROS 2**)
3. Try:
   - **Language toggle**: Click "Urdu" → Should translate page
   - **Personalize**: Sign in → Click "Personalize for Me"
   - **Chat**: Click floating chat button → Ask "What is ROS 2?"

## Step 5: Generate Embeddings

The RAG chatbot requires embeddings to be generated from your content:

```bash
cd backend
python -m scripts.generate_embeddings

# This will:
# 1. Scan docs/ directory for markdown files
# 2. Chunk content by sections
# 3. Generate embeddings using OpenAI (~$5 one-time cost)
# 4. Upload to Qdrant

# Output:
# ✅ Found 10 markdown files
# ✅ Generated 234 chunks
# ✅ Uploaded to Qdrant
```

**Note**: Run this script whenever you update book content.

## Configuration

### Backend Environment Variables

Edit `backend/.env`:

```env
# === Required ===
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-key
DATABASE_URL=postgresql://user:pass@host/db
OPENAI_API_KEY=sk-your-key

# === Optional (with defaults) ===
QDRANT_COLLECTION_NAME=physical-ai-book
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4-turbo-preview
APP_NAME=Physical AI Book API
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:3000"]
RAG_CHUNK_SIZE=1000
RAG_TOP_K_RESULTS=5
```

### Frontend Configuration

Edit `docusaurus.config.ts`:

```typescript
// Update these for your deployment
const config: Config = {
  url: 'https://yourusername.github.io',
  baseUrl: '/ai_humanoid_robotics_as/',
  organizationName: 'yourusername',
  projectName: 'ai_humanoid_robotics_as',

  // Backend API URL
  customFields: {
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
  },
};
```

## Deployment

### Deploy Backend (Google Cloud Run)

```bash
cd backend

# 1. Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/physical-ai-backend

# 2. Deploy
gcloud run deploy physical-ai-backend \
  --image gcr.io/PROJECT_ID/physical-ai-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "QDRANT_URL=...,QDRANT_API_KEY=...,DATABASE_URL=...,OPENAI_API_KEY=..."

# Get deployed URL (e.g., https://physical-ai-backend-xxx.run.app)
```

### Deploy Frontend (GitHub Pages)

```bash
# 1. Update docusaurus.config.ts with your GitHub username

# 2. Build
npm run build

# 3. Deploy
GIT_USER=<Your GitHub username> npm run deploy

# Site will be live at:
# https://yourusername.github.io/ai_humanoid_robotics_as/
```

### Update Frontend to Use Production Backend

```typescript
// src/components/TranslationToggle.tsx, etc.
const BACKEND_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-backend.run.app'
  : 'http://localhost:8000';

// Use BACKEND_URL in fetch calls
fetch(`${BACKEND_URL}/api/translation/translate`, ...)
```

## Database Migrations

### Create New Migration

```bash
cd backend

# After modifying models/
alembic revision --autogenerate -m "Add new field to user_profiles"

# Review generated migration in alembic/versions/

# Apply migration
alembic upgrade head
```

### Common Migration Commands

```bash
# Show current version
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Show SQL without executing
alembic upgrade head --sql
```

## Troubleshooting

### "Connection to Qdrant failed"

- Check `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Verify cluster is active in Qdrant dashboard
- Test connection: `curl -H "api-key: YOUR_KEY" https://your-cluster.qdrant.tech/collections`

### "Database connection error"

- Verify `DATABASE_URL` format:
  ```
  postgresql://user:password@host:5432/dbname?sslmode=require
  ```
- Check Neon project is active
- Run migrations: `alembic upgrade head`

### "OpenAI API rate limit exceeded"

- Check your OpenAI usage dashboard
- Add more credits to your account
- Reduce `RAG_TOP_K_RESULTS` to use fewer tokens

### "Embeddings generation failed"

- Ensure `docs/` directory exists and has .md files
- Check OpenAI API key is valid
- Verify Qdrant collection was created
- Check console output for specific error

### "React components not rendering"

- Ensure file extension is `.mdx` (not `.md`)
- Check component import path:
  ```tsx
  import BookPageWrapper from '@site/src/components/BookPageWrapper';
  ```
- Clear cache: `npm run clear && npm start`

### "CORS errors in browser console"

- Add your frontend URL to `CORS_ORIGINS` in backend `.env`:
  ```
  CORS_ORIGINS=["http://localhost:3000","https://yourusername.github.io"]
  ```
- Restart backend after changing `.env`

## Development Workflow

### Adding New Content

1. Create/edit markdown files in `docs/`
2. Use `.mdx` extension for pages with AI features
3. Wrap content with `<BookPageWrapper>`:
   ```mdx
   import BookPageWrapper from '@site/src/components/BookPageWrapper';

   <BookPageWrapper sectionId="modules/new-module/index">

   # Your Content Here

   </BookPageWrapper>
   ```
4. Regenerate embeddings:
   ```bash
   cd backend
   python -m scripts.generate_embeddings
   ```

### Testing Changes Locally

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
npm start

# Make changes, see live reload
```

### Committing Changes

```bash
git add .
git commit -m "feat: add new module on VLA systems"
git push origin main

# Deploy frontend
npm run deploy
```

## Cost Optimization

### Reduce OpenAI Costs

1. **Translation Caching**: Already implemented
   - First translation: ~$0.05
   - Cached translations: Free
   - Cache hit rate: 80-90%

2. **Reduce RAG Context**:
   ```env
   RAG_TOP_K_RESULTS=3  # Instead of 5
   RAG_CHUNK_SIZE=800   # Instead of 1000
   ```

3. **Use Cheaper Models**:
   ```env
   OPENAI_CHAT_MODEL=gpt-3.5-turbo  # $0.50/1M tokens vs $10/1M
   ```

### Monitor Usage

```sql
-- Check translation cache hit rate
SELECT
  COUNT(*) as total_translations,
  SUM(access_count) as cache_hits,
  (SUM(access_count)::float / COUNT(*)) as hit_rate
FROM translation_cache;

-- Check RAG query costs
SELECT
  DATE(created_at) as date,
  COUNT(*) as queries,
  AVG(response_time_ms) as avg_response_time
FROM rag_query_logs
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

## Performance Optimization

### Frontend

```bash
# Enable production build
npm run build
npm run serve

# Check bundle size
npx webpack-bundle-analyzer build/bundle-stats.json
```

### Backend

```bash
# Use production ASGI server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Enable caching
# Add Redis for session caching
```

## Support

### Getting Help

- **Documentation**: https://yourusername.github.io/ai_humanoid_robotics_as/
- **Issues**: https://github.com/yourusername/ai_humanoid_robotics_as/issues
- **Discussions**: https://github.com/yourusername/ai_humanoid_robotics_as/discussions

### Reporting Bugs

Include:
1. Error message (full stack trace)
2. Steps to reproduce
3. Environment (OS, Python version, Node version)
4. Backend logs (`uvicorn` output)
5. Browser console output

## Next Steps

- [ ] Complete your user profile (for personalization)
- [ ] Explore all modules with AI features
- [ ] Try the RAG chatbot on different topics
- [ ] Translate a page to your preferred language
- [ ] Share feedback and contribute!

---

**Ready to start learning Physical AI?** 🤖

Open http://localhost:3000 and begin your journey!
