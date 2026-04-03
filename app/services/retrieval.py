from __future__ import annotations

import json
import time
from typing import Any, Optional

from sqlmodel import Session

from app.models import RetrievalLog
from app.repositories import MemoryRepository, RetrievalLogRepository
from app.retrieval.prompt_builder import build_prompt_context
from app.retrieval.ranking import normalize_query, rank_memories


class RetrievalService:
    def __init__(
        self,
        memory_repository: Optional[MemoryRepository] = None,
        retrieval_log_repository: Optional[RetrievalLogRepository] = None,
    ) -> None:
        self.memory_repository = memory_repository or MemoryRepository()
        self.retrieval_log_repository = retrieval_log_repository or RetrievalLogRepository()

    def search(
        self,
        session: Session,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        started = time.time()
        normalized_query = normalize_query(query)

        candidates = self.memory_repository.search_text(
            session=session,
            query=query,
            user_id=user_id,
            agent_id=agent_id,
            limit=max(limit * 3, 10),
        )

        ranked = rank_memories(candidates, query)[:limit]

        log = RetrievalLog(
            user_id=user_id or "unknown",
            agent_id=agent_id,
            query_text=query,
            normalized_query=normalized_query,
            strategy="keyword_v1",
            result_ids_json=json.dumps([item["memory"].id for item in ranked]),
            latency_ms=int((time.time() - started) * 1000),
        )
        self.retrieval_log_repository.create(session, log)

        return ranked

    def recall_for_prompt(
        self,
        session: Session,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 5,
    ) -> dict[str, Any]:
        results = self.search(
            session=session,
            query=query,
            user_id=user_id,
            agent_id=agent_id,
            limit=limit,
        )
        return {
            "results": results,
            "context_text": build_prompt_context(results, max_items=limit),
        }
