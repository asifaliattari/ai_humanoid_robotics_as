# AI-Native Features

## Overview

This book is **AI-native**: it uses AI not just as a subject of study, but as a tool for learning, personalization, and content delivery. The platform includes:

1. 🤖 **RAG Chatbot** - Ask questions about any topic
2. 🎯 **Personalization Engine** - Content adapts to your hardware and experience
3. 🌐 **Multi-Language Translation** - Read in EN / UR / FR / AR / DE
4. 🧠 **Claude Subagents** - Specialized AI assistants for each module
5. 🛠️ **Reusable Skills** - AI-generated summaries, exercises, diagrams

## 1. RAG Chatbot

**Purpose**: Answer questions using the entire book as context

**Architecture**:
- **Frontend**: React chat widget (bottom-right floating button)
- **Backend**: FastAPI + Qdrant (vector search) + OpenAI ChatKit (agent orchestration)
- **Embeddings**: Book content chunked by section, stored in Qdrant with metadata

### Chatbot Modes

#### Mode A: Ask the Full Book
**Use Case**: General questions like "How do ROS 2 Actions work?"

**Pipeline**:
```
User Query → Embed query → Search Qdrant → Retrieve top-k chunks → LLM synthesis → Answer
```

**Metadata Filtering**:
- Filter by module (e.g., only search Module 1)
- Filter by difficulty (beginner, intermediate, advanced)
- Filter by language (EN, UR, FR, AR, DE)

#### Mode B: Ask About Selected Text
**Use Case**: Highlight a paragraph and ask "Explain this in simpler terms"

**Pipeline**:
```
Selected Text + User Query → LLM (no vector search) → Simplified Answer
```

**Advantages**:
- Faster (no retrieval)
- Context-specific
- Privacy-preserving (no logging selected text)

### Example Interactions

**Q**: "What's the difference between ROS 2 Topics and Services?"
**A**: "Topics use pub/sub for one-to-many asynchronous messaging (e.g., broadcasting camera images), while Services use request/response for one-to-one synchronous queries (e.g., asking a planner for a path). See [Module 1: ROS 2](/docs/modules/ros2/)."

**Q** (highlights URDF definition): "Can you give an example?"
**A**: "Sure! Here's a simple humanoid URDF with head, torso, and arm links: [example code]. The `<link>` tags define rigid bodies, and `<joint>` tags define how they connect."

---

## 2. Personalization Engine

**Purpose**: Adapt chapter content based on user hardware and experience

**Signup Flow**:
When you create an account, we ask:
1. **Hardware**: RTX GPU? Jetson Orin (Nano/NX)? Cloud-only?
2. **Software Experience**: Beginner / Intermediate / Advanced
3. **Preferred Language**: EN / UR / FR / AR / DE

**Personalization Rules**:

| User Profile | Content Adaptation |
|--------------|-------------------|
| No RTX GPU | Show cloud GPU alternatives in Module 3 |
| No Jetson | Emphasize simulation-first workflow |
| No Robot | Focus on simulation validation, defer physical deployment |
| ROS 2 Beginner | Add prerequisite links, simplify jargon |
| ML Advanced | Link to papers (RT-1, PaLM-E), reduce basic explanations |

**UI**: 🎛 **Personalize This Chapter** button at top of each page

---

## 3. Multi-Language Translation

**Supported Languages**:
- 🇬🇧 **English** (primary authoring language)
- 🇵🇰 **Urdu** (right-to-left)
- 🇫🇷 **French**
- 🇸🇦 **Arabic** (right-to-left)
- 🇩🇪 **German**

**Translation Strategy**:
1. **On-Demand**: User clicks 🌐 language toggle
2. **Cache Check**: Query Neon Postgres for existing translation
3. **LLM Translation** (if cache miss): GPT-4 translates text, preserves code blocks
4. **Cache Store**: Save translation for future users

**What Gets Translated**:
- ✅ Headings, paragraphs, list items
- ✅ Table text (except code columns)
- ❌ Code blocks (remain in original language)
- ❌ Commands, file paths, URLs
- ❌ Technical terms (ROS 2, Isaac Sim, URDF)

**RTL Handling**:
- Urdu and Arabic automatically switch layout direction
- Code blocks remain LTR even in RTL pages

---

## 4. Claude Subagents

**Concept**: Specialized AI assistants for specific domains

### Available Subagents

#### 🤖 **ROS2Expert**
- **Purpose**: Answer ROS 2 architecture and design questions
- **Training**: ROS 2 docs, Design docs, tutorials
- **Example**: "Why use Actions instead of Services for navigation?"

#### 🏗️ **IsaacSimArchitect**
- **Purpose**: Help with Isaac Sim setup and sim-to-real transfer
- **Training**: Isaac Sim docs, physics tuning guides
- **Example**: "How do I reduce the sim-to-real gap for depth sensors?"

#### 🎮 **GazeboSimulationDesigner**
- **Purpose**: Design custom Gazebo worlds and sensor configs
- **Training**: Gazebo SDF docs, plugin examples
- **Example**: "Create a staircase environment with configurable step height"

#### 🧠 **VLAMaster**
- **Purpose**: Design VLA pipelines and skill primitives
- **Training**: RT-1/RT-2 papers, LLM prompting best practices
- **Example**: "How should I structure the skill library for a kitchen robot?"

#### 📚 **ExplainForBeginners**
- **Purpose**: Simplify technical content for beginners
- **Training**: Pedagogical best practices, analogy generation
- **Example**: "Explain SLAM like I'm 10 years old"

#### ✍️ **GenerateExercises**
- **Purpose**: Create practice problems for each chapter
- **Training**: Robotics textbooks, exercise patterns
- **Example**: "Generate 3 exercises for ROS 2 Topics"

#### 🌐 **TranslateToMultiLanguage**
- **Purpose**: Translate technical content while preserving meaning
- **Training**: Translation examples, technical term glossaries
- **Example**: "Translate this Isaac ROS tutorial to Urdu"

### How to Invoke Subagents
- **In Chatbot**: "Ask ROS2Expert: [your question]"
- **Via Personalization**: Advanced users see "Ask an Expert" buttons

---

## 5. Reusable Skills

**Purpose**: AI-generated content enhancements

### Skill: Generate Module Summary
**Input**: Module ID (e.g., "module-1-ros2")
**Output**: 3-sentence summary suitable for social media or course catalog

**Example**: "Module 1 teaches the ROS 2 communication framework. You'll learn how nodes exchange messages via Topics, Services, and Actions. By the end, you can design distributed robot software architectures."

### Skill: Rewrite for Skill Level
**Input**: Section content + target level (beginner/intermediate/advanced)
**Output**: Adapted content with appropriate technical depth

**Example** (beginner): "ROS 2 Topics are like radio broadcasts. One node transmits, many others listen."
**Example** (advanced): "ROS 2 Topics implement DDS pub/sub with QoS policies for reliability and latency control."

### Skill: Generate Diagrams
**Input**: Concept description (e.g., "ROS 2 node communication")
**Output**: Mermaid diagram code + textual description

### Skill: Suggest Exercises
**Input**: Chapter content
**Output**: 3-5 practice problems with solutions

**Example**: "Exercise 1: Draw a node graph for a humanoid with camera, planner, and motor controller. Which nodes publish to which topics?"

### Skill: Create Glossary
**Input**: Module text
**Output**: Alphabetical list of technical terms with definitions

---

## Implementation Details

**Backend**: `D:\hakathon\ai_humanoid_robotics_as\backend\`
- `api/rag/`: Chatbot endpoints
- `api/personalization/`: User profile and content adaptation
- `api/translation/`: Translation service
- `services/embedding.py`: Qdrant integration
- `services/auth.py`: Better-Auth integration

**Frontend**: `D:\hakathon\ai_humanoid_robotics_as\src\components\`
- `RAGChatWidget.tsx`: Floating chat button
- `PersonalizationBar.tsx`: Hardware/experience display
- `TranslationButton.tsx`: Language toggle

**Data**: Neon Serverless Postgres
- `user_profiles`: Hardware, experience, language preferences
- `translation_cache`: Cached translations by (section_id, language, content_hash)
- `rag_query_log`: User queries for quality improvement

---

## Privacy & Ethics

**Data Collection**:
- ✅ User profiles (for personalization)
- ✅ RAG queries (anonymous, for improving chatbot)
- ✅ Translation requests (cached for performance)
- ❌ Selected text (Mode B queries NOT logged)
- ❌ Personal data (emails encrypted, GDPR-compliant)

**Opt-Out**:
- Users can disable personalization (get default content)
- Users can request data deletion (GDPR right to erasure)

---

## Next Steps

**In Iteration 2**, you will learn:
- How the RAG embedding pipeline works (chunking, metadata, Qdrant schema)
- How to customize Claude subagents for your domain
- How to add new languages beyond the current 5
- How to fine-tune personalization rules

## References

Lewis, P., Perez, E., Piktus, A., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS).

OpenAI. (2024). *ChatGPT API Documentation*. Retrieved from https://platform.openai.com/docs/

Anthropic. (2024). *Claude API Documentation*. Retrieved from https://docs.anthropic.com/
