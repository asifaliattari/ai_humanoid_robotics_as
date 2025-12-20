---
name: chatbot-qa
description: Develop and enhance the RAG-powered Q&A chatbot features. Use when implementing new chatbot functionality, fixing issues, or improving response quality. Covers both frontend widget and backend API.
allowed_tools: Read, Edit, Write, Bash, Grep, Glob
---

# Chatbot Q&A Development Skill

## Purpose

Develop, maintain, and enhance the AI-powered Q&A chatbot for the Physical AI & Humanoid Robotics textbook.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                       │
│  src/components/RAGChatWidget.tsx                        │
│  - Text selection detection                               │
│  - Chat UI with messages                                  │
│  - Mode switching (book-wide / selection)                │
└──────────────────────────────────────────────────────────┘
                          │
                     REST API
                          │
┌──────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                      │
│  hf-deploy/api/rag/book_qa.py      - Book-wide Q&A       │
│  hf-deploy/api/rag/selection_qa.py - Selection Q&A       │
└──────────────────────────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
┌─────────────────────┐    ┌─────────────────────┐
│    Qdrant Cloud     │    │     OpenAI API      │
│  (Vector Search)    │    │  (Embeddings + GPT) │
└─────────────────────┘    └─────────────────────┘
```

## Key Components

### Frontend Files

| File | Purpose |
|------|---------|
| `src/components/RAGChatWidget.tsx` | Main chat widget component |
| `src/components/RAGChatWidget.css` | Styling for chat widget |
| `src/config/api.ts` | API endpoint configuration |

### Backend Files

| File | Purpose |
|------|---------|
| `hf-deploy/api/rag/book_qa.py` | Book-wide Q&A endpoint |
| `hf-deploy/api/rag/selection_qa.py` | Selection-based Q&A |
| `hf-deploy/services/qdrant_service.py` | Vector database operations |
| `hf-deploy/services/embedding_service.py` | OpenAI embeddings |
| `hf-deploy/config.py` | Configuration settings |

## Common Development Tasks

### 1. Update System Prompts

Location: `hf-deploy/api/rag/book_qa.py` and `selection_qa.py`

```python
system_prompt = """
You are an expert assistant for the Physical AI & Humanoid Robotics textbook.
...
"""
```

### 2. Adjust RAG Parameters

Location: `hf-deploy/config.py`

```python
rag_top_k_results: int = 5        # Number of chunks to retrieve
rag_similarity_threshold: float = 0.1  # Minimum similarity
```

### 3. Regenerate Embeddings

```bash
cd backend
python -m scripts.generate_embeddings
```

### 4. Test API Endpoints

```bash
# Book-wide Q&A
curl -X POST "https://asifaliastolixgen-physical-ai-book-api.hf.space/api/rag/book-qa" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'

# Selection Q&A
curl -X POST "https://asifaliastolixgen-physical-ai-book-api.hf.space/api/rag/selection-qa" \
  -H "Content-Type: application/json" \
  -d '{"selected_text": "ROS 2 is...", "query": "Explain this"}'
```

## Feature Implementation Patterns

### Adding New Chat Mode

1. Define new mode type in `RAGChatWidget.tsx`
2. Create backend endpoint in `hf-deploy/api/rag/`
3. Add API endpoint to `src/config/api.ts`
4. Update frontend to handle new mode

### Improving Response Quality

1. Analyze failed queries in logs
2. Adjust system prompt for edge cases
3. Tune similarity threshold
4. Consider chunk size adjustments

### Language Support

Currently supports:
- English
- Roman Urdu (auto-detected)

To add new language:
1. Update system prompts to include detection
2. Add language examples for GPT guidance

## Debugging Guide

### Frontend Issues

```typescript
// Add console logging
console.log('API Response:', data);
console.log('Selected text:', selectedText);
```

### Backend Issues

```python
# Check logs
logger.info(f"Query: {request.query}")
logger.info(f"Results: {len(search_results)}")
```

### Common Problems

| Issue | Cause | Solution |
|-------|-------|----------|
| No results | Low similarity | Lower threshold |
| Wrong answers | Bad chunks | Regenerate embeddings |
| Slow response | Large context | Reduce top_k |
| CORS errors | Origin blocked | Check allow_origins |

## Deployment

### Push to Hugging Face

```bash
cd hf-deploy
git add .
git commit -m "Update chatbot"
git push
```

### Environment Variables (HF Secrets)

- `OPENAI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `AUTH_SECRET`
