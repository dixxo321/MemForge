# Memory Model

MemForge uses a hybrid memory model so agents can remember the right things without storing everything forever.

## Core memory types

### Semantic memory
General knowledge learned from user interactions, notes, documents, and prior sessions.

Examples:
- "The user prefers short answers."
- "Project Atlas uses FastAPI and SQLite."

### Episodic memory
Specific events that happened at a point in time.

Examples:
- "On April 3, the agent failed to deploy because the port was already in use."
- "The user asked to resume the unfinished report."

### Procedural memory
How to do something. Repeatable workflows, instructions, and step-by-step methods.

Examples:
- "To publish releases, run tests, build package, tag version, push GitHub release."
- "To restore a checkpoint, fetch latest stable snapshot and replay task state."

### User preference memory
Long-lived user-specific preferences that improve response quality across sessions.

Examples:
- "User likes simple English."
- "User wants Termux-ready commands."

### Session memory
Short-lived context for the active session.

Examples:
- current task goal
- active branch
- recent tool outputs
- current checkpoint pointer

## Why separate memory types?

Different memory types have different rules for:
- retention
- ranking
- decay
- recall
- update strategy

A preference memory should live longer than a temporary session note.
An episodic event should keep timestamp and provenance.
A procedural memory should support versioning.

## Memory lifecycle

1. Ingest event
2. Classify memory-worthiness
3. Detect memory type
4. Extract structured signals
5. Score importance and salience
6. Check duplicates and contradictions
7. Store structured record
8. Store embedding
9. Link related memories
10. Decay, archive, merge, or promote over time

## Design principles

- Local-first by default
- Structured + semantic retrieval
- Transparent inspection and editing
- Explainable recall
- Easy future expansion
