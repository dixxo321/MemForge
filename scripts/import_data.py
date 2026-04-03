import json
from pathlib import Path

from sqlmodel import Session

from app.core.database import engine, init_db
from app.models import Agent, Checkpoint, Memory, Project, Session as AgentSession, User


MODEL_MAP = {
    "users": User,
    "agents": Agent,
    "projects": Project,
    "sessions": AgentSession,
    "memories": Memory,
    "checkpoints": Checkpoint,
}


def main() -> None:
    init_db()
    import_path = Path("memforge_export.json")

    if not import_path.exists():
        print("memforge_export.json not found")
        return

    payload = json.loads(import_path.read_text(encoding="utf-8"))

    with Session(engine) as session:
        for key, model_cls in MODEL_MAP.items():
            for item in payload.get(key, []):
                obj = model_cls(**item)
                session.merge(obj)
        session.commit()

    print(f"Imported data from {import_path}")


if __name__ == "__main__":
    main()
