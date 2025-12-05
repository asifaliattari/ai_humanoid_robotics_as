# Implementation Plan: Physical AI & Humanoid Robotics Book

**Branch**: `002-book-layout-structure` | **Date**: 2025-12-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-book-layout-structure/spec.md`

## Summary

Build an AI-native technical textbook covering Physical AI and Humanoid Robotics using Docusaurus v3, structured around four core modules (ROS 2, Digital Twin, NVIDIA Isaac, Vision-Language-Action). The book includes integrated RAG chatbot, personalization engine, and translation capabilities. This iteration (Iteration 1) focuses on establishing the book structure, content architecture, and AI-native infrastructure without detailed tutorial content.

**Primary Requirement**: Create high-level book layout with clear navigation, module relationships, and hardware requirements that serves as blueprint for detailed content creation in Iteration 2.

**Technical Approach**: Docusaurus-based static site with modular Markdown content, FastAPI backend for RAG/personalization services, Qdrant for vector search, Neon Postgres for user data, and Better-Auth for authentication. Content follows spec-driven lifecycle with research-concurrent workflow.

## Technical Context

**Language/Version**: TypeScript 5.7.2 (Docusaurus frontend), Python 3.11+ (FastAPI backend), Node.js 20+
**Primary Dependencies**:
- Frontend: Docusaurus 3.6.3, React 18.3.1, MDX 3.1.0
- Backend: FastAPI 0.100+, Qdrant Client 1.7+, Neon Postgres (serverless), OpenAI SDK 1.0+
- Auth: Better-Auth (latest), LangChain 0.1+ (RAG pipeline)
**Storage**:
- Content: Markdown files in Docusaurus docs/ structure
- Vectors: Qdrant Cloud Free Tier (1GB)
- User data: Neon Serverless Postgres (512MB free tier)
**Testing**: Jest (frontend), pytest (backend), Docusaurus build validation
**Target Platform**: Web (GitHub Pages for book, cloud-hosted backend for RAG/personalization)
**Project Type**: Hybrid (static site + API backend)
**Performance Goals**:
- Page load <2s, RAG query <3s, translation <5s
- Support 100 concurrent readers (free tier limits)
**Constraints**:
- Free tier limitations (Qdrant 1GB, Neon 512MB)
- GitHub Pages static hosting (no server-side rendering)
- Markdown-only content (Docusaurus compatible)
- APA citations required for all technical claims
**Scale/Scope**:
- 4 modules + 3 support sections = ~7-10 major doc pages (Iteration 1)
- Iteration 2: 30-50 detailed chapter pages
- Target: 500-1000 pages when complete

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Writing
✅ **PASS**: This plan follows `/sp.specify` (spec.md) which defines all requirements. All content creation will have corresponding specs before writing.

### Principle II: Technical Accuracy
✅ **PASS**: Research phase (Phase 0) will validate all technical claims against official documentation (ROS 2, Gazebo, Unity, Isaac, Whisper). APA citations required.

### Principle III: Beginner-Friendly Style
✅ **PASS**: Spec targets beginner-to-intermediate learners. Content structure includes conceptual overviews before technical details. Personalization engine will adjust difficulty based on user experience level.

### Principle IV: Reproducibility
✅ **PASS**: Quickstart.md will provide step-by-step setup. All commands and workflows will be tested. GitHub repo enables version control and reproducibility.

### Principle V: AI-Native Modularity
✅ **PASS**: Modular Markdown structure with clear boundaries. RAG-friendly chunking. Personalization and translation engines support dynamic content modification without breaking structure.

**Constitution Compliance**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/002-book-layout-structure/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (research findings)
├── data-model.md        # Phase 1 output (content + user data models)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   ├── rag-api.yaml           # RAG chatbot endpoints
│   ├── personalization-api.yaml # Personalization endpoints
│   └── translation-api.yaml   # Translation endpoints
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Docusaurus Book Structure
docs/
├── intro.md                    # Physical AI Foundations + Book Overview
├── learning-outcomes.md        # Learning objectives across all modules
├── hardware-requirements.md    # Simulation Rig, Jetson, Robot Lab
├── module-1-ros2/
│   ├── _category_.json         # "Module 1: Robotic Nervous System (ROS 2)"
│   ├── index.md                # Module overview
│   ├── conceptual-overview.md
│   ├── architecture-diagram.md
│   ├── learning-outcomes.md
│   ├── key-concepts.md
│   └── capstone-contribution.md
├── module-2-digital-twin/
│   ├── _category_.json         # "Module 2: Digital Twin (Gazebo & Unity)"
│   ├── index.md
│   ├── conceptual-overview.md
│   ├── architecture-diagram.md
│   ├── learning-outcomes.md
│   ├── key-concepts.md
│   └── capstone-contribution.md
├── module-3-isaac/
│   ├── _category_.json         # "Module 3: AI-Robot Brain (NVIDIA Isaac)"
│   ├── index.md
│   ├── conceptual-overview.md
│   ├── architecture-diagram.md
│   ├── learning-outcomes.md
│   ├── key-concepts.md
│   └── capstone-contribution.md
├── module-4-vla/
│   ├── _category_.json         # "Module 4: Vision-Language-Action"
│   ├── index.md
│   ├── conceptual-overview.md
│   ├── architecture-diagram.md
│   ├── learning-outcomes.md
│   ├── key-concepts.md
│   └── capstone-contribution.md
└── capstone/
    ├── index.md                # Autonomous Humanoid overview
    ├── voice-to-action-pipeline.md
    ├── simulation-flow.md
    └── real-world-deployment.md

# RAG + Personalization Backend
backend/
├── api/
│   ├── rag/
│   │   ├── book_wide_qa.py     # Full book Q&A endpoint
│   │   └── selection_qa.py     # Highlighted text Q&A endpoint
│   ├── personalization/
│   │   ├── user_profile.py     # User hardware/experience profile
│   │   └── content_adapter.py  # Dynamic content adjustment
│   └── translation/
│       └── translate.py        # Urdu translation endpoint
├── services/
│   ├── embedding.py            # Qdrant embedding service
│   ├── retrieval.py            # RAG retrieval logic
│   └── auth.py                 # Better-Auth integration
├── models/
│   ├── user.py                 # User schema (Neon Postgres)
│   └── content.py              # Content metadata schema
├── config.py                   # Environment config
├── main.py                     # FastAPI app entry
└── requirements.txt

# Docusaurus Configuration
docusaurus.config.ts            # Site config (updated from 001-initial-setup)
sidebars.ts                     # Sidebar structure (updated for modules)
src/
├── components/
│   ├── RAGChatWidget.tsx       # Integrated chatbot UI
│   ├── PersonalizationBar.tsx  # Hardware/experience selector
│   └── TranslationButton.tsx   # "Translate to Urdu" button
└── css/
    └── custom.css              # Styles for new components

# Infrastructure
.github/
└── workflows/
    ├── deploy.yml              # Existing GitHub Pages deployment
    ├── backend-deploy.yml      # Backend deployment (Railway/Vercel)
    └── embeddings-update.yml   # Regenerate embeddings on content change
```

**Structure Decision**: Hybrid architecture with static Docusaurus frontend (GitHub Pages) and cloud-hosted FastAPI backend (Railway or Vercel). This separates content delivery (fast, cacheable) from AI services (dynamic, requires compute). Docusaurus `docs/` structure follows modular pattern with clear category boundaries. Each module is independently navigable and can be expanded in Iteration 2 without restructuring.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitution principles pass without justification needed.

## Architectural Decisions

### Decision 1: Simulation Strategy

**Context**: Book covers three simulation tools (Gazebo, Unity, Isaac Sim). Need to determine emphasis and local vs. cloud recommendations.

**Options**:

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. Gazebo-primary | Focus on Gazebo (ROS 2 native), Unity secondary, Isaac for advanced | + ROS 2 integration seamless<br>+ Lightweight, runs on modest hardware<br>- Limited photorealism<br>- Less industry momentum than Isaac |
| B. Isaac-primary | Focus on Isaac Sim, Gazebo for basics, Unity for visualization | + Industry standard (NVIDIA momentum)<br>+ Photorealistic, best sim-to-real<br>- Requires RTX GPU (expensive)<br>- Steeper learning curve |
| C. Balanced coverage | Equal weight to all three based on use case | + Readers choose based on hardware<br>+ Covers all major tools<br>- More content to maintain<br>- Can confuse beginners |

**Recommended Choice**: **Option B (Isaac-primary)** with fallback paths

**Rationale**:
- Aligns with "Physical AI & Humanoid Robotics" positioning (cutting-edge)
- Isaac Sim is industry direction (NVIDIA Jetson ecosystem integration)
- Module 3 dedicated to Isaac justifies depth
- Gazebo covered in Module 2 as foundational/accessible option
- Personalization engine can adapt content for readers without RTX GPUs (suggest cloud options, Gazebo alternatives)

**Local vs Cloud**:
- **Recommended**: Local RTX GPU for Isaac Sim (best performance)
- **Fallback**: Cloud GPU instances (AWS, RunPod) with latency considerations documented
- **Budget Path**: Gazebo-only workflow with note that Isaac content is conceptual until hardware available

**ADR**: This decision is architecturally significant and should be documented via `/sp.adr "Simulation Strategy - Isaac Primary with Fallback Paths"` after plan approval.

---

### Decision 2: Hardware Pathways

**Context**: Readers have varying budgets and access to hardware. Book must support proxy → miniature → premium progression.

**Options**:

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. Jetson Orin Nano | $499, 40 TOPS, 8GB RAM | + Affordable entry point<br>+ Sufficient for Nav2, basic perception<br>- Limited for heavy Isaac ROS workloads<br>- May bottleneck VLA experiments |
| B. Jetson Orin NX | $899, 100 TOPS, 16GB RAM | + Handles Isaac ROS perception well<br>+ VLA workloads feasible<br>- 2x cost of Nano<br>- Overkill for ROS 2 basics |
| C. Configurable path | Recommend based on modules reader wants to complete | + Cost-effective for partial completion<br>+ Personalization-friendly<br>- Requires clear decision tree<br>- May confuse beginners |

**Recommended Choice**: **Option C (Configurable path)** with clear decision tree

**Rationale**:
- Module 1 (ROS 2): No Jetson required (simulation only)
- Module 2 (Digital Twin): No Jetson required (simulation only)
- Module 3 (Isaac): Jetson Orin NX recommended (Isaac ROS perception)
- Module 4 (VLA): Jetson Orin NX required (multimodal perception + LLM)

**Decision Tree**:
```
If (completing Modules 1-2 only) → No Jetson needed
If (completing Module 3) → Orin Nano sufficient (with caveats)
If (completing Module 4 or Capstone) → Orin NX required
If (budget constrained) → Cloud Jetson instances or delay physical deployment
```

**Robot Options**:

| Robot | Cost | Use Case |
|-------|------|----------|
| Proxy (Torso Kit) | $200-500 | Upper-body manipulation, tabletop tasks |
| Unitree Go2 | $1,600 | Quadruped, navigation, perception |
| Robotis OP3 | $10,000 | Bipedal humanoid, full-body control |
| Unitree G1 | $16,000 | Advanced humanoid, industry-grade |

**Recommended**: Proxy → Go2 → OP3/G1 progression. Personalization engine asks user's robot (or "simulation only") and adjusts chapter content accordingly.

**ADR**: This decision affects user experience significantly and should be documented via `/sp.adr "Hardware Pathways - Configurable Jetson and Robot Progression"`.

---

### Decision 3: Software Architecture - VLA Action Representation

**Context**: Module 4 (VLA) requires defining how LLM plans translate to robot actions.

**Options**:

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. Direct ROS Actions | LLM outputs ROS 2 Action names (e.g., "NavigateToGoa") | + Simple, direct ROS 2 integration<br>+ No intermediate representation<br>- LLM must know exact action names<br>- Brittle to action interface changes |
| B. Semantic action layer | LLM outputs semantic intents (e.g., "go to kitchen"), middleware translates to ROS Actions | + LLM-friendly natural language<br>+ Decouples LLM from ROS specifics<br>- Requires custom middleware<br>- More complexity to maintain |
| C. Skill primitives | LLM composes predefined skills (pick, place, navigate, search) | + Reusable skill library<br>+ Middle ground between A and B<br>- Requires skill ontology design<br>- May limit expressiveness |

**Recommended Choice**: **Option C (Skill primitives)** with extensible ontology

**Rationale**:
- Balances LLM usability (names skills naturally) with ROS 2 integration (skills map to Actions/Services)
- Aligns with embodied AI best practices (skill-based planning)
- Skill library can grow in Iteration 2 (basic skills in conceptual content, detailed implementations in tutorials)
- Example skills: `navigate_to(location)`, `pick_object(target)`, `scan_environment()`, `speak(text)`

**Navigation**: Use Nav2 (ROS 2 standard) for navigation skills. Custom planners only for advanced extensions (out of scope for Iteration 1).

**ADR**: This decision defines the VLA architecture and should be documented via `/sp.adr "VLA Action Representation - Skill Primitive Layer"`.

---

### Decision 4: RAG & Auth Architecture

**Context**: RAG chatbot requires embeddings, retrieval, and user personalization. Need to define storage and query strategy.

#### 4.1 Embedding Strategy

**Chunk Size**:
- **Recommended**: 500-1000 tokens per chunk with 100-token overlap
- **Rationale**: Balances context (enough for concept explanation) with retrieval precision (not too broad)

**Metadata Fields**:
```json
{
  "module": "module-1-ros2",
  "section": "key-concepts",
  "topic": "ROS 2 Topics",
  "difficulty": "beginner",
  "requires_hardware": false,
  "keywords": ["ROS 2", "pub-sub", "topics", "messages"]
}
```

**Embedding Model**: OpenAI `text-embedding-3-small` (1536 dimensions, cost-effective)

#### 4.2 Personalization Logic

**User Profile Schema** (Neon Postgres):
```sql
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP,
  -- Hardware
  has_rtx_gpu BOOLEAN,
  has_jetson BOOLEAN,
  jetson_model VARCHAR(50), -- 'orin-nano', 'orin-nx', null
  robot_type VARCHAR(50),   -- 'none', 'proxy', 'go2', 'op3', 'g1'
  -- Experience
  ros2_experience VARCHAR(20), -- 'none', 'beginner', 'intermediate', 'advanced'
  ml_experience VARCHAR(20),
  robotics_experience VARCHAR(20),
  -- Preferences
  preferred_language VARCHAR(10) DEFAULT 'en',
  theme VARCHAR(20) DEFAULT 'light'
);
```

**Personalization Rules**:
1. If `has_rtx_gpu = false` → Show cloud GPU alternatives in Isaac module
2. If `has_jetson = false` → Emphasize simulation-first workflow
3. If `robot_type = 'none'` → Focus on simulation validation, defer physical deployment
4. If `ros2_experience = 'none'` → Add beginner prerequisites to Module 1
5. If `ml_experience = 'advanced'` → Link to advanced VLA papers, reduce LLM basics

**Content Injection Points**: Personalized content injected via Docusaurus custom components (`<PersonalizationBlock>`). Backend API returns adapted content based on user profile.

#### 4.3 RAG Query Modes

**Mode 1: Book-wide Q&A**
```
POST /api/rag/book-qa
{
  "query": "How do I integrate LLMs with ROS 2 actions?",
  "user_id": "uuid",
  "filters": {
    "modules": ["module-1-ros2", "module-4-vla"],
    "difficulty": "beginner"
  }
}
```
- Searches entire book embeddings (filtered by user profile if authenticated)
- Returns top-k relevant chunks with source citations
- Uses retrieved context + LLM to synthesize answer

**Mode 2: Selection-based Q&A**
```
POST /api/rag/selection-qa
{
  "selected_text": "ROS 2 Actions provide a mechanism...",
  "query": "Can you explain this in simpler terms?",
  "user_id": "uuid"
}
```
- Uses `selected_text` as primary context (no vector search)
- LLM answers based only on provided selection
- Useful for clarifications, simplifications, translations of specific paragraphs

**ADR**: RAG architecture decisions should be documented via `/sp.adr "RAG Architecture - Qdrant Embeddings with Two-Mode Query"`.

---

### Decision 5: Book Formatting Standards

**Context**: Complex diagrams, code blocks, and multi-modal content require formatting standards.

**Diagrams**:
- **Recommended**: Mermaid (Docusaurus native support)
- **Alternative**: Excalidraw (hand-drawn style) exported as SVG
- **Architecture diagrams**: Mermaid flowcharts and sequence diagrams
- **Conceptual diagrams**: Custom SVG or Excalidraw

**Code Blocks**:
- **Language tags required**: Always specify language (`python`, `bash`, `yaml`)
- **Comments**: Include conceptual comments for beginner audience
- **Example format**:
  ```python
  # File: voice_action_bridge.py
  # Purpose: Translates speech to ROS 2 actions using Whisper + LLM

  import rclpy
  from openai import OpenAI
  ```

**Citations (APA)**:
```markdown
The Nav2 stack provides ... (Macenski et al., 2020).

## References

Macenski, S., Martín, F., White, R., & Ginés Clavero, J. (2020). The Marathon 2: A Navigation System. *IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*.
```

**ADR**: Not architecturally significant, no ADR needed. Document in content style guide (Iteration 2).

---

## Phase 0: Research (Outline & Knowledge Gathering)

**Purpose**: Resolve technical unknowns and gather authoritative sources for content accuracy.

### Research Tasks

| Task | Goal | Sources | Output |
|------|------|---------|--------|
| R1. ROS 2 Core Concepts | Validate Nodes, Topics, Services, Actions, URDF concepts | ROS 2 documentation (docs.ros.org), ROS 2 Design docs | Conceptual definitions + official citations |
| R2. Gazebo vs Unity | Compare simulation capabilities, ROS integration, use cases | Gazebo docs, Unity Robotics Hub | Decision rationale for Module 2 structure |
| R3. Isaac Sim Architecture | Understand Isaac Sim + Isaac ROS integration, VSLAM capabilities | NVIDIA Isaac docs, Isaac ROS GitHub | Module 3 content boundaries |
| R4. VLA Pipeline Best Practices | Research LLM-to-action patterns, Whisper integration, skill primitives | OpenAI docs, RT-1/RT-2 papers, embodied AI research | VLA architecture validation |
| R5. Qdrant + Neon Setup | Confirm free tier limits, API patterns, Postgres schema design | Qdrant Cloud docs, Neon docs | Backend implementation constraints |
| R6. Better-Auth Integration | User profile storage, Docusaurus integration patterns | Better-Auth docs, Docusaurus auth plugins | Auth flow design |
| R7. Translation Pipeline | LLM translation quality for technical content, caching strategy | OpenAI GPT-4 translation examples, i18n best practices | Translation API design |
| R8. Hardware Specifications | Validate Jetson Orin models, RTX GPU requirements, robot specs | NVIDIA Jetson docs, Unitree specs, Robotis docs | Hardware requirements accuracy |

### Research Concurrent Workflow

**Timing**: Research happens **during content drafting**, not upfront.
- Module 1 research → Draft Module 1 content → Validate citations
- Module 2 research → Draft Module 2 content → Validate citations
- (Continue for Modules 3, 4)

**Research Validation**:
- All factual claims must link to authoritative source (APA citation)
- Official documentation preferred over blog posts or tutorials
- If official docs unclear, mark as `[NEEDS CLARIFICATION: <specific question>]` and research alternatives

### Research Output: `research.md`

**Format**:
```markdown
# Research Findings: Physical AI & Humanoid Robotics Book

## R1. ROS 2 Core Concepts

**Decision**: Use ROS 2 Humble (LTS) as reference version

**Rationale**: Humble is Long-Term Support (until 2027), widely adopted, stable for educational content

**Alternatives Considered**:
- ROS 2 Foxy (older LTS, less relevant)
- ROS 2 Iron (newer, not LTS)

**Sources**:
- Open Robotics. (2023). *ROS 2 Humble Documentation*. Retrieved from https://docs.ros.org/en/humble/
- Macenski, S., & Foote, T. (2021). *ROS 2 Design Principles*. Open Robotics Technical Report.

**Key Concepts Validated**:
- Nodes: Independent processes communicating via middleware
- Topics: Pub/sub message passing (one-to-many)
- Services: Request/response (one-to-one, synchronous)
- Actions: Goal-based asynchronous operations with feedback
- URDF: XML robot description format

## R2. Gazebo vs Unity

[Continue for each research task...]
```

**STOP**: Phase 0 complete when `research.md` exists with all 8 research tasks documented and all `NEEDS CLARIFICATION` markers resolved.

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete, all technical unknowns resolved

### 1.1 Data Model Design

**Purpose**: Define content structure and user data schemas

#### Content Entities

```markdown
# Content Data Model

## Entity: Module
**Purpose**: Top-level learning unit

**Attributes**:
- `id` (string): Unique identifier (e.g., "module-1-ros2")
- `title` (string): Display name (e.g., "Module 1: Robotic Nervous System (ROS 2)")
- `order` (integer): Sequence number (1-4)
- `description` (string): Brief overview
- `prerequisites` (array<string>): Module IDs required before this (e.g., Module 3 requires Module 1)
- `learning_outcomes` (array<string>): What readers will learn
- `sections` (array<Section>): Child sections

**Relationships**:
- Contains multiple Sections
- May depend on other Modules (prerequisites)

## Entity: Section
**Purpose**: Sub-unit within a module (e.g., "Conceptual Overview", "Key Concepts")

**Attributes**:
- `id` (string): Unique identifier (e.g., "module-1-ros2/key-concepts")
- `title` (string): Display name
- `content` (markdown): Main content body
- `difficulty` (enum): beginner | intermediate | advanced
- `requires_hardware` (boolean): Whether this section needs physical hardware
- `hardware_types` (array<string>): Specific hardware if required (e.g., ["rtx-gpu", "jetson-orin-nx"])
- `keywords` (array<string>): For search and RAG retrieval

**Relationships**:
- Belongs to one Module
- May reference other Sections (cross-links)

## Entity: HardwareRequirement
**Purpose**: Hardware spec referenced in content

**Attributes**:
- `id` (string): "rtx-gpu", "jetson-orin-nano", etc.
- `category` (enum): simulation_rig | edge_ai_kit | sensors | robot_platform
- `name` (string): Display name
- `cost_range` (string): "$200-500", "$1000+", etc.
- `required_for` (array<string>): Module IDs requiring this hardware
- `alternatives` (array<string>): Alternative hardware IDs or cloud options

## Entity: Citation
**Purpose**: APA-formatted source reference

**Attributes**:
- `id` (string): Short reference key (e.g., "macenski2020")
- `authors` (string): APA author list
- `year` (integer)
- `title` (string)
- `publication` (string): Journal, conference, or URL
- `url` (string): Direct link to source
- `access_date` (string): For web sources
```

#### User Data Model

```markdown
# User Data Model

## Entity: UserProfile (Neon Postgres)
**Purpose**: Store user preferences and hardware inventory

**Schema** (see Decision 4.2 for SQL schema)

**Validation Rules**:
- Email must be unique and valid format
- Jetson model must be from allowed list: ['orin-nano', 'orin-nx', null]
- Robot type must be from allowed list: ['none', 'proxy', 'go2', 'op3', 'g1']
- Experience levels must be from allowed list: ['none', 'beginner', 'intermediate', 'advanced']

**State Transitions**:
1. User signs up → Profile created with defaults (all hardware = false, experience = 'none')
2. User completes onboarding survey → Hardware and experience fields populated
3. User updates profile anytime → Fields updated, personalization re-evaluated

## Entity: ReadingProgress
**Purpose**: Track which modules/sections user has completed

**Schema**:
```sql
CREATE TABLE reading_progress (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES user_profiles(id),
  section_id VARCHAR(255), -- e.g., "module-1-ros2/key-concepts"
  completed_at TIMESTAMP,
  time_spent_seconds INTEGER
);
```

## Entity: RAGQueryLog
**Purpose**: Track chatbot interactions for quality improvement

**Schema**:
```sql
CREATE TABLE rag_query_log (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES user_profiles(id),
  query_text TEXT,
  query_mode VARCHAR(50), -- 'book-wide' or 'selection-based'
  retrieved_chunks JSONB, -- Array of {section_id, score}
  response_text TEXT,
  user_feedback VARCHAR(20), -- 'helpful', 'not-helpful', null
  created_at TIMESTAMP
);
```
```

**Output**: `data-model.md` in `specs/002-book-layout-structure/`

---

### 1.2 API Contracts

**Purpose**: Define backend API endpoints for RAG, personalization, and translation

#### Contract 1: RAG API

**File**: `specs/002-book-layout-structure/contracts/rag-api.yaml`

```yaml
openapi: 3.0.3
info:
  title: Physical AI Book - RAG Chatbot API
  version: 1.0.0
  description: Retrieval-Augmented Generation API for book Q&A

servers:
  - url: https://api.physical-ai-book.com/v1
    description: Production backend

paths:
  /rag/book-qa:
    post:
      summary: Book-wide Q&A
      description: Answer questions using entire book content via vector search
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - query
              properties:
                query:
                  type: string
                  example: "How do I integrate LLMs with ROS 2 actions?"
                user_id:
                  type: string
                  format: uuid
                  description: Optional for personalized results
                filters:
                  type: object
                  properties:
                    modules:
                      type: array
                      items:
                        type: string
                      example: ["module-1-ros2", "module-4-vla"]
                    difficulty:
                      type: string
                      enum: [beginner, intermediate, advanced]
                    requires_hardware:
                      type: boolean
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  answer:
                    type: string
                    description: LLM-generated answer
                  sources:
                    type: array
                    items:
                      type: object
                      properties:
                        section_id:
                          type: string
                        title:
                          type: string
                        relevance_score:
                          type: number
                        excerpt:
                          type: string
                  query_id:
                    type: string
                    format: uuid

  /rag/selection-qa:
    post:
      summary: Selection-based Q&A
      description: Answer questions about user-highlighted text
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - selected_text
                - query
              properties:
                selected_text:
                  type: string
                  description: Text highlighted by user
                query:
                  type: string
                  example: "Can you explain this in simpler terms?"
                user_id:
                  type: string
                  format: uuid
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  answer:
                    type: string
                  query_id:
                    type: string
                    format: uuid
```

#### Contract 2: Personalization API

**File**: `specs/002-book-layout-structure/contracts/personalization-api.yaml`

```yaml
openapi: 3.0.3
info:
  title: Physical AI Book - Personalization API
  version: 1.0.0

paths:
  /personalization/profile:
    get:
      summary: Get user profile
      parameters:
        - name: user_id
          in: query
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: User profile
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserProfile'

    put:
      summary: Update user profile
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserProfile'
      responses:
        '200':
          description: Profile updated

  /personalization/adapt-content:
    post:
      summary: Get personalized content version
      description: Returns adapted content based on user's hardware and experience
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - section_id
                - user_id
              properties:
                section_id:
                  type: string
                user_id:
                  type: string
                  format: uuid
      responses:
        '200':
          description: Personalized content
          content:
            application/json:
              schema:
                type: object
                properties:
                  original_content:
                    type: string
                    description: Markdown content
                  personalized_blocks:
                    type: array
                    items:
                      type: object
                      properties:
                        insert_after:
                          type: string
                          description: Heading or marker to insert after
                        content:
                          type: string
                          description: Personalized markdown block

components:
  schemas:
    UserProfile:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
        has_rtx_gpu:
          type: boolean
        has_jetson:
          type: boolean
        jetson_model:
          type: string
          enum: [orin-nano, orin-nx, null]
        robot_type:
          type: string
          enum: [none, proxy, go2, op3, g1]
        ros2_experience:
          type: string
          enum: [none, beginner, intermediate, advanced]
        ml_experience:
          type: string
          enum: [none, beginner, intermediate, advanced]
        robotics_experience:
          type: string
          enum: [none, beginner, intermediate, advanced]
```

#### Contract 3: Translation API

**File**: `specs/002-book-layout-structure/contracts/translation-api.yaml`

```yaml
openapi: 3.0.3
info:
  title: Physical AI Book - Translation API
  version: 1.0.0

paths:
  /translation/translate:
    post:
      summary: Translate section to target language
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - section_id
                - target_language
              properties:
                section_id:
                  type: string
                target_language:
                  type: string
                  enum: [ur] # Urdu for now, expand later
                user_id:
                  type: string
                  format: uuid
                  description: For caching preferences
      responses:
        '200':
          description: Translated content
          content:
            application/json:
              schema:
                type: object
                properties:
                  translated_content:
                    type: string
                    description: Markdown with translated text, code blocks unchanged
                  cache_hit:
                    type: boolean
                    description: Whether result was cached
                  translation_time_ms:
                    type: integer

  /translation/supported-languages:
    get:
      summary: Get supported languages
      responses:
        '200':
          description: List of supported language codes
          content:
            application/json:
              schema:
                type: object
                properties:
                  languages:
                    type: array
                    items:
                      type: object
                      properties:
                        code:
                          type: string
                          example: "ur"
                        name:
                          type: string
                          example: "Urdu"
```

**Output**: 3 OpenAPI YAML files in `specs/002-book-layout-structure/contracts/`

---

### 1.3 Quickstart Guide

**Purpose**: Step-by-step setup instructions for developers/content authors

**File**: `specs/002-book-layout-structure/quickstart.md`

```markdown
# Quickstart: Physical AI & Humanoid Robotics Book

This guide helps you set up the development environment for the Physical AI book (Docusaurus frontend + FastAPI backend).

## Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- Git
- (Optional) Docker for backend services

## Frontend Setup (Docusaurus Book)

### 1. Clone Repository

\```bash
git clone https://github.com/YOUR_USERNAME/ai_humanoid_robotics_as.git
cd ai_humanoid_robotics_as
\```

### 2. Install Dependencies

\```bash
npm install
\```

### 3. Run Development Server

\```bash
npm start
\```

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

\```bash
cd backend
\```

### 2. Create Virtual Environment

\```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\```

### 3. Install Dependencies

\```bash
pip install -r requirements.txt
\```

### 4. Configure Environment Variables

Create `.env` file:

\```env
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
\```

### 5. Initialize Database

\```bash
python -m alembic upgrade head
\```

### 6. Generate Embeddings (First Time)

\```bash
python scripts/generate_embeddings.py
\```

This reads all Markdown files from `docs/`, chunks them, and uploads embeddings to Qdrant.

### 7. Run Backend Server

\```bash
uvicorn main:app --reload --port 8000
\```

API available at `http://localhost:8000`.

### 8. Test RAG Endpoint

\```bash
curl -X POST http://localhost:8000/api/rag/book-qa \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
\```

## Content Authoring Workflow

### 1. Create Feature Spec

\```bash
# Always start with a specification
/sp.specify "Add chapter on ROS 2 Services"
\```

### 2. Plan Implementation

\```bash
/sp.plan
\```

### 3. Write Content

Edit Markdown files in `docs/`:
- Follow Docusaurus Markdown format
- Include APA citations for all technical claims
- Add code examples with language tags

### 4. Regenerate Embeddings

\```bash
cd backend
python scripts/generate_embeddings.py --incremental
\```

### 5. Test Locally

\```bash
npm run build
npm run serve
\```

### 6. Commit and Push

\```bash
git add .
git commit -m "feat: add ROS 2 Services chapter"
git push origin <branch-name>
\```

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
- Explore [Plan](specs/002-book-layout-structure/plan.md) (this file's parent) for architecture details
```

**Output**: `quickstart.md` in `specs/002-book-layout-structure/`

---

### 1.4 Agent Context Update

**Purpose**: Update Claude Code context file with technologies introduced in this plan

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**What it does**:
- Reads `CLAUDE.md` (agent-specific context file)
- Appends new technologies between `<!-- CONTEXT_START -->` and `<!-- CONTEXT_END -->` markers
- Preserves manual additions outside markers

**New Technologies to Add**:
- Docusaurus v3 (already present from feature 001)
- FastAPI (backend framework)
- Qdrant (vector database)
- Neon Serverless Postgres
- Better-Auth (authentication)
- ROS 2 Humble (robotics framework - conceptual only, not code)
- OpenAI Embeddings API (for RAG)
- LangChain (RAG pipeline)

**Output**: Updated `CLAUDE.md` with backend stack context

---

## Phase 1 Complete

**Stop and Verify**:
1. ✅ `research.md` exists with all 8 research tasks documented
2. ✅ `data-model.md` defines content and user entities
3. ✅ `contracts/` contains 3 OpenAPI YAML files
4. ✅ `quickstart.md` provides setup instructions
5. ✅ `CLAUDE.md` updated with new technologies

**Constitution Re-Check**:
- ✅ Spec-Driven Writing: Plan follows spec.md requirements
- ✅ Technical Accuracy: Research phase ensures authoritative sources
- ✅ Beginner-Friendly: Quickstart provides clear setup steps
- ✅ Reproducibility: Quickstart enables environment replication
- ✅ AI-Native Modularity: Modular docs structure, RAG-friendly chunking

**All gates pass. Ready for Phase 2 (tasks generation via `/sp.tasks`).**

---

## Phase 2: Implementation Readiness

**Note**: Phase 2 outputs are generated by `/sp.tasks` command, not `/sp.plan`.

This plan provides the foundation for task generation:
- Architecture decisions documented
- API contracts defined
- Data models specified
- Research findings recorded
- Setup instructions written

**Next Command**: `/sp.tasks` will break down implementation into:
1. Foundational tasks (Docusaurus structure, backend scaffolding)
2. Module 1 content tasks (ROS 2 conceptual pages)
3. Module 2 content tasks (Digital Twin conceptual pages)
4. Module 3 content tasks (Isaac conceptual pages)
5. Module 4 content tasks (VLA conceptual pages)
6. RAG backend tasks (FastAPI endpoints, Qdrant setup, embedding generation)
7. Personalization tasks (Better-Auth integration, profile API, content adaptation)
8. Translation tasks (Translation API, Urdu pipeline, caching)
9. Testing and validation tasks

---

## Summary

This implementation plan defines the architecture and design for an AI-native technical textbook covering Physical AI and Humanoid Robotics. The plan establishes:

**Architecture**:
- Docusaurus v3 static site (GitHub Pages)
- FastAPI backend (RAG, personalization, translation)
- Qdrant vector database (embeddings)
- Neon Serverless Postgres (user data)
- Better-Auth (authentication)

**Content Structure**:
- 4 modules (ROS 2, Digital Twin, Isaac, VLA)
- 3 support sections (Foundations, Hardware, Capstone)
- Modular Markdown with clear boundaries

**Key Decisions**:
1. Isaac Sim primary simulation strategy with Gazebo fallback
2. Configurable hardware pathways (Jetson Orin Nano vs NX, robot progression)
3. Skill primitive layer for VLA action representation
4. Two-mode RAG (book-wide + selection-based Q&A)
5. Mermaid diagrams for architecture visualization

**Research Approach**:
- Research-concurrent workflow (research while drafting)
- APA citations for all technical claims
- Official documentation prioritized

**Phase 0 Output**: `research.md` with 8 research tasks documented
**Phase 1 Output**: `data-model.md`, 3 API contracts (OpenAPI), `quickstart.md`

**Constitution Compliance**: All 5 principles pass (Spec-Driven, Technical Accuracy, Beginner-Friendly, Reproducibility, AI-Native Modularity)

**Ready for**: `/sp.tasks` to generate detailed implementation tasks
