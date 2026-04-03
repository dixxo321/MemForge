from __future__ import annotations

from typing import Any, Optional

from sqlmodel import Session

from app.core.database import engine, init_db
from app.services import CheckpointService, MemoryService, RetrievalService


class MemForgeClient:
    def __init__(self) -> None:
        init_db()
        self.memory_service = MemoryService()
        self.retrieval_service = RetrievalService()
        self.checkpoint_service = CheckpointService()

    def add_memory(
        self,
        *,
        user_id: str,
        agent_id: str,
        content: str,
        memory_type: str = "semantic",
        summary: Optional[str] = None,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        with Session(engine) as session:
            return self.memory_service.add_memory(
                session=session,
                user_id=user_id,
                agent_id=agent_id,
                content=content,
                memory_type=memory_type,
                summary=summary,
                project_id=project_id,
                session_id=session_id,
            )

    def list_memories(
        self,
        *,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 20,
    ):
        with Session(engine) as session:
            return self.memory_service.list_memories(
                session=session,
                user_id=user_id,
                agent_id=agent_id,
                limit=limit,
            )

    def search_memory(
        self,
        *,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        with Session(engine) as session:
            return self.retrieval_service.search(
                session=session,
                query=query,
                user_id=user_id,
                agent_id=agent_id,
                limit=limit,
            )

    def recall_for_prompt(
        self,
        *,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 5,
    ) -> dict[str, Any]:
        with Session(engine) as session:
            return self.retrieval_service.recall_for_prompt(
                session=session,
                query=query,
                user_id=user_id,
                agent_id=agent_id,
                limit=limit,
            )

    def save_checkpoint(
        self,
        *,
        user_id: str,
        agent_id: str,
        state_json: str,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        name: Optional[str] = None,
        kind: str = "auto",
        is_latest_stable: bool = False,
    ):
        with Session(engine) as session:
            return self.checkpoint_service.save_checkpoint(
                session=session,
                user_id=user_id,
                agent_id=agent_id,
                state_json=state_json,
                session_id=session_id,
                project_id=project_id,
                name=name,
                kind=kind,
                is_latest_stable=is_latest_stable,
            )

    def restore_latest_checkpoint(
        self,
        *,
        session_id: str,
        stable_only: bool = False,
    ):
        with Session(engine) as session:
            return self.checkpoint_service.restore_latest(
                session=session,
                session_id=session_id,
                stable_only=stable_only,
            )
