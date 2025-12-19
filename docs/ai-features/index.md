# AI-Native Features

## Overview

This book is **AI-native**: it uses AI not just as a subject of study, but as a tool for learning. The platform includes:

1. **RAG Chatbot** - Ask questions about any topic
2. **User Authentication** - Secure login with JWT

---

## 1. RAG Chatbot

**Purpose**: Answer questions using the entire book as context

**Architecture**:
- **Frontend**: React chat widget (bottom-right floating button)
- **Backend**: FastAPI + Qdrant (vector search) + OpenAI GPT-4
- **Embeddings**: Book content chunked by section, stored in Qdrant with metadata

### Chatbot Modes

#### Mode A: Ask the Full Book
**Use Case**: General questions like "How do ROS 2 Actions work?"

**Pipeline**:
```
User Query → Embed query → Search Qdrant → Retrieve top-k chunks → LLM synthesis → Answer
```

#### Mode B: Ask About Selected Text
**Use Case**: Highlight a paragraph and ask "Explain this in simpler terms"

**Pipeline**:
```
Selected Text + User Query → LLM (no vector search) → Simplified Answer
```

### Example Interactions

**Q**: "What's the difference between ROS 2 Topics and Services?"
**A**: "Topics use pub/sub for one-to-many asynchronous messaging (e.g., broadcasting camera images), while Services use request/response for one-to-one synchronous queries (e.g., asking a planner for a path). See [Module 1: ROS 2](/docs/modules/ros2/)."

---

## 2. User Authentication

**Purpose**: Secure user login and registration

**Features**:
- JWT-based authentication
- Secure password hashing with bcrypt
- User avatar with initials in navbar
- Persistent sessions

**Endpoints**:
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login-json` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

---

## Implementation Details

**Backend**: `backend/`
- `api/auth/`: Authentication endpoints
- `api/rag/`: Chatbot endpoints
- `models/auth.py`: User model

**Frontend**: `src/components/`
- `RAGChatWidget.tsx`: Floating chat button
- `UserNavbarItem/`: User avatar and login

---

## References

Lewis, P., Perez, E., Piktus, A., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS).

OpenAI. (2024). *ChatGPT API Documentation*. Retrieved from https://platform.openai.com/docs/
