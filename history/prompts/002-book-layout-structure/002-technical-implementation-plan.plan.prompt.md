---
id: 002
title: Technical Implementation Plan Created
stage: plan
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-book-layout-structure
branch: 002-book-layout-structure
user: user
command: /sp.plan
labels: ["plan", "architecture", "rag", "personalization", "fastapi", "qdrant", "docusaurus"]
links:
  spec: specs/002-book-layout-structure/spec.md
  plan: specs/002-book-layout-structure/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-book-layout-structure/plan.md
tests:
  - Constitution Check (all 5 principles PASS)
---

## Prompt

/sp.plan Physical AI & Humanoid Robotics Book (Technical Plan)

Use the business requirements and course specification from the Physical AI & Humanoid Robotics textbook project to create the technical execution plan for building the complete book and integrated RAG system using Docusaurus, Spec-Kit Plus, Claude Code, and additional hackathon features.

This plan must define architecture, structure, research methodology, decisions, and validation testing for the entire project.

[Full prompt includes detailed requirements for: Architecture Sketch (Content, Book Production, RAG Chatbot, Personalization & Translation), Section Structure, Research Approach, Quality Validation Plan, Architectural Decisions, Testing Strategy, Phase Organization]

## Response snapshot

Created comprehensive technical implementation plan (1199 lines) for AI-native Physical AI & Humanoid Robotics textbook with integrated RAG chatbot, personalization engine, and translation capabilities.

**Architecture Defined**:

1. **Frontend**: Docusaurus v3 static site (GitHub Pages)
   - 4 modules (ROS 2, Digital Twin, Isaac, VLA)
   - 3 support sections (Foundations, Hardware, Capstone)
   - Modular Markdown structure with clear boundaries

2. **Backend**: FastAPI + Qdrant + Neon Postgres + Better-Auth
   - RAG chatbot (two modes: book-wide Q&A, selection-based Q&A)
   - Personalization engine (hardware-based content adaptation)
   - Translation service (Urdu with caching)

3. **Tech Stack**:
   - TypeScript 5.7.2, Python 3.11+, Node.js 20+
   - Docusaurus 3.6.3, FastAPI 0.100+, Qdrant Client 1.7+
   - Neon Serverless Postgres, OpenAI SDK, LangChain
   - Better-Auth for user authentication

**Five Major Architectural Decisions**:

1. **Simulation Strategy**: Isaac Sim primary with Gazebo fallback, local RTX GPU recommended
2. **Hardware Pathways**: Configurable Jetson Orin (Nano vs NX) based on module completion
3. **VLA Architecture**: Skill primitive layer (navigate_to, pick_object, scan_environment, speak)
4. **RAG Architecture**: Qdrant embeddings (500-1000 token chunks, OpenAI text-embedding-3-small)
5. **Formatting Standards**: Mermaid diagrams, APA citations, beginner-friendly code comments

**Project Structure**:
- docs/ → Modular Markdown (module-1-ros2/, module-2-digital-twin/, module-3-isaac/, module-4-vla/, capstone/)
- backend/ → FastAPI (api/rag/, api/personalization/, api/translation/, services/, models/)
- src/components/ → RAGChatWidget.tsx, PersonalizationBar.tsx, TranslationButton.tsx

**Research Tasks** (Phase 0):
- R1. ROS 2 Core Concepts (Nodes, Topics, Services, Actions, URDF)
- R2. Gazebo vs Unity comparison
- R3. Isaac Sim architecture
- R4. VLA pipeline best practices
- R5. Qdrant + Neon setup
- R6. Better-Auth integration
- R7. Translation pipeline
- R8. Hardware specifications

**Design Artifacts** (Phase 1):
- data-model.md: Content entities (Module, Section, Citation) + User entities (UserProfile, ReadingProgress, RAGQueryLog)
- contracts/: 3 OpenAPI YAML files (rag-api.yaml, personalization-api.yaml, translation-api.yaml)
- quickstart.md: Step-by-step setup for frontend + backend + content authoring workflow

**Constitution Compliance**: ✅ ALL 5 PRINCIPLES PASS
- Spec-Driven Writing, Technical Accuracy, Beginner-Friendly Style, Reproducibility, AI-Native Modularity

**Performance Goals**:
- Page load <2s, RAG query <3s, translation <5s
- Support 100 concurrent readers (free tier limits)

**Constraints**:
- Qdrant Cloud Free Tier (1GB), Neon Free Tier (512MB)
- GitHub Pages static hosting only
- APA citations required for all technical claims

**Phase 0 Output**: research.md (8 research tasks with authoritative sources)
**Phase 1 Output**: data-model.md, 3 API contracts, quickstart.md, updated CLAUDE.md
**Phase 2**: Ready for /sp.tasks (tasks generation)

## Outcome

- ✅ Impact: Complete technical architecture and implementation plan for AI-native technical textbook; defines RAG, personalization, translation systems; establishes research-concurrent workflow
- 🧪 Tests: Constitution Check passed (all 5 principles), architectural decisions documented with tradeoffs
- 📁 Files: Created plan.md (1199 lines) in specs/002-book-layout-structure/
- 🔁 Next prompts: Phase 0 - Research (8 tasks), Phase 1 - Design artifacts (data-model.md, contracts/, quickstart.md), `/sp.tasks` for task breakdown
- 🧠 Reflection: Comprehensive plan successfully defines hybrid architecture (static Docusaurus + dynamic FastAPI backend). Key decisions documented with ADR suggestions. Ready for research and implementation phases.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed with all required sections
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 5 principles validated)
- Prompt variant (if applicable): Extended /sp.plan with detailed architecture requirements (RAG, personalization, translation)
- Next experiment (smallest change to try): Execute Phase 0 research tasks in parallel for faster validation; test whether research-concurrent workflow (research while drafting) maintains citation quality
