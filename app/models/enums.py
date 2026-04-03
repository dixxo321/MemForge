from enum import Enum


class MemoryType(str, Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    WORKING = "working"
    SESSION = "session"
    USER_PREFERENCE = "user_preference"
    TOOL_EXECUTION = "tool_execution"
    TASK_PROJECT = "task_project"


class MemoryStatus(str, Enum):
    ACTIVE = "active"
    MERGED = "merged"
    DEPRECATED = "deprecated"
    DELETED = "deleted"


class PrivacyScope(str, Enum):
    PRIVATE = "private"
    AGENT = "agent"
    PROJECT = "project"


class CheckpointKind(str, Enum):
    AUTO = "auto"
    MANUAL = "manual"
    STABLE = "stable"
    BRANCH = "branch"


class TaskStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"
