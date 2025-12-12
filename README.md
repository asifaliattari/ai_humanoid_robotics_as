# Physical AI & Humanoid Robotics - AI-Native Textbook

An interactive AI-native textbook built with **Docusaurus v3**, **FastAPI**, **RAG chatbot**, **multi-language translation**, and **personalized learning**. Powered by **OpenAI GPT-4**, **Qdrant**, and **Neon Postgres**.

## 🌟 Features

### AI-Native Learning Experience

- **🤖 RAG Chatbot**: Ask questions about the entire book or selected text
  - Book-wide semantic search powered by Qdrant vector database
  - Selection-based Q&A for highlighted text
  - Answers with cited sources

- **🌐 Multi-Language Translation**: Instant translation to 5 languages
  - English, Urdu (اردو), French (Français), Arabic (العربية), German (Deutsch)
  - RTL support for Urdu and Arabic
  - Smart caching reduces costs by 80-90%
  - Code blocks and technical terms preserved

- **⚙️ Personalized Learning**: Content adapts to your setup
  - Hardware-based: Cloud GPU alternatives, Jetson optimizations
  - Experience-based: Beginner tutorials, expert research papers
  - Robot-specific: Integration guides for your hardware

### Technical Excellence

- **Spec-driven development** - No content without specifications
- **Technical accuracy** - All content based on official documentation
- **Beginner-friendly style** - Clear, accessible instruction
- **Reproducibility** - All tutorials and commands are verified
- **AI-native modularity** - Structured for continuous improvement

## Quick Start

### 5-Minute Setup with Docker

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/ai_humanoid_robotics_as.git
cd ai_humanoid_robotics_as

# 2. Configure backend (get free API keys - see SETUP.md)
cd backend
cp .env.example .env
# Edit .env with your API keys

# 3. Start everything with Docker Compose
cd ..
docker-compose up -d

# ✅ Frontend: http://localhost:3000
# ✅ Backend API: http://localhost:8000/docs
```

### Manual Setup

**Prerequisites:**
- Node.js 18+ and npm
- Python 3.11+
- API keys (Qdrant, Neon, OpenAI) - See [SETUP.md](SETUP.md)

**Frontend:**
```bash
npm install
npm start
# Opens at http://localhost:3000
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys
alembic upgrade head
python -m scripts.generate_embeddings
uvicorn main:app --reload
# API at http://localhost:8000
```

📘 **Detailed setup guide**: [SETUP.md](SETUP.md)

### Build for Production

```bash
# Build static files
npm run build

# Serve production build locally
npm run serve
```

The production build will be in the `build/` directory.

## Project Structure

```
ai_humanoid_robotics_as/
├── backend/                    # FastAPI backend
│   ├── alembic/                # Database migrations
│   │   ├── versions/           # Migration scripts
│   │   └── env.py
│   ├── api/                    # API endpoints
│   │   ├── rag/                # RAG chatbot
│   │   │   ├── book_qa.py      # Book-wide Q&A
│   │   │   └── selection_qa.py # Selection-based Q&A
│   │   ├── personalization/    # Content adaptation
│   │   │   ├── user_profile.py
│   │   │   └── content_adapter.py
│   │   └── translation/        # Multi-language
│   │       └── translate.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py             # User profiles
│   │   └── content.py          # Progress, logs, cache
│   ├── services/               # Business logic
│   │   ├── qdrant_service.py   # Vector database
│   │   └── embedding_service.py # OpenAI embeddings
│   ├── scripts/
│   │   └── generate_embeddings.py # Embed docs
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   ├── requirements.txt        # Python deps
│   ├── .env.example            # Config template
│   ├── Dockerfile              # Container
│   └── README.md               # Backend docs
├── docs/                       # Book content
│   ├── foundations/            # Physical AI basics
│   ├── modules/                # 4 core modules
│   │   ├── ros2/               # Module 1: ROS 2
│   │   ├── digital-twin/       # Module 2: Simulation
│   │   ├── isaac/              # Module 3: NVIDIA Isaac
│   │   └── vla/                # Module 4: VLA systems
│   ├── hardware/               # Hardware guides
│   ├── capstone/               # Integration project
│   ├── ai-features/            # AI features docs
│   └── meta/                   # How to use
├── src/
│   ├── components/             # React components
│   │   ├── TranslationToggle.tsx # 5-language selector
│   │   ├── PersonalizeButton.tsx # Content adaptation
│   │   ├── RAGChatWidget.tsx     # Floating chatbot
│   │   ├── BookPageWrapper.tsx   # Wrapper component
│   │   └── index.ts
│   ├── css/
│   │   └── custom.css
│   └── pages/
│       └── index.tsx           # Homepage
├── specs/                      # Feature specifications
│   └── 002-book-layout-structure/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── contracts/          # API specs
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
├── docker-compose.yml          # Local development
├── docusaurus.config.ts        # Docusaurus config
├── sidebars.ts                 # Sidebar config
├── SETUP.md                    # Detailed setup guide
└── README.md                   # This file
```

## Development Workflow

### Creating New Content

1. **Write a specification** in `specs/<feature-name>/spec.md` following the spec template
2. **Implement content** based on the spec
3. **Validate** that content matches spec requirements
4. **Commit** with meaningful commit message

### NPM Scripts

- `npm start` - Start development server with hot reload
- `npm run build` - Build production static files
- `npm run serve` - Serve production build locally
- `npm run clear` - Clear Docusaurus cache
- `npm run deploy` - Deploy to GitHub Pages (manual)

## Deployment

### Automated Deployment (Recommended)

The project uses GitHub Actions for automated deployment:

1. Push code to `main` or `master` branch
2. GitHub Actions automatically builds the site
3. Site deploys to GitHub Pages at `https://YOUR_USERNAME.github.io/ai_humanoid_robotics_as/`

**Note**: Ensure GitHub Pages is enabled in repository settings and set to deploy from GitHub Actions.

### Manual Deployment

```bash
# Build the site
npm run build

# Deploy (requires GitHub authentication)
GIT_USER=YOUR_USERNAME npm run deploy
```

## Configuration

### Update GitHub Username

Before deploying, update these files with your GitHub username:

**`docusaurus.config.ts`** (line 8):
```typescript
const githubUsername = 'YOUR_USERNAME'; // Change this
```

**`blog/authors.yml`**:
```yaml
admin:
  url: https://github.com/YOUR_USERNAME  # Change this
  image_url: https://github.com/YOUR_USERNAME.png  # Change this
```

### Docusaurus Configuration

Main configuration is in `docusaurus.config.ts`:

- **Title & tagline**: Update site metadata
- **URL & baseUrl**: Configure for GitHub Pages
- **Theme**: Customize colors, navbar, footer
- **Plugins**: Add additional Docusaurus plugins

## Constitution & Principles

This project follows the principles defined in `.specify/memory/constitution.md`:

### Core Principles

1. **Spec-Driven Writing** - All content must have corresponding specifications
2. **Technical Accuracy** - Content based on official documentation with APA citations
3. **Beginner-Friendly Style** - Clear, accessible, step-by-step instruction
4. **Reproducibility** - All commands and workflows must be executable
5. **AI-Native Modularity** - Structured for iterative AI/human improvement

### Standards

- **Formatting Consistency** - Commands in code blocks, consistent file trees
- **Validation Discipline** - All instructions tested from clean environment
- **External References** - APA citation format for all external sources
- **Version Control** - Conventional commit messages, meaningful PRs

### Constraints

- **Output Format**: Markdown (Docusaurus v3+) only
- **Deployment**: GitHub Pages via GitHub Actions (automated)
- **Specs**: Stored in `/specs/` directory
- **Technology**: Docusaurus v3+ required

## Troubleshooting

### Port Already in Use

If `npm start` fails with "Port 3000 already in use":

```bash
# Use different port
npm start -- --port 3001
```

### Build Fails

```bash
# Clear cache and rebuild
npm run clear
npm run build
```

### Dependencies Issues

```bash
# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Contributing

1. Create a feature specification in `specs/<feature-name>/spec.md`
2. Create a feature branch following naming convention
3. Implement content following the spec
4. Ensure build succeeds: `npm run build`
5. Commit with conventional commit format
6. Create pull request referencing the spec

## Resources

- **Docusaurus Documentation**: https://docusaurus.io/docs
- **Spec-Kit Plus**: Templates in `.specify/templates/`
- **Constitution**: `.specify/memory/constitution.md`
- **Specifications**: `specs/` directory

## License

This project is licensed under the MIT License.

## Support

For issues or questions:

- Check the [Docusaurus documentation](https://docusaurus.io/docs)
- Review existing specifications in `specs/`
- Open an issue on GitHub

---

**Built with**: Docusaurus v3.6.3 | Node.js 20+ | TypeScript
**Deployed to**: GitHub Pages
**Maintained by**: [Your Name]
