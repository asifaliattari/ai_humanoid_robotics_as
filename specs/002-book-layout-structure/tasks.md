# Tasks: Physical AI & Humanoid Robotics Book Layout

**Input**: Design documents from `/specs/002-book-layout-structure/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: Tests are NOT explicitly requested in the feature specification. This feature focuses on content structure and layout (Iteration 1), not implementation testing.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Docusaurus book**: `docs/` (content), `src/` (components), `backend/` (API services)
- **Specs**: `specs/002-book-layout-structure/` (design documents)
- **Configuration**: Root directory (`docusaurus.config.ts`, `sidebars.ts`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for Docusaurus book and backend services

- [ ] T001 Verify Docusaurus 3.6.3 installation and build system in package.json
- [ ] T002 [P] Create backend/ directory structure (api/, services/, models/, config.py, main.py)
- [ ] T003 [P] Create backend/requirements.txt with FastAPI 0.100+, Qdrant Client 1.7+, OpenAI SDK, LangChain, Better-Auth
- [ ] T004 [P] Configure environment variables template in backend/.env.example (QDRANT_URL, DATABASE_URL, OPENAI_API_KEY, AUTH_SECRET)
- [ ] T005 Update docusaurus.config.ts with book-specific metadata (title, tagline, navbar items)
- [ ] T006 Create initial sidebars.ts structure for 4 modules + support sections

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create docs/ folder structure per plan.md (intro.md, learning-outcomes.md, hardware-requirements.md, module-1-ros2/, module-2-digital-twin/, module-3-isaac/, module-4-vla/, capstone/)
- [ ] T008 [P] Create _category_.json files for each module directory with correct titles and positions
- [ ] T009 [P] Initialize backend FastAPI app in backend/main.py with CORS middleware and health check endpoint
- [ ] T010 [P] Setup Neon Postgres connection in backend/config.py with DATABASE_URL from environment
- [ ] T011 [P] Create database schema migrations in backend/migrations/ for user_profiles, reading_progress, rag_query_log, translation_cache tables
- [ ] T012 [P] Setup Qdrant client in backend/services/embedding.py with collection creation logic (1536 dimensions, OpenAI text-embedding-3-small)
- [ ] T013 [P] Create Better-Auth configuration in backend/services/auth.py with user profile hooks
- [ ] T014 [P] Create base models in backend/models/ (user.py, content.py) matching data-model.md schemas
- [ ] T015 Create Docusaurus custom components directory src/components/ for RAGChatWidget.tsx, PersonalizationBar.tsx, TranslationButton.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Reader Navigates Book Structure (Priority: P1) 🎯 MVP

**Goal**: Readers can open the book homepage, view the table of contents, understand the four-module progression, and identify which module addresses their current learning need

**Independent Test**: Reader can navigate to book homepage, see clear module structure in sidebar, and identify that Module 2 (Digital Twin) addresses simulation learning needs

### Implementation for User Story 1

- [ ] T016 [P] [US1] Create docs/intro.md with Physical AI Foundations overview, explaining embodied intelligence vs digital AI per FR-004
- [ ] T017 [P] [US1] Create docs/learning-outcomes.md listing target audience (beginner-to-intermediate) and expected background knowledge
- [ ] T018 [P] [US1] Create docs/module-1-ros2/index.md with Module 1 overview, purpose statement, and relationship to Physical AI (no detailed content yet)
- [ ] T019 [P] [US1] Create docs/module-2-digital-twin/index.md with Module 2 overview, purpose statement, and relationship to simulation
- [ ] T020 [P] [US1] Create docs/module-3-isaac/index.md with Module 3 overview, purpose statement, and NVIDIA Isaac introduction
- [ ] T021 [P] [US1] Create docs/module-4-vla/index.md with Module 4 overview, purpose statement, and Vision-Language-Action introduction
- [ ] T022 [US1] Update sidebars.ts to organize modules in logical progression (ROS 2 → Digital Twin → Isaac → VLA) per FR-002
- [ ] T023 [US1] Add clear module titles and descriptions to navbar in docusaurus.config.ts
- [ ] T024 [US1] Create docs/intro.md homepage with welcome message and "Why Physical AI?" section explaining the four-module approach
- [ ] T025 [US1] Test navigation flow by verifying all module index pages render correctly and sidebar shows correct hierarchy

**Checkpoint**: At this point, readers should be able to navigate the book structure and identify which module addresses their learning needs (SC-001)

---

## Phase 4: User Story 2 - Reader Understands Module Relationships (Priority: P1)

**Goal**: Readers can explain how the four modules connect together to form a complete Physical AI system for humanoid robots

**Independent Test**: Reader can answer "How does VLA use ROS 2?" by referencing module prerequisite statements and capstone integration concept

### Implementation for User Story 2

- [ ] T026 [P] [US2] Create docs/module-1-ros2/conceptual-overview.md explaining ROS 2 as the "robotic nervous system" foundation per FR-006
- [ ] T027 [P] [US2] Create docs/module-1-ros2/key-concepts.md covering Nodes, Topics, Services, Actions, URDF at conceptual level only (no code)
- [ ] T028 [P] [US2] Create docs/module-1-ros2/capstone-contribution.md explaining how ROS 2 provides control infrastructure for autonomous humanoid
- [ ] T029 [P] [US2] Create docs/module-2-digital-twin/conceptual-overview.md explaining simulation purpose and physics concepts per FR-007
- [ ] T030 [P] [US2] Create docs/module-2-digital-twin/key-concepts.md covering Gazebo/Unity simulation, physics, virtual sensors (conceptual only)
- [ ] T031 [P] [US2] Create docs/module-2-digital-twin/capstone-contribution.md explaining how Digital Twin enables safe testing before physical deployment
- [ ] T032 [P] [US2] Create docs/module-3-isaac/conceptual-overview.md explaining Isaac Sim and Isaac ROS integration per FR-008
- [ ] T033 [P] [US2] Create docs/module-3-isaac/key-concepts.md covering photorealistic simulation, VSLAM, Nav2, sim-to-real concepts (conceptual only)
- [ ] T034 [P] [US2] Create docs/module-3-isaac/capstone-contribution.md explaining how Isaac accelerates perception and navigation for humanoid
- [ ] T035 [P] [US2] Create docs/module-4-vla/conceptual-overview.md explaining LLMs as planners and voice-to-action pipelines per FR-009
- [ ] T036 [P] [US2] Create docs/module-4-vla/key-concepts.md covering Whisper, LLM planning, multimodal perception, skill primitives (conceptual only)
- [ ] T037 [P] [US2] Create docs/module-4-vla/capstone-contribution.md explaining how VLA provides cognitive layer for autonomous decision-making
- [ ] T038 [US2] Create docs/capstone/index.md with Capstone concept overview per FR-013
- [ ] T039 [US2] Create docs/capstone/voice-to-action-pipeline.md showing integration: LLM plans → ROS actions → simulated in Digital Twin → accelerated by Isaac
- [ ] T040 [US2] Create docs/capstone/simulation-flow.md with Mermaid diagram showing all four modules integrated in autonomous humanoid workflow
- [ ] T041 [US2] Add prerequisite statements to each module index.md per FR-011 (e.g., Module 3 requires Module 1 understanding)
- [ ] T042 [US2] Test module relationships by verifying cross-references between modules work correctly and prerequisite chain is clear

**Checkpoint**: At this point, readers should understand how all four modules integrate in the Capstone concept (SC-007)

---

## Phase 5: User Story 3 - Reader Assesses Hardware Requirements (Priority: P2)

**Goal**: Readers can create a shopping list of required hardware (simulation rig, edge AI kit, sensors, robot options) based on the Hardware Requirements Summary section

**Independent Test**: Reader can identify they need RTX GPU for Isaac module, Jetson Orin NX for VLA module, and can choose robot platform based on budget

### Implementation for User Story 3

- [ ] T043 [P] [US3] Create docs/hardware-requirements.md with four major categories per FR-005: Simulation Rig, Edge AI Kit, Sensors, Robot Platforms
- [ ] T044 [P] [US3] Add Simulation Rig section to hardware-requirements.md with RTX GPU specs per research.md R8 (min RTX 3070, recommended RTX 4090)
- [ ] T045 [P] [US3] Add Edge AI Kit section to hardware-requirements.md with Jetson Orin decision tree from plan.md Decision 2 (Modules 1-2: none, Module 3: Nano, Module 4: NX)
- [ ] T046 [P] [US3] Add Sensors section to hardware-requirements.md with RealSense, LiDAR, IMU high-level descriptions and purposes
- [ ] T047 [P] [US3] Add Robot Platforms section to hardware-requirements.md with Proxy ($200-500), Go2 ($1,600), OP3 ($10,000), G1 ($16,000) comparisons per plan.md Decision 2
- [ ] T048 [US3] Create hardware categorization table in hardware-requirements.md showing function-based grouping per FR-012
- [ ] T049 [US3] Add "Simulation-First Workflow" note to hardware-requirements.md clarifying Modules 1-2 only need simulation rig (Jetson optional)
- [ ] T050 [US3] Add "Cloud vs On-Prem" section to hardware-requirements.md discussing cloud GPU alternatives (AWS g5/g6e instances) for readers without RTX
- [ ] T051 [US3] Test hardware assessment flow by verifying readers can identify minimum hardware for simulation-only learning vs. full physical deployment

**Checkpoint**: At this point, readers should be able to create categorized hardware shopping list and understand tiered progression (SC-004)

---

## Phase 6: User Story 4 - Content Author Creates Chapter Specs (Priority: P3)

**Goal**: Content authors can use this layout specification to create detailed chapter specifications in Iteration 2 without confusion about boundaries

**Independent Test**: Content author can take Module 1 (ROS 2) from this spec and identify which topics are conceptual overviews (in scope) vs. detailed tutorials (out of scope for Iteration 1)

### Implementation for User Story 4

- [ ] T052 [P] [US4] Create docs/module-1-ros2/architecture-diagram.md placeholder with Mermaid diagram showing ROS 2 node communication architecture (conceptual level)
- [ ] T053 [P] [US4] Create docs/module-1-ros2/learning-outcomes.md listing what readers will learn from Module 1 (understanding ROS patterns, not implementation skills)
- [ ] T054 [P] [US4] Create docs/module-2-digital-twin/architecture-diagram.md placeholder with Gazebo/Unity comparison table and use case mapping
- [ ] T055 [P] [US4] Create docs/module-2-digital-twin/learning-outcomes.md listing simulation concepts readers will understand
- [ ] T056 [P] [US4] Create docs/module-3-isaac/architecture-diagram.md placeholder with Isaac Sim + Isaac ROS integration diagram
- [ ] T057 [P] [US4] Create docs/module-3-isaac/learning-outcomes.md listing NVIDIA Isaac ecosystem understanding goals
- [ ] T058 [P] [US4] Create docs/module-4-vla/architecture-diagram.md placeholder with skill primitive layer diagram per plan.md Decision 3
- [ ] T059 [P] [US4] Create docs/module-4-vla/learning-outcomes.md listing VLA pipeline understanding goals
- [ ] T060 [US4] Add "Content Authoring Guidelines" section to docs/intro.md explaining Iteration 1 vs. Iteration 2 boundaries per spec.md Out of Scope
- [ ] T061 [US4] Create examples in each module showing correct conceptual vs. implementation content boundaries (e.g., "ROS 2 Topics enable pub/sub messaging" vs. "rclpy.Publisher() code example")
- [ ] T062 [US4] Add APA citation examples in docs/module-1-ros2/key-concepts.md showing correct reference format per plan.md Decision 5
- [ ] T063 [US4] Test authoring guidelines by verifying all current content has zero implementation details (SC-008: zero code, commands, configurations)

**Checkpoint**: At this point, content authors should clearly understand conceptual-only boundaries for Iteration 1 and can create aligned chapter specs for Iteration 2

---

## Phase 7: RAG Chatbot Implementation

**Purpose**: Implement RAG chatbot with book-wide Q&A and selection-based Q&A modes per contracts/rag-api.yaml

- [ ] T064 [P] Implement backend/api/rag/book_wide_qa.py endpoint matching rag-api.yaml POST /rag/book-qa spec
- [ ] T065 [P] Implement backend/api/rag/selection_qa.py endpoint matching rag-api.yaml POST /rag/selection-qa spec
- [ ] T066 [P] Implement backend/services/retrieval.py with Qdrant vector search logic (top-k chunks, relevance scoring)
- [ ] T067 Create backend/scripts/generate_embeddings.py to read docs/ Markdown files, chunk by section (500-1000 tokens), and upload to Qdrant
- [ ] T068 Add metadata extraction logic to generate_embeddings.py for module, section, difficulty, requires_hardware, keywords per plan.md Decision 4.1
- [ ] T069 [P] Implement src/components/RAGChatWidget.tsx React component with global Q&A mode and selection-based Q&A mode toggle
- [ ] T070 [P] Add RAGChatWidget to Docusaurus theme wrapper in src/theme/Root.tsx
- [ ] T071 Run generate_embeddings.py script to populate Qdrant with initial book content embeddings
- [ ] T072 Test book-wide Q&A by querying "How do I integrate LLMs with ROS 2 actions?" and verifying retrieval from Module 1 and Module 4 content
- [ ] T073 Test selection-based Q&A by highlighting "ROS 2 Actions provide goal-based async operations" and asking "Explain in simpler terms"

---

## Phase 8: Personalization Engine Implementation

**Purpose**: Implement personalization engine with user profiles and content adaptation per contracts/personalization-api.yaml

- [ ] T074 [P] Implement backend/api/personalization/user_profile.py with GET and PUT endpoints matching personalization-api.yaml
- [ ] T075 [P] Implement backend/api/personalization/content_adapter.py with POST /personalization/adapt-content endpoint
- [ ] T076 Implement signup flow extension in backend/services/auth.py to collect hardware profile (has_rtx_gpu, has_jetson, jetson_model, robot_type)
- [ ] T077 Implement signup flow extension in backend/services/auth.py to collect experience levels (ros2_experience, ml_experience, robotics_experience)
- [ ] T078 Implement personalization rules in backend/api/personalization/content_adapter.py per plan.md Decision 4.2 (RTX GPU alternatives, Jetson recommendations, simulation-first emphasis)
- [ ] T079 [P] Implement src/components/PersonalizationBar.tsx showing current user hardware profile and experience level
- [ ] T080 [P] Create Docusaurus custom component <PersonalizationBlock> for conditional content rendering based on user profile
- [ ] T081 Add personalization blocks to docs/module-3-isaac/index.md showing cloud GPU alternatives for users without RTX
- [ ] T082 Test personalization by creating user profile with has_rtx_gpu=false and verifying cloud GPU recommendations appear in Isaac module
- [ ] T083 Test personalization by creating user profile with ros2_experience='none' and verifying beginner prerequisites appear in Module 1

---

## Phase 9: Translation Service Implementation

**Purpose**: Implement Urdu translation service with caching per contracts/translation-api.yaml

- [ ] T084 [P] Implement backend/api/translation/translate.py with POST /translation/translate endpoint matching translation-api.yaml
- [ ] T085 [P] Implement backend/api/translation/translate.py with GET /translation/supported-languages endpoint returning ['en', 'ur']
- [ ] T086 Implement translation logic in backend/api/translation/translate.py using OpenAI GPT-4 with prompt: "Translate to Urdu, preserve code blocks unchanged"
- [ ] T087 Implement translation cache lookup in backend/api/translation/translate.py checking translation_cache table by (section_id, target_language, content_hash)
- [ ] T088 Implement cache storage in backend/api/translation/translate.py storing translated content with access_count tracking
- [ ] T089 [P] Implement src/components/TranslationButton.tsx with language toggle (English | Urdu) per section
- [ ] T090 Add TranslationButton to Docusaurus theme per-page header via src/theme/DocItem/Footer/index.tsx
- [ ] T091 Test translation by translating docs/module-1-ros2/conceptual-overview.md to Urdu and verifying code blocks remain in English
- [ ] T092 Test translation cache by translating same section twice and verifying second request is <500ms (cache hit)

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [ ] T093 [P] Add Mermaid diagrams to docs/capstone/simulation-flow.md showing autonomous humanoid workflow integration
- [ ] T094 [P] Add APA citations to all technical claims in module conceptual-overview.md files using research.md sources
- [ ] T095 [P] Update README.md with project overview, quick start instructions, and link to deployed book
- [ ] T096 [P] Create GitHub Actions workflow in .github/workflows/embeddings-update.yml to regenerate Qdrant embeddings on docs/ content changes
- [ ] T097 [P] Create GitHub Actions workflow in .github/workflows/backend-deploy.yml for Railway/Vercel backend deployment
- [ ] T098 Run Docusaurus build validation with `npm run build` and fix any broken links or Markdown errors
- [ ] T099 Test full user journey: New reader navigates homepage → explores Module 1 → checks hardware requirements → asks RAG chatbot question → switches to Urdu
- [ ] T100 Validate against spec.md success criteria (SC-001 through SC-008): navigation time <30s, module identification accuracy, zero implementation details
- [ ] T101 Run quickstart.md validation by following frontend setup instructions on clean system
- [ ] T102 Deploy Docusaurus site to GitHub Pages and verify all content renders correctly
- [ ] T103 Deploy FastAPI backend to Railway/Vercel and update frontend API endpoints to production URLs

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1) and User Story 2 (P1) can proceed in parallel after Phase 2
  - User Story 3 (P2) can proceed in parallel with US1/US2 after Phase 2
  - User Story 4 (P3) should wait for US1-US3 completion for content examples
- **RAG (Phase 7)**: Depends on Foundational (Phase 2) and User Story 1 completion (needs initial content for embeddings)
- **Personalization (Phase 8)**: Depends on Foundational (Phase 2) and User Story 3 completion (needs hardware requirements content)
- **Translation (Phase 9)**: Depends on Foundational (Phase 2) and User Story 1 completion (needs content to translate)
- **Polish (Phase 10)**: Depends on all prior phases being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independently testable, integrates with US1 for cross-references
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independently testable, references modules from US1/US2
- **User Story 4 (P3)**: Should wait for US1-US3 completion to have content examples - Uses content from prior stories as authoring guideline examples

### Within Each User Story

- All module index.md files within a story can be created in parallel (marked [P])
- Conceptual overview files can be created in parallel (marked [P])
- Learning outcomes files can be created in parallel (marked [P])
- Sidebar and navigation updates must happen sequentially after content files exist

### Parallel Opportunities

- **Phase 1 Setup**: T002, T003, T004 can run in parallel (different files)
- **Phase 2 Foundational**: T008, T009, T010, T011, T012, T013, T014, T015 can run in parallel (different subsystems)
- **Phase 3 User Story 1**: T016, T017, T018, T019, T020, T021 can run in parallel (different module files)
- **Phase 4 User Story 2**: T026-T037 can run in parallel (different module conceptual files)
- **Phase 5 User Story 3**: T044, T045, T046, T047 can run in parallel (different hardware categories)
- **Phase 6 User Story 4**: T052-T059 can run in parallel (different module architecture diagrams)
- **Phase 7 RAG**: T064, T065, T066 can run in parallel (different API endpoints)
- **Phase 8 Personalization**: T074, T075, T079, T080 can run in parallel (API vs. frontend components)
- **Phase 9 Translation**: T084, T085, T089 can run in parallel (API vs. frontend components)
- **Phase 10 Polish**: T093, T094, T095, T096, T097 can run in parallel (documentation and CI/CD)

---

## Parallel Example: User Story 1

```bash
# Launch all module index files for User Story 1 together:
claude-code: "Create docs/module-1-ros2/index.md with Module 1 overview"
claude-code: "Create docs/module-2-digital-twin/index.md with Module 2 overview"
claude-code: "Create docs/module-3-isaac/index.md with Module 3 overview"
claude-code: "Create docs/module-4-vla/index.md with Module 4 overview"

# These tasks (T018, T019, T020, T021) can execute concurrently since they modify different files
```

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational backend setup tasks together:
claude-code: "Initialize FastAPI app in backend/main.py"
claude-code: "Setup Neon Postgres connection in backend/config.py"
claude-code: "Setup Qdrant client in backend/services/embedding.py"
claude-code: "Create Better-Auth configuration in backend/services/auth.py"
claude-code: "Create base models in backend/models/"

# These tasks (T009, T010, T012, T013, T014) can execute concurrently
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T015) - CRITICAL blocker
3. Complete Phase 3: User Story 1 (T016-T025)
4. **STOP and VALIDATE**: Test navigation independently (SC-001: readers can identify modules in <30 seconds)
5. Deploy Docusaurus to GitHub Pages for initial demo

### Incremental Delivery (Full Feature)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (P1) → Test navigation independently → Deploy (MVP!)
3. Add User Story 2 (P1) in parallel or after US1 → Test module relationships → Deploy
4. Add User Story 3 (P2) → Test hardware assessment → Deploy
5. Add User Story 4 (P3) → Test authoring guidelines → Deploy
6. Add RAG Chatbot (Phase 7) → Test Q&A modes → Deploy
7. Add Personalization (Phase 8) → Test profile-based content adaptation → Deploy
8. Add Translation (Phase 9) → Test Urdu translation → Deploy
9. Polish (Phase 10) → Final validation → Production deploy

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Developer A**: User Story 1 + User Story 2 (book structure and relationships)
   - **Developer B**: User Story 3 (hardware requirements)
   - **Developer C**: RAG backend (Phase 7)
   - **Developer D**: Personalization backend (Phase 8)
3. **After content complete**: Translation (Phase 9) and Polish (Phase 10)

---

## Expansion Notes for Future Iterations

**Iteration 2 Scope** (after tasks.md completion):
- Detailed chapter specifications for each module
- Step-by-step tutorials with code examples
- URDF/SDF robot definitions
- Configuration files and scripts
- Multi-language expansion (French, Arabic, German per user's comprehensive prompts)
- Interactive exercises and quizzes
- Video tutorial integration

**Expansion Prompts Provided**:
User provided comprehensive `/sp.outline`, `/sp.decisions`, `/sp.workflow`, `/sp.tasks` prompts that expand this project to include:
- 5-language support (EN/UR/FR/AR/DE) vs. current 2 languages (EN/UR)
- More granular content structure (/docs/foundations/, /docs/modules/, /docs/hardware/, /docs/capstone/, /docs/ai-features/, /docs/meta/)
- Reusable intelligence subagents and skills documentation
- Additional AI-native features

These expansion prompts can be referenced when creating Iteration 2 specifications.

---

## Notes

- [P] tasks = different files, no dependencies within same phase
- [Story] label maps task to specific user story (US1, US2, US3, US4) for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group of [P] tasks
- Stop at any checkpoint to validate story independently
- **Iteration 1 Focus**: High-level conceptual content only - no tutorials, code examples, or detailed configurations per spec.md Out of Scope
- All technical claims must include APA citations from research.md sources
- Avoid: implementation details in Iteration 1, cross-story dependencies that break independence, vague tasks
