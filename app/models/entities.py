from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import BaseRecord
from app.models.enums import CheckpointKind, MemoryStatus, MemoryType, PrivacyScope, TaskStatus


class User(BaseRecord, table=True):
    __tablename__ = "users"

    external_id: Optional[str] = Field(default=None, index=True)
    name: str = Field(index=True)
    email: Optional[str] = Field(default=None, index=True)
    is_active: bool = Field(default=True)


class Agent(BaseRecord, table=True):
    __tablename__ = "agents"

    user_id: str = Field(foreign_key="users.id", index=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    model_name: Optional[str] = None
    config_profile_id: Optional[str] = Field(default=None, index=True)


class Project(BaseRecord, table=True):
    __tablename__ = "projects"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    status: str = Field(default="active", index=True)


class Session(BaseRecord, table=True):
    __tablename__ = "sessions"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: str = Field(foreign_key="agents.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    title: Optional[str] = None
    status: str = Field(default="active", index=True)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = Field(default=None)


class Conversation(BaseRecord, table=True):
    __tablename__ = "conversations"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: str = Field(foreign_key="agents.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    title: Optional[str] = None


class Message(BaseRecord, table=True):
    __tablename__ = "messages"

    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    role: str = Field(index=True)
    content: str
    normalized_content: Optional[str] = None
    token_count: Optional[int] = Field(default=None)
    source_type: Optional[str] = Field(default=None, index=True)
    source_id: Optional[str] = Field(default=None, index=True)


class Memory(BaseRecord, table=True):
    __tablename__ = "memories"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: str = Field(foreign_key="agents.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)

    memory_type: MemoryType = Field(index=True)
    status: MemoryStatus = Field(default=MemoryStatus.ACTIVE, index=True)
    privacy_scope: PrivacyScope = Field(default=PrivacyScope.PRIVATE, index=True)

    content: str
    normalized_content: Optional[str] = None
    summary: Optional[str] = None
    embedding_ref: Optional[str] = Field(default=None, index=True)

    source_type: Optional[str] = Field(default=None, index=True)
    source_id: Optional[str] = Field(default=None, index=True)

    tags_json: Optional[str] = None
    entities_json: Optional[str] = None

    salience_score: float = Field(default=0.0, index=True)
    importance_score: float = Field(default=0.0, index=True)
    confidence_score: float = Field(default=1.0, index=True)
    recency_score: float = Field(default=0.0, index=True)

    access_count: int = Field(default=0)
    last_accessed_at: Optional[datetime] = Field(default=None)

    expires_at: Optional[datetime] = Field(default=None)
    version: int = Field(default=1)


class MemoryChunk(BaseRecord, table=True):
    __tablename__ = "memory_chunks"

    memory_id: str = Field(foreign_key="memories.id", index=True)
    chunk_index: int = Field(index=True)
    content: str
    normalized_content: Optional[str] = None
    embedding_ref: Optional[str] = Field(default=None, index=True)
    token_count: Optional[int] = None


class EmbeddingMetadata(BaseRecord, table=True):
    __tablename__ = "embeddings_metadata"

    object_type: str = Field(index=True)
    object_id: str = Field(index=True)
    provider: Optional[str] = Field(default=None, index=True)
    model: Optional[str] = Field(default=None, index=True)
    vector_backend: Optional[str] = Field(default=None, index=True)
    vector_key: str = Field(index=True)
    dimension: Optional[int] = None
    content_hash: Optional[str] = Field(default=None, index=True)


class Preference(BaseRecord, table=True):
    __tablename__ = "preferences"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    key: str = Field(index=True)
    value: str
    namespace: str = Field(default="default", index=True)
    confidence_score: float = Field(default=1.0)
    source_memory_id: Optional[str] = Field(default=None, foreign_key="memories.id", index=True)


class Entity(BaseRecord, table=True):
    __tablename__ = "entities"

    user_id: str = Field(foreign_key="users.id", index=True)
    name: str = Field(index=True)
    entity_type: str = Field(index=True)
    canonical_name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None


class Fact(BaseRecord, table=True):
    __tablename__ = "facts"

    user_id: str = Field(foreign_key="users.id", index=True)
    memory_id: Optional[str] = Field(default=None, foreign_key="memories.id", index=True)
    entity_id: Optional[str] = Field(default=None, foreign_key="entities.id", index=True)
    subject: str = Field(index=True)
    predicate: str = Field(index=True)
    object_value: str
    confidence_score: float = Field(default=1.0)
    valid_from: Optional[datetime] = Field(default=None)
    valid_to: Optional[datetime] = Field(default=None)


class EpisodicEvent(BaseRecord, table=True):
    __tablename__ = "episodic_events"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    memory_id: Optional[str] = Field(default=None, foreign_key="memories.id", index=True)
    event_type: str = Field(index=True)
    title: str = Field(index=True)
    details: Optional[str] = None
    occurred_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class Procedure(BaseRecord, table=True):
    __tablename__ = "procedures"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    steps_json: str
    source_memory_id: Optional[str] = Field(default=None, foreign_key="memories.id", index=True)


class Summary(BaseRecord, table=True):
    __tablename__ = "summaries"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    summary_type: str = Field(index=True)
    content: str
    source_refs_json: Optional[str] = None


class Checkpoint(BaseRecord, table=True):
    __tablename__ = "checkpoints"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: str = Field(foreign_key="agents.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)

    kind: CheckpointKind = Field(index=True)
    name: Optional[str] = Field(default=None, index=True)
    state_json: str
    planner_state_json: Optional[str] = None
    tool_state_json: Optional[str] = None
    partial_output: Optional[str] = None
    parent_checkpoint_id: Optional[str] = Field(default=None, foreign_key="checkpoints.id", index=True)
    is_latest_stable: bool = Field(default=False, index=True)


class ToolRun(BaseRecord, table=True):
    __tablename__ = "tool_runs"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    tool_name: str = Field(index=True)
    status: str = Field(index=True)
    input_json: Optional[str] = None
    output_json: Optional[str] = None
    error_text: Optional[str] = None
    latency_ms: Optional[int] = None
    source_memory_id: Optional[str] = Field(default=None, foreign_key="memories.id", index=True)


class Artifact(BaseRecord, table=True):
    __tablename__ = "artifacts"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    artifact_type: str = Field(index=True)
    name: str = Field(index=True)
    path_or_uri: Optional[str] = None
    content_hash: Optional[str] = Field(default=None, index=True)


class Tag(BaseRecord, table=True):
    __tablename__ = "tags"

    user_id: str = Field(foreign_key="users.id", index=True)
    name: str = Field(index=True, unique=True)
    color: Optional[str] = None
    description: Optional[str] = None


class MemoryLink(BaseRecord, table=True):
    __tablename__ = "memory_links"

    source_memory_id: str = Field(foreign_key="memories.id", index=True)
    target_memory_id: str = Field(foreign_key="memories.id", index=True)
    link_type: str = Field(index=True)
    weight: float = Field(default=1.0)


class MemoryVersion(BaseRecord, table=True):
    __tablename__ = "memory_versions"

    memory_id: str = Field(foreign_key="memories.id", index=True)
    version_number: int = Field(index=True)
    content: str
    summary: Optional[str] = None
    change_reason: Optional[str] = None


class FeedbackSignal(BaseRecord, table=True):
    __tablename__ = "feedback_signals"

    user_id: str = Field(foreign_key="users.id", index=True)
    memory_id: Optional[str] = Field(default=None, foreign_key="memories.id", index=True)
    retrieval_log_id: Optional[str] = Field(default=None, foreign_key="retrieval_logs.id", index=True)
    score: int = Field(index=True)
    feedback_type: str = Field(index=True)
    notes: Optional[str] = None


class RetrievalLog(BaseRecord, table=True):
    __tablename__ = "retrieval_logs"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    query_text: str
    normalized_query: Optional[str] = None
    strategy: Optional[str] = Field(default=None, index=True)
    filters_json: Optional[str] = None
    result_ids_json: Optional[str] = None
    latency_ms: Optional[int] = None


class EvaluationRun(BaseRecord, table=True):
    __tablename__ = "evaluation_runs"

    user_id: Optional[str] = Field(default=None, foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    name: str = Field(index=True)
    dataset_name: Optional[str] = Field(default=None, index=True)
    metrics_json: Optional[str] = None
    notes: Optional[str] = None


class ConfigProfile(BaseRecord, table=True):
    __tablename__ = "config_profiles"

    user_id: Optional[str] = Field(default=None, foreign_key="users.id", index=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    config_json: str


class Task(BaseRecord, table=True):
    __tablename__ = "tasks"

    user_id: str = Field(foreign_key="users.id", index=True)
    agent_id: Optional[str] = Field(default=None, foreign_key="agents.id", index=True)
    project_id: Optional[str] = Field(default=None, foreign_key="projects.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="sessions.id", index=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    priority: int = Field(default=0, index=True)
    due_at: Optional[datetime] = Field(default=None)
    source_memory_id: Optional[str] = Field(default=None, foreign_key="memories.id", index=True)


class TaskStep(BaseRecord, table=True):
    __tablename__ = "task_steps"

    task_id: str = Field(foreign_key="tasks.id", index=True)
    step_index: int = Field(index=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    output_json: Optional[str] = None
