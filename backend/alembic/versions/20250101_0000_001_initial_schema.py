"""Initial schema - user profiles, reading progress, RAG logs, translation cache

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables"""

    # Create ENUM types
    op.execute("""
        CREATE TYPE jetson_model AS ENUM (
            'none', 'nano', 'xavier_nx', 'agx_xavier', 'orin_nano', 'agx_orin'
        )
    """)

    op.execute("""
        CREATE TYPE robot_type AS ENUM (
            'none', 'turtlebot3', 'kobuki', 'jetbot', 'jetson_nano_robot',
            'clearpath_jackal', 'unitree_go1', 'custom'
        )
    """)

    op.execute("""
        CREATE TYPE experience_level AS ENUM (
            'none', 'beginner', 'intermediate', 'advanced', 'expert'
        )
    """)

    op.execute("""
        CREATE TYPE language AS ENUM ('en', 'ur', 'fr', 'ar', 'de')
    """)

    op.execute("""
        CREATE TYPE theme AS ENUM ('light', 'dark', 'auto')
    """)

    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),

        # Hardware inventory
        sa.Column('has_rtx_gpu', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('has_jetson', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('jetson_model', postgresql.ENUM(name='jetson_model', create_type=False), nullable=True),
        sa.Column('robot_type', postgresql.ENUM(name='robot_type', create_type=False), nullable=False),
        sa.Column('has_realsense', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('has_lidar', sa.Boolean(), nullable=False, server_default='false'),

        # Experience levels
        sa.Column('ros2_experience', postgresql.ENUM(name='experience_level', create_type=False), nullable=False),
        sa.Column('ml_experience', postgresql.ENUM(name='experience_level', create_type=False), nullable=False),
        sa.Column('robotics_experience', postgresql.ENUM(name='experience_level', create_type=False), nullable=False),
        sa.Column('simulation_experience', postgresql.ENUM(name='experience_level', create_type=False), nullable=False),

        # Preferences
        sa.Column('preferred_language', postgresql.ENUM(name='language', create_type=False), nullable=False),
        sa.Column('theme', postgresql.ENUM(name='theme', create_type=False), nullable=False),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create reading_progress table
    op.create_table(
        'reading_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False, index=True),
        sa.Column('section_id', sa.String(255), nullable=False, index=True),
        sa.Column('progress_percentage', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('last_position', sa.Integer(), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create unique index on user_id + section_id
    op.create_index(
        'idx_reading_progress_user_section',
        'reading_progress',
        ['user_id', 'section_id'],
        unique=True
    )

    # Create rag_query_logs table
    op.create_table(
        'rag_query_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=True, index=True),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('query_mode', sa.String(50), nullable=False),
        sa.Column('selected_text', sa.Text(), nullable=True),
        sa.Column('retrieved_chunks', postgresql.JSONB(), nullable=True),
        sa.Column('response_text', sa.Text(), nullable=False),
        sa.Column('response_time_ms', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create index on query_mode
    op.create_index(
        'idx_rag_query_logs_mode',
        'rag_query_logs',
        ['query_mode']
    )

    # Create translation_cache table
    op.create_table(
        'translation_cache',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('section_id', sa.String(255), nullable=False, index=True),
        sa.Column('target_language', sa.String(10), nullable=False, index=True),
        sa.Column('content_hash', sa.String(64), nullable=False, index=True),
        sa.Column('original_content', sa.Text(), nullable=False),
        sa.Column('translated_content', sa.Text(), nullable=False),
        sa.Column('access_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_accessed_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create unique index on section_id + target_language + content_hash
    op.create_index(
        'idx_translation_cache_lookup',
        'translation_cache',
        ['section_id', 'target_language', 'content_hash'],
        unique=True
    )


def downgrade() -> None:
    """Drop all tables and types"""

    # Drop tables
    op.drop_table('translation_cache')
    op.drop_table('rag_query_logs')
    op.drop_table('reading_progress')
    op.drop_table('user_profiles')

    # Drop ENUM types
    op.execute('DROP TYPE IF EXISTS theme')
    op.execute('DROP TYPE IF EXISTS language')
    op.execute('DROP TYPE IF EXISTS experience_level')
    op.execute('DROP TYPE IF EXISTS robot_type')
    op.execute('DROP TYPE IF EXISTS jetson_model')
