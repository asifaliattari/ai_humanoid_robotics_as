# Physical AI & Humanoid Robotics - Complete Project Documentation

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Architecture & System Design](#3-architecture--system-design)
4. [Folder Structure](#4-folder-structure)
5. [Authentication System](#5-authentication-system)
6. [API Endpoints](#6-api-endpoints)
7. [Frontend Components](#7-frontend-components)
8. [Services & Business Logic](#8-services--business-logic)
9. [Database Schema](#9-database-schema)
10. [Libraries & Dependencies](#10-libraries--dependencies)
11. [Flowcharts](#11-flowcharts)
12. [Interview Q&A](#12-interview-qa)
13. [Known Issues & Future Improvements](#13-known-issues--future-improvements)

---

## 1. Project Overview

**Project Name:** Physical AI & Humanoid Robotics - AI-Native Textbook

**Description:** An interactive, AI-powered learning platform for building autonomous humanoid robots. The platform features:
- A Docusaurus-based textbook with 6 comprehensive modules
- AI-powered RAG (Retrieval-Augmented Generation) chatbot
- Multi-language translation support (English, Urdu, French, Arabic, German)
- User personalization based on hardware and experience
- JWT-based authentication system

**Target Audience:** Students, researchers, and developers learning humanoid robotics

**Deployment:**
- Frontend: GitHub Pages / Vercel
- Backend: Docker-ready for Railway, Vercel, or self-hosted
- Database: Neon Serverless Postgres + Qdrant Vector DB

---

## 2. Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Docusaurus | 3.6.3 | Static site generator for documentation |
| React | 18.3.1 | UI component library |
| TypeScript | 5.7.2 | Type-safe JavaScript |
| MDX | 3.1.0 | Markdown with JSX support |
| Prism | 2.4.1 | Code syntax highlighting |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.109.0 | Async Python web framework |
| Uvicorn | 0.27.0 | ASGI server |
| SQLAlchemy | 2.0.25 | ORM for database operations |
| Pydantic | 2.5.3 | Data validation |

### Authentication
| Technology | Version | Purpose |
|------------|---------|---------|
| python-jose | 3.3.0 | JWT token handling |
| passlib | 1.7.4 | Password hashing |
| bcrypt | 4.2.1 | Secure password encryption |

### AI/ML
| Technology | Version | Purpose |
|------------|---------|---------|
| OpenAI | 1.10.0 | GPT-4 for chat, text-embedding-3-small for vectors |
| Qdrant | 1.7.3 | Vector database for semantic search |
| tiktoken | 0.5.2 | Token counting for OpenAI |

### Database
| Technology | Purpose |
|------------|---------|
| Neon Postgres | Primary relational database (serverless) |
| Qdrant | Vector database for RAG embeddings |
| Alembic | Database migrations |

---

## 3. Architecture & System Design

### High-Level Architecture

```
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|   Docusaurus      |---->|   FastAPI         |---->|   Neon Postgres   |
|   Frontend        |     |   Backend         |     |   Database        |
|   (React/TS)      |<----|   (Python)        |<----|                   |
|                   |     |                   |     +-------------------+
+-------------------+     +-------------------+              |
        |                         |                         |
        |                         v                         v
        |                 +-------------------+     +-------------------+
        |                 |                   |     |                   |
        +---------------->|   OpenAI API      |     |   Qdrant          |
                          |   (GPT-4, Embed)  |     |   Vector DB       |
                          |                   |     |                   |
                          +-------------------+     +-------------------+
```

### Request Flow

```
User Browser
    |
    v
Docusaurus Frontend (localhost:3000)
    |
    |-- Static Content --> MDX/Markdown Files
    |
    |-- API Calls --> FastAPI Backend (localhost:8000)
                            |
                            |-- Auth --> JWT Validation --> Postgres (users table)
                            |
                            |-- RAG --> OpenAI Embeddings --> Qdrant --> GPT-4 Response
                            |
                            |-- Translation --> GPT-4 --> Cache (Postgres)
                            |
                            |-- Personalization --> User Profile (Postgres)
```

---

## 4. Folder Structure

```
D:\hakathon\ai_humanoid_robotics_as/
|
├── backend/                          # FastAPI Python Backend
│   ├── api/                          # API Route Handlers
│   │   ├── auth/
│   │   │   ├── auth.py               # Login, Register, User endpoints
│   │   │   └── __init__.py
│   │   ├── rag/
│   │   │   ├── book_qa.py            # Book-wide Q&A endpoint
│   │   │   ├── selection_qa.py       # Text selection Q&A
│   │   │   └── __init__.py
│   │   ├── personalization/
│   │   │   ├── user_profile.py       # User profile management
│   │   │   ├── content_adapter.py    # Content recommendations
│   │   │   └── __init__.py
│   │   └── translation/
│   │       ├── translate.py          # Translation endpoint
│   │       └── __init__.py
│   │
│   ├── models/                       # SQLAlchemy ORM Models
│   │   ├── auth.py                   # User authentication model
│   │   ├── user.py                   # UserProfile with preferences
│   │   ├── content.py                # ReadingProgress, QueryLog, Cache
│   │   └── __init__.py               # Database session setup
│   │
│   ├── services/                     # Business Logic Services
│   │   ├── qdrant_service.py         # Vector database operations
│   │   ├── embedding_service.py      # OpenAI embedding generation
│   │   └── __init__.py
│   │
│   ├── scripts/
│   │   ├── generate_embeddings.py    # Populate Qdrant with book content
│   │   └── __init__.py
│   │
│   ├── alembic/                      # Database Migrations
│   │   └── versions/
│   │
│   ├── main.py                       # FastAPI application entry point
│   ├── config.py                     # Settings from environment
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables (git-ignored)
│   ├── Dockerfile                    # Container configuration
│   └── README.md
│
├── src/                              # Frontend React Components
│   ├── components/
│   │   ├── RAGChatWidget.tsx         # AI Chatbot widget (230 lines)
│   │   ├── RAGChatWidget.css
│   │   ├── TranslationToggle.tsx     # 5-language selector (130 lines)
│   │   ├── TranslationToggle.css
│   │   ├── PersonalizeButton.tsx     # Content adaptation trigger
│   │   ├── PersonalizeButton.css
│   │   ├── BookPageWrapper.tsx
│   │   ├── SimpleBookPage.tsx
│   │   └── index.ts                  # Component exports
│   │
│   ├── pages/
│   │   ├── login.tsx                 # Login/Signup page (230 lines)
│   │   ├── index.tsx                 # Homepage with features
│   │   └── index.module.css
│   │
│   ├── theme/
│   │   └── Root.tsx                  # Root layout (adds chatbot globally)
│   │
│   ├── config/
│   │   └── api.ts                    # API endpoint configuration
│   │
│   └── css/
│       └── custom.css                # Custom styling
│
├── docs/                             # Book Content (Markdown/MDX)
│   ├── intro.md
│   ├── foundations/                  # Foundation chapters
│   ├── modules/
│   │   ├── ros2/                     # Module 1: ROS 2
│   │   ├── digital-twin/             # Module 2: Digital Twin
│   │   ├── isaac/                    # Module 3: NVIDIA Isaac
│   │   └── vla/                      # Module 4: Vision-Language-Action
│   ├── hardware/                     # Hardware integration
│   ├── capstone/                     # Final project
│   └── ai-features/                  # AI feature documentation
│
├── blog/                             # Blog posts
├── static/                           # Static assets (images, icons)
├── build/                            # Production build output
│
├── docusaurus.config.ts              # Docusaurus configuration
├── sidebars.ts                       # Sidebar navigation
├── package.json                      # NPM dependencies
├── tsconfig.json                     # TypeScript configuration
└── docker-compose.yml                # Local development containers
```

---

## 5. Authentication System

### Overview
The authentication system uses JWT (JSON Web Tokens) with bcrypt password hashing.

### Components

**Backend Files:**
- `backend/api/auth/auth.py` - Authentication endpoints
- `backend/models/auth.py` - User database model
- `backend/config.py` - JWT settings

**Frontend Files:**
- `src/pages/login.tsx` - Login/Signup UI
- `src/config/api.ts` - API endpoint URLs

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        REGISTRATION FLOW                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  User                    Frontend                   Backend         │
│   │                         │                          │            │
│   │ Fill form               │                          │            │
│   │────────────────────────>│                          │            │
│   │                         │                          │            │
│   │                         │ POST /api/auth/register  │            │
│   │                         │ {email, password, name}  │            │
│   │                         │─────────────────────────>│            │
│   │                         │                          │            │
│   │                         │                          │ Check if   │
│   │                         │                          │ email      │
│   │                         │                          │ exists     │
│   │                         │                          │            │
│   │                         │                          │ Hash       │
│   │                         │                          │ password   │
│   │                         │                          │ (bcrypt)   │
│   │                         │                          │            │
│   │                         │                          │ Save to    │
│   │                         │                          │ database   │
│   │                         │                          │            │
│   │                         │ {id, email, name}        │            │
│   │                         │<─────────────────────────│            │
│   │                         │                          │            │
│   │ "Account created!"      │                          │            │
│   │<────────────────────────│                          │            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                          LOGIN FLOW                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  User                    Frontend                   Backend         │
│   │                         │                          │            │
│   │ Enter credentials       │                          │            │
│   │────────────────────────>│                          │            │
│   │                         │                          │            │
│   │                         │ POST /api/auth/login-json│            │
│   │                         │ {email, password}        │            │
│   │                         │─────────────────────────>│            │
│   │                         │                          │            │
│   │                         │                          │ Find user  │
│   │                         │                          │ by email   │
│   │                         │                          │            │
│   │                         │                          │ Verify     │
│   │                         │                          │ password   │
│   │                         │                          │ (bcrypt)   │
│   │                         │                          │            │
│   │                         │                          │ Generate   │
│   │                         │                          │ JWT token  │
│   │                         │                          │            │
│   │                         │ {access_token, user_id,  │            │
│   │                         │  email, token_type}      │            │
│   │                         │<─────────────────────────│            │
│   │                         │                          │            │
│   │                         │ Store in localStorage:   │            │
│   │                         │ - access_token           │            │
│   │                         │ - user_id                │            │
│   │                         │ - user_email             │            │
│   │                         │                          │            │
│   │ Redirect to /docs/intro │                          │            │
│   │<────────────────────────│                          │            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### JWT Token Structure

```javascript
// Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// Payload
{
  "sub": "user-uuid",        // User ID
  "email": "user@example.com",
  "exp": 1234567890          // Expiration (30 min default)
}

// Signature
HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), AUTH_SECRET)
```

### Password Security
- **Algorithm:** bcrypt
- **Library:** passlib[bcrypt]
- **Auto-salt:** Yes
- **Work factor:** Default (12 rounds)

---

## 6. API Endpoints

### Base URL
- **Development:** `http://localhost:8000`
- **Production:** Set via `PRODUCTION_BACKEND_URL`

### Authentication Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/auth/register` | POST | Create new user | `{email, password, name?}` | `{id, email, name, is_active, is_verified}` |
| `/api/auth/login-json` | POST | Login with JSON | `{email, password}` | `{access_token, token_type, user_id, email}` |
| `/api/auth/login` | POST | OAuth2 login | Form data | `{access_token, token_type, user_id, email}` |
| `/api/auth/me` | GET | Get current user | Authorization header | `{id, email, name, is_active, is_verified}` |

### RAG Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/rag/book-qa` | POST | Book-wide Q&A | `{question, context?}` | `{answer, sources}` |
| `/api/rag/selection-qa` | POST | Selection Q&A | `{selection, question}` | `{answer}` |

### Personalization Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/personalization/profile` | GET/PUT | User profile | Profile data | Profile object |
| `/api/personalization/adapt-content` | POST | Adapt content | `{content, user_id}` | Adapted content |

### Translation Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/translation/translate` | POST | Translate text | `{text, target_lang}` | `{translated_text}` |
| `/api/translation/supported-languages` | GET | Get languages | - | Language list |

### System Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/` | GET | API info |
| `/docs` | GET | Swagger UI (dev only) |
| `/redoc` | GET | ReDoc (dev only) |

---

## 7. Frontend Components

### RAGChatWidget (`src/components/RAGChatWidget.tsx`)
**Purpose:** Floating AI chatbot available on all pages

**Features:**
- Floating action button (bottom-right corner)
- Toggle open/close
- Message history with timestamps
- Loading indicators
- Source attribution from RAG
- Welcome hints

**State Management:**
```typescript
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: string[];
}
```

### TranslationToggle (`src/components/TranslationToggle.tsx`)
**Purpose:** Multi-language content translation

**Supported Languages:**
- English (EN)
- Urdu (UR) - RTL
- French (FR)
- Arabic (AR) - RTL
- German (DE)

### Login Page (`src/pages/login.tsx`)
**Purpose:** User authentication UI

**Features:**
- Login/Signup toggle
- Email validation
- Password requirements (8+ chars)
- OAuth buttons (placeholder)
- Guest continue option
- Demo mode (when backend unavailable)

**Data Storage (localStorage):**
```javascript
localStorage.setItem('access_token', token);
localStorage.setItem('user_id', userId);
localStorage.setItem('user_email', email);
```

### Root Component (`src/theme/Root.tsx`)
**Purpose:** Global wrapper adding chatbot to all pages

---

## 8. Services & Business Logic

### Qdrant Service (`backend/services/qdrant_service.py`)
**Purpose:** Vector database operations

**Functions:**
- Initialize connection to Qdrant
- Create/manage collections
- Upsert vectors with metadata
- Search similar vectors
- Delete vectors

### Embedding Service (`backend/services/embedding_service.py`)
**Purpose:** Generate OpenAI embeddings

**Model:** `text-embedding-3-small`
**Dimensions:** 1536

**Functions:**
- Generate single embedding
- Batch embeddings
- Handle rate limits

### Authentication Utilities (`backend/api/auth/auth.py`)
```python
def verify_password(plain, hashed) -> bool
def get_password_hash(password) -> str
def create_access_token(data, expires_delta) -> str
async def get_current_user(token, db) -> User
```

---

## 9. Database Schema

### Users Table (`models/auth.py`)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    name VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    last_login TIMESTAMP
);
```

### User Profiles Table (`models/user.py`)
```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),

    -- Hardware Inventory
    has_rtx_gpu BOOLEAN DEFAULT FALSE,
    jetson_model VARCHAR,  -- 'orin_nano', 'orin_nx', 'agx_orin', etc.
    robot_type VARCHAR,    -- 'humanoid', 'quadruped', 'arm', etc.
    sensors JSONB,         -- Array of sensor types

    -- Experience Levels (1-5)
    ros2_experience INTEGER DEFAULT 1,
    ml_experience INTEGER DEFAULT 1,
    robotics_experience INTEGER DEFAULT 1,
    simulation_experience INTEGER DEFAULT 1,

    -- Preferences
    preferred_language VARCHAR DEFAULT 'en',
    theme VARCHAR DEFAULT 'system',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### Reading Progress Table (`models/content.py`)
```sql
CREATE TABLE reading_progress (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    section_id VARCHAR NOT NULL,
    progress_percent INTEGER DEFAULT 0,
    time_spent_seconds INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    last_accessed TIMESTAMP DEFAULT NOW()
);
```

### Translation Cache Table
```sql
CREATE TABLE translation_cache (
    id UUID PRIMARY KEY,
    source_text_hash VARCHAR NOT NULL,
    source_lang VARCHAR NOT NULL,
    target_lang VARCHAR NOT NULL,
    translated_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);
```

---

## 10. Libraries & Dependencies

### Frontend (package.json)
```json
{
  "dependencies": {
    "@docusaurus/core": "3.6.3",
    "@docusaurus/preset-classic": "3.6.3",
    "@mdx-js/react": "3.1.0",
    "clsx": "2.1.1",
    "prism-react-renderer": "2.4.1",
    "react": "18.3.1",
    "react-dom": "18.3.1"
  },
  "devDependencies": {
    "@docusaurus/module-type-aliases": "3.6.3",
    "@docusaurus/tsconfig": "3.6.3",
    "@docusaurus/types": "3.6.3",
    "typescript": "5.7.2"
  }
}
```

### Backend (requirements.txt)
```
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
asyncpg==0.29.0
sqlalchemy==2.0.25
alembic==1.13.1

# Vector Database
qdrant-client==1.7.3

# AI/ML
openai==1.10.0
tiktoken==0.5.2

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.2.1
email-validator>=2.0.0

# HTTP & Utils
httpx==0.26.0
python-json-logger==2.0.7
python-dotenv==1.0.0
```

---

## 11. Flowcharts

### Overall System Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER JOURNEY                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐      │
│   │           │     │           │     │           │     │           │      │
│   │  Landing  │────>│   Login   │────>│   Book    │────>│  Chapter  │      │
│   │   Page    │     │   Page    │     │   Home    │     │  Content  │      │
│   │           │     │           │     │           │     │           │      │
│   └───────────┘     └───────────┘     └───────────┘     └───────────┘      │
│         │                 │                 │                 │             │
│         │                 │                 │                 │             │
│         v                 v                 v                 v             │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐      │
│   │ View      │     │ Register/ │     │ Browse    │     │ Read      │      │
│   │ Features  │     │ Login     │     │ Modules   │     │ Content   │      │
│   │           │     │ JWT Auth  │     │           │     │           │      │
│   └───────────┘     └───────────┘     └───────────┘     └───────────┘      │
│                                                               │             │
│                                                               │             │
│                           ┌───────────────────────────────────┘             │
│                           │                                                 │
│                           v                                                 │
│   ┌───────────────────────────────────────────────────────────────┐        │
│   │                     AI FEATURES (Available on all pages)       │        │
│   │                                                                │        │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │        │
│   │  │ RAG Chat    │  │ Translation │  │ Personalization     │   │        │
│   │  │ Widget      │  │ Toggle      │  │ Button              │   │        │
│   │  │             │  │             │  │                     │   │        │
│   │  │ Ask about   │  │ EN/UR/FR/   │  │ Adapt content to    │   │        │
│   │  │ book content│  │ AR/DE       │  │ user hardware &     │   │        │
│   │  │             │  │             │  │ experience          │   │        │
│   │  └─────────────┘  └─────────────┘  └─────────────────────┘   │        │
│   │                                                                │        │
│   └───────────────────────────────────────────────────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### RAG Chatbot Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAG CHATBOT FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Question                                                  │
│       │                                                         │
│       v                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Generate Embedding                          │   │
│  │              (OpenAI text-embedding-3-small)             │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       v                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Search Qdrant                               │   │
│  │              (Top 5 similar chunks)                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       v                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Build Context                               │   │
│  │              (Question + Retrieved chunks)               │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       v                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Generate Answer                             │   │
│  │              (GPT-4-turbo-preview)                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       v                                                         │
│  Response + Source Citations                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Translation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSLATION FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Content + Target Language                                      │
│       │                                                         │
│       v                                                         │
│  ┌────────────────────┐                                        │
│  │  Check Cache       │                                        │
│  │  (hash lookup)     │                                        │
│  └────────────────────┘                                        │
│       │                                                         │
│       ├── Cache Hit ──────────> Return Cached Translation      │
│       │                                                         │
│       v                                                         │
│  ┌────────────────────┐                                        │
│  │  Call OpenAI GPT-4 │                                        │
│  │  for translation   │                                        │
│  └────────────────────┘                                        │
│       │                                                         │
│       v                                                         │
│  ┌────────────────────┐                                        │
│  │  Store in Cache    │                                        │
│  │  (24hr TTL)        │                                        │
│  └────────────────────┘                                        │
│       │                                                         │
│       v                                                         │
│  Return Translation                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Interview Q&A

### Project Overview Questions

**Q: What is this project about?**
> A: This is an AI-native textbook platform for learning humanoid robotics. It combines a Docusaurus static site with a FastAPI backend, featuring AI-powered Q&A, multi-language translation, and personalized content based on user hardware and experience.

**Q: Why did you choose this technology stack?**
> A:
> - **Docusaurus:** Best-in-class documentation framework with MDX support, perfect for technical books
> - **FastAPI:** Async Python framework with automatic OpenAPI docs, ideal for AI/ML workloads
> - **Neon Postgres:** Serverless PostgreSQL for cost-effective scaling
> - **Qdrant:** Purpose-built vector database for RAG applications
> - **JWT:** Stateless authentication that scales horizontally

**Q: How does the authentication work?**
> A: We use JWT-based authentication with bcrypt password hashing:
> 1. User registers with email/password
> 2. Password is hashed using bcrypt (salt auto-generated)
> 3. On login, password is verified against hash
> 4. JWT token is generated with user_id and email
> 5. Token expires in 30 minutes
> 6. Frontend stores token in localStorage

**Q: What is RAG and how did you implement it?**
> A: RAG (Retrieval-Augmented Generation) combines search with LLM generation:
> 1. Book content is chunked and embedded using OpenAI's text-embedding-3-small
> 2. Embeddings stored in Qdrant vector database
> 3. User questions are embedded and searched against Qdrant
> 4. Top 5 relevant chunks are retrieved
> 5. GPT-4 generates answer using retrieved context
> 6. Sources are cited in the response

**Q: How do you handle multiple languages?**
> A: Translation is handled via GPT-4 with aggressive caching:
> 1. Content is hashed to create a cache key
> 2. Cache checked first (24-hour TTL)
> 3. If miss, GPT-4 translates
> 4. Result cached for future requests
> 5. RTL languages (Urdu, Arabic) trigger layout changes

### Technical Deep-Dive Questions

**Q: Explain the database schema design.**
> A: We have 4 main tables:
> - `users`: Core auth data (email, password_hash, active status)
> - `user_profiles`: Hardware inventory, experience levels, preferences
> - `reading_progress`: Track user progress through chapters
> - `translation_cache`: Cache translations to reduce API costs
>
> We use UUIDs for all primary keys and foreign key relationships between users and profiles.

**Q: How do you handle CORS?**
> A: CORS is configured in FastAPI middleware:
> ```python
> app.add_middleware(
>     CORSMiddleware,
>     allow_origins=settings.cors_origins,  # From .env
>     allow_credentials=True,
>     allow_methods=["*"],
>     allow_headers=["*"],
> )
> ```

**Q: What security measures are in place?**
> A:
> - Bcrypt password hashing (12 rounds)
> - JWT tokens with expiration
> - CORS restrictions
> - Input validation via Pydantic
> - SQL injection prevention via SQLAlchemy ORM
> - Environment variables for secrets

**Q: How would you scale this application?**
> A:
> - **Frontend:** Already static, use CDN (Vercel/Cloudflare)
> - **Backend:** Horizontal scaling with load balancer (Railway/Vercel)
> - **Database:** Neon auto-scales, add read replicas if needed
> - **Vector DB:** Qdrant Cloud has built-in scaling
> - **Caching:** Add Redis for session/rate limiting

**Q: What improvements would you make?**
> A:
> 1. Add OAuth (GitHub, Google) - currently placeholder
> 2. Display username in navbar after login - not implemented
> 3. Add rate limiting for API endpoints
> 4. Implement refresh tokens for better UX
> 5. Add WebSocket for real-time chat
> 6. Add user progress dashboard

---

## 13. Known Issues & Future Improvements

### Current Issues

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| No username display after login | Medium | `docusaurus.config.ts` | Login stores data but navbar doesn't show username |
| GitHub OAuth placeholder | Low | `src/pages/login.tsx:161-177` | Shows "OAuth coming soon" alert |
| No refresh token | Medium | `backend/api/auth/auth.py` | Only access token, re-login required after 30 min |

### Recommended Improvements

1. **Add NavbarItem for User Display**
   - Create custom Docusaurus NavbarItem
   - Read from localStorage
   - Show avatar + name or "Login" button

2. **Implement OAuth**
   - Add GitHub OAuth in FastAPI
   - Add Google OAuth
   - Update frontend buttons

3. **Add Rate Limiting**
   - Use slowapi or Redis-based limiting
   - Protect auth and RAG endpoints

4. **Improve Personalization**
   - Add onboarding questionnaire
   - Store reading history
   - ML-based recommendations

5. **Add Tests**
   - pytest for backend
   - Cypress for frontend E2E
   - CI/CD pipeline

---

## Quick Reference Card

### Start Development

```bash
# Frontend (Terminal 1)
npm start

# Backend (Terminal 2)
cd backend
python -m uvicorn main:app --reload
```

### Test Login API

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456","name":"Test"}'

# Login
curl -X POST http://localhost:8000/api/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'

# Get Current User
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Environment Variables

```env
# Required
DATABASE_URL=postgresql://user:pass@host/db
AUTH_SECRET=your_32_character_secret_key

# Optional
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
```

---

*Document generated: December 16, 2025*
*Project: Physical AI & Humanoid Robotics - AI-Native Textbook*
