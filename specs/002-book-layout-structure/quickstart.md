# Quickstart: Physical AI & Humanoid Robotics Book

This guide helps you set up the development environment for the Physical AI book (Docusaurus frontend + FastAPI backend).

## Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- Git
- (Optional) Docker for backend services

## Frontend Setup (Docusaurus Book)

### 1. Clone Repository

```bash
git clone https://github.com/asifaliattari/ai_humanoid_robotics_as.git
cd ai_humanoid_robotics_as
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Development Server

```bash
npm start
```

Site opens at `http://localhost:3000`.

### 4. Verify Module Structure

Navigate to:
- `/docs/intro` - Physical AI Foundations
- `/docs/module-1-ros2` - ROS 2 module
- `/docs/module-2-digital-twin` - Digital Twin module
- `/docs/module-3-isaac` - Isaac module
- `/docs/module-4-vla` - VLA module
- `/docs/capstone` - Capstone integration

## Backend Setup (RAG + Personalization)

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file:

```env
# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_api_key

# Neon Postgres
DATABASE_URL=postgres://user:pass@ep-xxx.neon.tech/physical_ai_book

# OpenAI
OPENAI_API_KEY=sk-...

# Better-Auth
AUTH_SECRET=your_secret_key
AUTH_URL=http://localhost:8000
```

### 5. Initialize Database

```bash
python -m alembic upgrade head
```

### 6. Generate Embeddings (First Time)

```bash
python scripts/generate_embeddings.py
```

This reads all Markdown files from `docs/`, chunks them, and uploads embeddings to Qdrant.

### 7. Run Backend Server

```bash
uvicorn main:app --reload --port 8000
```

API available at `http://localhost:8000`.

### 8. Test RAG Endpoint

```bash
curl -X POST http://localhost:8000/api/rag/book-qa \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

## Content Authoring Workflow

### 1. Create Feature Spec

```bash
# Always start with a specification
/sp.specify "Add chapter on ROS 2 Services"
```

### 2. Plan Implementation

```bash
/sp.plan
```

### 3. Write Content

Edit Markdown files in `docs/`:
- Follow Docusaurus Markdown format
- Include APA citations for all technical claims
- Add code examples with language tags

### 4. Regenerate Embeddings

```bash
cd backend
python scripts/generate_embeddings.py --incremental
```

### 5. Test Locally

```bash
npm run build
npm run serve
```

### 6. Commit and Push

```bash
git add .
git commit -m "feat: add ROS 2 Services chapter"
git push origin <branch-name>
```

GitHub Actions will automatically deploy to GitHub Pages.

## Troubleshooting

**Docusaurus build fails**:
- Clear cache: `npm run clear`
- Check for broken links in Markdown

**Backend embeddings fail**:
- Verify Qdrant API key and cluster URL
- Check Markdown file formatting (no malformed frontmatter)

**Translation not working**:
- Verify OpenAI API key has GPT-4 access
- Check translation cache in Postgres

## Next Steps

- Review [Constitution](.specify/memory/constitution.md) for content standards
- Read [Specification](specs/002-book-layout-structure/spec.md) for feature requirements
- Explore [Plan](specs/002-book-layout-structure/plan.md) for architecture details
