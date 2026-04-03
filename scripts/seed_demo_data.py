from sqlmodel import Session

from app.core.database import engine, init_db
from app.models import Agent, MemoryType, User
from app.services import MemoryService


def main() -> None:
    init_db()
    memory_service = MemoryService()

    with Session(engine) as session:
        user = User(name="Demo User", email="demo@example.com")
        session.add(user)
        session.commit()
        session.refresh(user)

        agent = Agent(user_id=user.id, name="Demo Agent", model_name="local-dev")
        session.add(agent)
        session.commit()
        session.refresh(agent)

        memory_service.add_memory(
            session=session,
            user_id=user.id,
            agent_id=agent.id,
            content="User prefers short technical answers.",
            memory_type=MemoryType.USER_PREFERENCE,
            summary="Communication preference",
        )

        memory_service.add_memory(
            session=session,
            user_id=user.id,
            agent_id=agent.id,
            content="Project Atlas uses FastAPI and SQLite.",
            memory_type=MemoryType.TASK_PROJECT,
            summary="Atlas tech stack",
        )

        memory_service.add_memory(
            session=session,
            user_id=user.id,
            agent_id=agent.id,
            content="Remember to continue unfinished deployment tasks across sessions.",
            memory_type=MemoryType.SESSION,
            summary="Session continuity requirement",
        )

        print("Demo data seeded.")
        print(f"user_id={user.id}")
        print(f"agent_id={agent.id}")


if __name__ == "__main__":
    main()
