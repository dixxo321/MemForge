import json
from pathlib import Path

from sqlmodel import Session, select

from app.core.database import engine, init_db
from app.models import Agent, Checkpoint, Memory, Project, Session as AgentSession, User


def rows_to_dicts(rows):
    output = []
    for row in rows:
        output.append(row.dict())
    return output


def main() -> None:
    init_db()
    export_path = Path("memforge_export.json")

    with Session(engine) as session:
        payload = {
            "users": rows_to_dicts(session.exec(select(User)).all()),
            "agents": rows_to_dicts(session.exec(select(Agent)).all()),
            "projects": rows_to_dicts(session.exec(select(Project)).all()),
            "sessions": rows_to_dicts(session.exec(select(AgentSession)).all()),
            "memories": rows_to_dicts(session.exec(select(Memory)).all()),
            "checkpoints": rows_to_dicts(session.exec(select(Checkpoint)).all()),
        }

    export_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"Exported data to {export_path}")


if __name__ == "__main__":
    main()
