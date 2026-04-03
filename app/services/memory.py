from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Session

from app.models import Memory, MemoryStatus, MemoryType, PrivacyScope
from app.pipelines.write_pipeline import (
    detect_simple_contradiction,
    estimate_importance,
    estimate_salience,
    find_duplicate_memory,
    is_memory_worthy,
    normalize_text,
)
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
        importance_score: Optional[float] = None,
        salience_score: Optional[float] = None,
        confidence_score: float = 1.0,
        recency_score: float = 0.5,
        privacy_scope: PrivacyScope = PrivacyScope.PRIVATE,
    ) -> Memory:
        normalized_content = normalize_text(content)

        if not is_memory_worthy(content):
            raise ValueError("Content is not memory-worthy enough to store.")

        existing = self.repository.list_memories(
            session=session,
            user_id=user_id,
            agent_id=agent_id,
            session_id=session_id,
            project_id=project_id,
            limit=200,
        )

        duplicate = find_duplicate_memory(existing, normalized_content)
        if duplicate:
            duplicate.access_count += 1
            duplicate.last_accessed_at = datetime.utcnow()
            if summary and not duplicate.summary:
                duplicate.summary = summary
            return self.repository.save(session, duplicate)

        contradiction = detect_simple_contradiction(existing, normalized_content)
        if contradiction:
            content = f"[POTENTIAL_CONTRADICTION_WITH:{contradiction.id}] {content}"
            summary = summary or "Potential contradiction detected"

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
            importance_score=importance_score if importance_score is not None else estimate_importance(content),
            salience_score=salience_score if salience_score is not None else estimate_salience(content),
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

    def recall_for_prompt(
        self,
        session: Session,
        *,
        query: str,
        retrieval_service,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 5,
    ) -> list[dict]:
        results = retrieval_service.search(
            session=session,
            query=query,
            user_id=user_id,
            agent_id=agent_id,
            limit=limit,
        )
        for item in results:
            self.update_memory_access(session, item["memory"])
        return results
