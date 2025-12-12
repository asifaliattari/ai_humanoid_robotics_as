# Database Migrations

This directory contains Alembic migrations for the Physical AI & Humanoid Robotics backend.

## Setup

1. Ensure your `.env` file has the correct `DATABASE_URL`:
   ```bash
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

2. Run migrations:
   ```bash
   # From backend/ directory
   alembic upgrade head
   ```

## Creating New Migrations

### Auto-generate migration from model changes:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Create empty migration:
```bash
alembic revision -m "Description of changes"
```

## Common Commands

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Show SQL without executing
alembic upgrade head --sql
```

## Migrations

### 001 - Initial Schema (2025-01-01)
- Creates user_profiles table with hardware/experience/preferences
- Creates reading_progress table for tracking chapter completion
- Creates rag_query_logs table for chatbot analytics
- Creates translation_cache table for caching translations
- Creates ENUM types: jetson_model, robot_type, experience_level, language, theme

## Database Schema

### user_profiles
User hardware, experience, and preferences for personalization

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | String | Unique user email |
| has_rtx_gpu | Boolean | RTX GPU availability |
| has_jetson | Boolean | Jetson device availability |
| jetson_model | Enum | Jetson model (nano, xavier_nx, agx_xavier, orin_nano, agx_orin) |
| robot_type | Enum | Robot type (turtlebot3, kobuki, jetbot, etc.) |
| has_realsense | Boolean | RealSense camera availability |
| has_lidar | Boolean | LiDAR sensor availability |
| ros2_experience | Enum | ROS 2 skill level |
| ml_experience | Enum | ML skill level |
| robotics_experience | Enum | Robotics skill level |
| simulation_experience | Enum | Simulation skill level |
| preferred_language | Enum | UI language (en, ur, fr, ar, de) |
| theme | Enum | UI theme (light, dark, auto) |

### reading_progress
Track which chapters users have read

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | String | User identifier |
| section_id | String | Section identifier (e.g., 'modules/ros2/index') |
| progress_percentage | Integer | 0-100 completion |
| completed | Boolean | Full completion flag |
| last_position | Integer | Last scroll position |
| time_spent_seconds | Integer | Total time on section |

### rag_query_logs
Log all RAG chatbot queries for analytics

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | String | User identifier (optional) |
| query_text | Text | User's question |
| query_mode | String | 'book-wide' or 'selection-based' |
| selected_text | Text | Highlighted text (selection-based only) |
| retrieved_chunks | JSONB | Retrieved context chunks |
| response_text | Text | Generated answer |
| response_time_ms | Integer | Response latency |

### translation_cache
Cache translations to reduce API costs

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| section_id | String | Section identifier |
| target_language | String | Target language code |
| content_hash | String | SHA-256 of original content |
| original_content | Text | Original English text |
| translated_content | Text | Translated text |
| access_count | Integer | Number of cache hits |
| last_accessed_at | DateTime | Last cache access |

## Notes

- All UUIDs are generated automatically
- Timestamps (created_at, updated_at) use PostgreSQL CURRENT_TIMESTAMP
- Unique constraints:
  - user_profiles: email
  - reading_progress: (user_id, section_id)
  - translation_cache: (section_id, target_language, content_hash)
- Indexes on frequently queried columns for performance
