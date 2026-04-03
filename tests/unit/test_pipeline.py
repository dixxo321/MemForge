from sqlmodel import Session

from app.core.database import engine, init_db
from app.models import Agent, MemoryType, User
from app.services import MemoryService, RetrievalService


def ensure_user_agent(session: Session) -> tuple[str, str]:
    user = User(name="Pipeline User")
    session.add(user)
    session.commit()
    session.refresh(user)

    agent = Agent(user_id=user.id, name="Pipeline Agent")
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return user.id, agent.id


def test_duplicate_and_contradiction_flow() -> None:
    init_db()
    memory_service = MemoryService()
    retrieval_service = RetrievalService()

    with Session(engine) as session:
        user_id, agent_id = ensure_user_agent(session)

        first = memory_service.add_memory(
            session=session,
            user_id=user_id,
            agent_id=agent_id,
            content="User likes dark mode",
            memory_type=MemoryType.USER_PREFERENCE,
        )
        assert first.id is not None

        duplicate = memory_service.add_memory(
            session=session,
            user_id=user_id,
            agent_id=agent_id,
            content="User likes dark mode",
            memory_type=MemoryType.USER_PREFERENCE,
        )
        assert duplicate.id == first.id

        contradiction = memory_service.add_memory(
            session=session,
            user_id=user_id,
            agent_id=agent_id,
            content="User dislikes dark mode",
            memory_type=MemoryType.USER_PREFERENCE,
        )
        assert "POTENTIAL_CONTRADICTION_WITH" in contradiction.content

        payload = retrieval_service.recall_for_prompt(
            session=session,
            query="dark mode",
            user_id=user_id,
            agent_id=agent_id,
            limit=5,
        )
        assert "Relevant memory context:" in payload["context_text"]
