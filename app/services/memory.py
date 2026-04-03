from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Session

from app.models import Memory, MemoryStatus, MemoryType, PrivacyScope
from app.repositories import MemoryRepository


class MemoryService:
    def __init__(self, repository: Optional[MemoryRepository] = None) -> None:
        self.repository = repository or MemoryRepository()

    def add_memory(
        self,
        session: Session,
        *,
        user_id: str,
        agent_id: str,
        content: str,
        memory_type: MemoryType = MemoryType.SEMANTIC,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        summary: Optional[str] = None,
        source_type: Optional[str] = None,
        source_id: Optional[str] = None,
        importance_score: float = 0.5,
        salience_score: float = 0.5,
        confidence_score: float = 1.0,
        recency_score: float = 0.5,
        privacy_scope: PrivacyScope = PrivacyScope.PRIVATE,
    ) -> Memory:
        normalized_content = " ".join(content.strip().lower().split())

        memory = Memory(
            user_id=user_id,
            agent_id=agent_id,
            session_id=session_id,
            project_id=project_id,
            memory_type=memory_type,
            status=MemoryStatus.ACTIVE,
            privacy_scope=privacy_scope,
            content=content,
            normalized_content=normalized_content,
            summary=summary,
            source_type=source_type,
            source_id=source_id,
            importance_score=importance_score,
            salience_score=salience_score,
            confidence_score=confidence_score,
            recency_score=recency_score,
        )
        return self.repository.create(session, memory)

    def list_memories(
        self,
        session: Session,
        *,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Memory]:
        return self.repository.list_memories(
            session=session,
            user_id=user_id,
            agent_id=agent_id,
            session_id=session_id,
            project_id=project_id,
            memory_type=memory_type,
            limit=limit,
            offset=offset,
        )

    def update_memory_access(self, session: Session, memory: Memory) -> Memory:
        memory.access_count += 1
        memory.last_accessed_at = datetime.utcnow()
        return self.repository.save(session, memory)

    def delete_memory(self, session: Session, memory_id: str) -> bool:
        memory = self.repository.get(session, memory_id)
        if not memory:
            return False
        self.repository.delete(session, memory)
        return True
