from sqlmodel import Session

from app.core.database import engine, init_db
from app.models import CheckpointKind, MemoryType, User, Agent
from app.services import CheckpointService, MemoryService, RetrievalService


def ensure_user_agent(session: Session) -> tuple[str, str]:
    user = User(name="Pushpa Test")
    session.add(user)
    session.commit()
    session.refresh(user)

    agent = Agent(user_id=user.id, name="Test Agent")
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return user.id, agent.id


def test_memory_and_checkpoint_flow() -> None:
    init_db()
    memory_service = MemoryService()
    checkpoint_service = CheckpointService()
    retrieval_service = RetrievalService()

    with Session(engine) as session:
        user_id, agent_id = ensure_user_agent(session)

        memory = memory_service.add_memory(
            session=session,
            user_id=user_id,
            agent_id=agent_id,
            content="User prefers concise technical answers.",
            summary="Preference for concise technical answers",
            memory_type=MemoryType.USER_PREFERENCE,
        )
        assert memory.id is not None

        results = retrieval_service.search(
            session=session,
            query="concise technical answers",
            user_id=user_id,
            agent_id=agent_id,
            limit=5,
        )
        assert len(results) >= 1

        checkpoint = checkpoint_service.save_checkpoint(
            session=session,
            user_id=user_id,
            agent_id=agent_id,
            session_id="session-1",
            state_json='{"step": 1}',
            kind=CheckpointKind.MANUAL,
            is_latest_stable=True,
        )
        assert checkpoint.id is not None

        restored = checkpoint_service.restore_latest(
            session=session,
            session_id="session-1",
            stable_only=True,
        )
        assert restored is not None
        assert restored.state_json == '{"step": 1}'
