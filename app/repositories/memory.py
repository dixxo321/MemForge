from typing import Optional

from sqlmodel import Session, or_, select

from app.models import Memory
from app.repositories.base import BaseRepository


class MemoryRepository(BaseRepository[Memory]):
    def __init__(self) -> None:
        super().__init__(Memory)

    def list_memories(
        self,
        session: Session,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Memory]:
        statement = select(Memory)

        if user_id:
            statement = statement.where(Memory.user_id == user_id)
        if agent_id:
            statement = statement.where(Memory.agent_id == agent_id)
        if session_id:
            statement = statement.where(Memory.session_id == session_id)
        if project_id:
            statement = statement.where(Memory.project_id == project_id)
        if memory_type:
            statement = statement.where(Memory.memory_type == memory_type)

        statement = statement.offset(offset).limit(limit)
        return list(session.exec(statement).all())

    def search_text(
        self,
        session: Session,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 20,
    ) -> list[Memory]:
        statement = select(Memory).where(
            or_(
                Memory.content.contains(query),
                Memory.summary.contains(query),
                Memory.normalized_content.contains(query),
            )
        )

        if user_id:
            statement = statement.where(Memory.user_id == user_id)
        if agent_id:
            statement = statement.where(Memory.agent_id == agent_id)

        statement = statement.limit(limit)
        return list(session.exec(statement).all())
