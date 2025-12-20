# Physical AI & Humanoid Robotics
## AI-Native Interactive Textbook

**Author:** Asif Ali
**Project Type:** Hackathon Project
**Live Demo:** [ai-humanoid-robotics-as.vercel.app](https://ai-humanoid-robotics-as.vercel.app)

---

## Project Overview

An AI-native interactive textbook for building autonomous humanoid robots. This platform combines comprehensive educational content with AI-powered features to create an immersive learning experience.

### Key Features
- Interactive RAG-powered AI Chatbot
- Text selection-based Q&A
- User authentication system
- 145+ searchable topics
- 6 core learning modules
- Dark/Light mode support
- Fully responsive design

---

## Technology Stack

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Docusaurus** | 3.6.3 | Static site generator for documentation |
| **React** | 18.3.1 | UI component library |
| **TypeScript** | 5.7.2 | Type-safe JavaScript |
| **MDX** | 3.1.0 | Markdown with JSX components |
| **Prism React Renderer** | 2.4.1 | Syntax highlighting |
| **CSS Modules** | - | Scoped styling |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.109.0 | High-performance Python web framework |
| **Uvicorn** | 0.27.0 | ASGI server |
| **Pydantic** | 2.5.3 | Data validation |
| **SQLAlchemy** | 2.0.25 | ORM for database operations |
| **Alembic** | 1.13.1 | Database migrations |

### AI & Machine Learning

| Technology | Version | Purpose |
|------------|---------|---------|
| **OpenAI API** | 1.10.0 | GPT-4 for answer generation |
| **Qdrant** | 1.7.3 | Vector database for semantic search |
| **Tiktoken** | 0.5.2 | Token counting |
| **text-embedding-3-small** | - | OpenAI embeddings model |

### Authentication & Security

| Technology | Version | Purpose |
|------------|---------|---------|
| **python-jose** | 3.3.0 | JWT token handling |
| **Passlib + bcrypt** | 1.7.4 / 4.2.1 | Password hashing |
| **Email Validator** | 2.0.0 | Email validation |

### Database

| Technology | Purpose |
|------------|---------|
| **SQLite** | Local development database |
| **PostgreSQL** | Production database (optional) |
| **Qdrant Cloud** | Vector storage for embeddings |

### Deployment

| Platform | Purpose |
|----------|---------|
| **Vercel** | Frontend hosting (auto-deploy from GitHub) |
| **Hugging Face Spaces** | Backend API hosting |
| **GitHub** | Version control & CI/CD |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ Docusaurus  │  │    React     │  │     RAG Chat Widget     │ │
│  │   (SSG)     │  │  Components  │  │  - Book-wide Q&A        │ │
│  │             │  │              │  │  - Selection-based Q&A  │ │
│  └─────────────┘  └──────────────┘  └─────────────────────────┘ │
│                         │                                        │
│                    Vercel Hosting                                │
└─────────────────────────────────────────────────────────────────┘
                          │
                    HTTPS REST API
                          │
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      FastAPI                                 ││
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  ││
│  │  │  Auth API   │  │   RAG API    │  │   Health Check     │  ││
│  │  │  /register  │  │  /book-qa    │  │   /health          │  ││
│  │  │  /login     │  │  /selection  │  │                    │  ││
│  │  │  /me        │  │    -qa       │  │                    │  ││
│  │  └─────────────┘  └──────────────┘  └────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
│                         │                                        │
│              Hugging Face Spaces Hosting                         │
└─────────────────────────────────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
┌─────────────────────┐    ┌─────────────────────┐
│      SQLite         │    │    Qdrant Cloud     │
│   (User Data)       │    │  (Vector Embeddings)│
│  - Users            │    │  - 119 chunks       │
│  - Query logs       │    │  - 1536 dimensions  │
└─────────────────────┘    └─────────────────────┘
                                    │
                           ┌────────┴────────┐
                           │   OpenAI API    │
                           │  - Embeddings   │
                           │  - GPT-4 Chat   │
                           └─────────────────┘
```

---

## RAG (Retrieval-Augmented Generation) System

### How It Works

```
User Question
      │
      ▼
┌─────────────────┐
│  Embed Query    │  ← OpenAI text-embedding-3-small
│  (1536 dims)    │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Vector Search  │  ← Qdrant similarity search
│  (Top 5 chunks) │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Filter Results │  ← Similarity threshold: 0.1
│  (Relevant only)│
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Build Context  │  ← Combine relevant chunks
│  + User Query   │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  GPT-4 Answer   │  ← Generate contextual answer
│  Generation     │
└─────────────────┘
      │
      ▼
   Response with Sources
```

### Key Metrics
- **119 embedded chunks** from 13 markdown files
- **1536-dimensional vectors** (OpenAI embeddings)
- **Sub-second response time** for vector search
- **Top-5 retrieval** with similarity scoring

---

## Features Deep Dive

### 1. AI Chatbot (Book-wide Q&A)
- Ask any question about the textbook content
- Semantic search across all 145+ topics
- Source citations with relevance scores
- Conversational interface

### 2. Selection-based Q&A
- Highlight any text on the page
- "Ask AI" button appears above selection
- Get explanations, examples, or clarifications
- Context-aware responses

### 3. User Authentication
- JWT-based secure authentication
- Password hashing with bcrypt
- User initials avatar in navbar
- Persistent login sessions

### 4. Learning Modules

| Module | Topics Covered |
|--------|----------------|
| **ROS 2** | Robot Operating System, nodes, topics, services |
| **Digital Twin** | Gazebo simulation, virtual environments |
| **NVIDIA Isaac** | GPU-accelerated robotics simulation |
| **VLA** | Vision-Language-Action models |
| **Hardware** | Jetson, sensors, actuators integration |
| **Capstone** | Complete robot project |

---

## API Endpoints

### Authentication
```
POST /api/auth/register     - Create new user account
POST /api/auth/login-json   - Login and get JWT token
GET  /api/auth/me           - Get current user info
```

### RAG Chatbot
```
POST /api/rag/book-qa       - Ask about entire book
POST /api/rag/selection-qa  - Ask about selected text
```

### Health
```
GET  /health                - API health check
```

---

## Project Structure

```
ai_humanoid_robotics_as/
├── docs/                    # Markdown content (145+ topics)
│   ├── foundations/         # Foundation concepts
│   ├── modules/             # Core learning modules
│   │   ├── ros2/
│   │   ├── digital-twin/
│   │   ├── isaac/
│   │   └── vla/
│   ├── hardware/            # Hardware integration
│   ├── capstone/            # Final project
│   └── ai-features/         # AI feature documentation
├── src/
│   ├── components/          # React components
│   │   ├── RAGChatWidget.tsx
│   │   ├── BookPageWrapper.tsx
│   │   └── UserNavbarItem/
│   ├── config/              # API configuration
│   ├── css/                 # Global styles
│   ├── pages/               # Homepage
│   └── theme/               # Docusaurus theme overrides
├── backend/                 # FastAPI backend (development)
│   ├── api/
│   │   ├── auth/
│   │   └── rag/
│   ├── models/
│   ├── services/
│   └── scripts/
├── hf-deploy/               # Hugging Face deployment
├── static/                  # Static assets
└── docusaurus.config.ts     # Site configuration
```

---

## Development Workflow

### Local Development
```bash
# Frontend
npm install
npm start              # http://localhost:3000

# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Regenerate Embeddings
```bash
cd backend
python -m scripts.generate_embeddings
```

### Deploy
```bash
# Frontend: Auto-deploys on push to main (Vercel)
git push origin main

# Backend: Push to hf-deploy folder
cd hf-deploy
git add . && git commit -m "Update" && git push
```

---

## Performance & Scalability

| Metric | Value |
|--------|-------|
| Build Time | ~45 seconds |
| Page Load | < 2 seconds |
| API Response | < 1 second |
| Vector Search | < 100ms |
| Embedding Generation | ~2 min (119 chunks) |

---

## Security Measures

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure, expiring tokens
- **CORS**: Configured for allowed origins
- **Input Validation**: Pydantic models
- **Rate Limiting**: Via Hugging Face Spaces
- **Environment Variables**: Secrets in .env files

---

## Future Enhancements

1. **Progress Tracking**: Save user reading progress
2. **Quiz System**: Interactive assessments
3. **Code Sandbox**: In-browser code execution
4. **Collaborative Notes**: Shared annotations
5. **Offline Mode**: PWA support
6. **Voice Interface**: Speech-to-text Q&A

---

## Contact

**Asif Ali**
- Email: asif.alimusharaf@gmail.com
- LinkedIn: [linkedin.com/in/asif-ali-a1879a2ba](https://linkedin.com/in/asif-ali-a1879a2ba)
- GitHub: [github.com/asifaliattari](https://github.com/asifaliattari)
- YouTube: [youtube.com/@AstolixGen](https://youtube.com/@AstolixGen)
- Phone: +92 330 2541908

---

## Live Links

- **Frontend**: [ai-humanoid-robotics-as.vercel.app](https://ai-humanoid-robotics-as.vercel.app)
- **Backend API**: [asifaliastolixgen-physical-ai-book-api.hf.space](https://asifaliastolixgen-physical-ai-book-api.hf.space)
- **GitHub Repo**: [github.com/asifaliattari/ai_humanoid_robotics_as](https://github.com/asifaliattari/ai_humanoid_robotics_as)
- **API Docs**: [Backend /docs endpoint](https://asifaliastolixgen-physical-ai-book-api.hf.space/docs)

---

## Thank You!

*Built with passion for AI, Robotics, and Education*
