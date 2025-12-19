# Physical AI & Humanoid Robotics - AI-Native Textbook

An interactive AI-native textbook built with **Docusaurus v3**, **FastAPI**, and **RAG chatbot**. Powered by **OpenAI GPT-4**, **Qdrant**, and **SQLite/Neon Postgres**.

## Live Demo

- **Frontend**: [Vercel Deployment](https://ai-humanoid-robotics-as.vercel.app)
- **Backend API**: [Hugging Face Spaces](https://asifaliastolixgen-physical-ai-book-api.hf.space)

## Features

- **RAG Chatbot**: Ask questions about the book content
  - Semantic search powered by Qdrant vector database
  - AI-powered answers with GPT-4

- **User Authentication**: JWT-based login system
  - Secure registration and login
  - User avatar with initials in navbar

- **Technical Content**: Comprehensive robotics learning
  - ROS 2, NVIDIA Isaac, Digital Twin, VLA systems
  - Hardware guides and tutorials
  - Beginner-friendly instruction

## Quick Start

### Frontend (Docusaurus)

```bash
# Install dependencies
npm install

# Start development server
npm start
# Opens at http://localhost:3000
```

### Backend (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run server
uvicorn main:app --reload
# API at http://localhost:8000
```

### Build for Production

```bash
npm run build
npm run serve
```

## Project Structure

```
ai_humanoid_robotics_as/
├── backend/                    # FastAPI backend
│   ├── api/                    # API endpoints
│   │   ├── auth/               # Authentication (JWT)
│   │   └── rag/                # RAG chatbot
│   ├── models/                 # SQLAlchemy models
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   └── requirements.txt        # Python dependencies
├── docs/                       # Book content (Markdown)
│   ├── foundations/            # Physical AI basics
│   ├── modules/                # Core learning modules
│   │   ├── ros2/               # Module 1: ROS 2
│   │   ├── digital-twin/       # Module 2: Simulation
│   │   ├── isaac/              # Module 3: NVIDIA Isaac
│   │   └── vla/                # Module 4: VLA systems
│   ├── hardware/               # Hardware guides
│   ├── capstone/               # Integration project
│   └── ai-features/            # AI features documentation
├── src/
│   ├── components/             # React components
│   │   ├── RAGChatWidget.tsx   # Floating chatbot
│   │   └── UserNavbarItem/     # User avatar/login
│   ├── pages/                  # Custom pages
│   │   ├── index.tsx           # Homepage
│   │   └── login.tsx           # Login page
│   └── theme/                  # Theme customizations
├── hf-deploy/                  # Hugging Face backend (submodule)
├── blog/                       # Blog posts
├── static/                     # Static assets
├── docusaurus.config.ts        # Docusaurus configuration
├── sidebars.ts                 # Sidebar navigation
└── package.json                # NPM dependencies
```

## Deployment

### Frontend (Vercel)

The frontend automatically deploys to Vercel on push to `main` branch.

### Backend (Hugging Face Spaces)

The backend is deployed as a Hugging Face Space. Push changes to `hf-deploy/` submodule.

```bash
cd hf-deploy
git add .
git commit -m "Update backend"
git push
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login-json` | POST | Login (returns JWT) |
| `/api/auth/me` | GET | Get current user |
| `/api/rag/book-qa` | POST | Ask questions about book |
| `/api/rag/selection-qa` | POST | Q&A on selected text |
| `/health` | GET | Health check |

## Development

### NPM Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm run serve` - Serve production build
- `npm run clear` - Clear Docusaurus cache

### Environment Variables

Backend requires these in `backend/.env`:

```env
DATABASE_URL=sqlite:///./database.db
AUTH_SECRET=your-secret-key-min-32-chars
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
```

## Contributing

1. Create a feature branch
2. Make changes
3. Test with `npm run build`
4. Submit pull request

## License

MIT License

---

**Built with**: Docusaurus v3 | FastAPI | React | TypeScript
