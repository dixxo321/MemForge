# MemForge

**Local-first hybrid memory system for AI agents.**

MemForge is a developer-friendly memory backend for AI agents that want to remember useful things across sessions instead of relying only on raw chat history.

## Why this project exists

Most AI agents forget too much or remember too much.

Common problems:
- they lose preferences between sessions
- they cannot continue unfinished work well
- they dump too much old chat into prompts
- they do not separate facts, events, preferences, and tasks
- they are hard to inspect locally

MemForge solves this by combining:
- structured memory in SQLite
- memory retrieval services
- checkpoints for resumable state
- selective memory writing
- prompt-ready memory recall

## What MemForge does

MemForge helps agents:
- remember user preferences
- continue unfinished work
- recall project facts
- store checkpoints
- build prompt-ready memory context

It is designed for:
- local-first use
- privacy-first workflows
- Python agent integration
- easy inspection and editing
- open-source developer use

## Current status

MemForge is currently an **early working MVP**.

### Working now
- local SQLite database
- core memory schema
- add, list, and search memory
- duplicate detection
- simple contradiction detection
- recall-for-prompt
- checkpoint service base
- Python SDK base
- export and import scripts
- seed demo data
- CLI workflow in Termux

### Not complete yet
- active vector backend
- embeddings integration
- stable FastAPI server on the current phone stack
- stronger ranking
- advanced merge and version rules
- full production polish

## Architecture overview

MemForge uses a hybrid design:

### 1. Relational layer
SQLite stores:
- users
- agents
- sessions
- conversations
- messages
- memories
- tasks
- checkpoints
- retrieval logs
- preferences
- summaries
- links
- versions

### 2. Retrieval layer
The retrieval layer:
- normalizes queries
- searches memory text
- ranks memory matches
- explains why each memory matched
- builds prompt-ready context

### 3. Checkpoint layer
The checkpoint system stores:
- active state
- partial workflow state
- resumable snapshots
- restore points

## Memory types supported

MemForge supports:
- short_term
- long_term
- semantic
- episodic
- procedural
- working
- session
- user_preference
- tool_execution
- task_project

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/dixxo321/MemForge.git
cd MemForge
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

### 4. Create local environment file
```bash
cp .env.example .env
```

### 5. Initialize the database
```bash
python -m app.cli.main initdb
```

## How to use MemForge

### Check setup
```bash
python -m app.cli.main doctor
```

### Add memory
```bash
python -m app.cli.main add-memory user-1 agent-1 "User likes short clear answers" --summary "Communication preference"
```

### List memories
```bash
python -m app.cli.main list-memories --limit 10
```

### Search memories
```bash
python -m app.cli.main search-memory "short answers" --limit 5
```

### Build prompt-ready recall
```bash
python -m app.cli.main recall-prompt "response preference" --limit 5
```

### Seed demo data
```bash
python scripts/seed_demo_data.py
```

### Export local data
```bash
python scripts/export_data.py
```

### Import local data
```bash
python scripts/import_data.py
```

## When to use MemForge

Use MemForge when your agent needs to:
- remember preferences across sessions
- keep project memory
- continue tasks later
- retrieve only relevant context
- stay private and local-first

## Where to use MemForge

You can use it in:
- personal AI assistants
- coding agents
- research agents
- workflow agents
- local desktop agents
- Termux-based phone agents
- custom Python automation tools

## Python SDK example

```python
from sdk.python.memforge import MemForgeClient

client = MemForgeClient()

client.add_memory(
    user_id="user-1",
    agent_id="agent-1",
    content="User prefers short technical answers.",
    memory_type="user_preference",
    summary="Response style preference",
)

payload = client.recall_for_prompt(
    query="response preference",
    user_id="user-1",
    agent_id="agent-1",
    limit=5,
)

print(payload["context_text"])
```

## Project structure

```text
app/
docs/
examples/
scripts/
sdk/python/memforge/
tests/
```

## Is it complete?

Not fully complete yet.

It is:
- functional
- usable
- a strong MVP
- ready for early GitHub publishing

It is not yet a full production release because the vector backend, embeddings path, and some platform stability work are still pending.

## License

Recommended license: MIT
