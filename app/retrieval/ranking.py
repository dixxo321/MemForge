from __future__ import annotations

from typing import Any

from app.models import Memory


def normalize_query(query: str) -> str:
    return " ".join(query.strip().lower().split())


def score_memory_keyword_match(memory: Memory, normalized_query: str) -> float:
    haystacks = [
        memory.content or "",
        memory.summary or "",
        memory.normalized_content or "",
    ]
    joined = " ".join(haystacks).lower()
    if not normalized_query:
        return 0.0

    score = 0.0
    for token in normalized_query.split():
        if token in joined:
            score += 1.0

    score += float(memory.importance_score or 0.0) * 0.25
    score += float(memory.salience_score or 0.0) * 0.25
    score += float(memory.recency_score or 0.0) * 0.15
    return score


def rank_memories(memories: list[Memory], query: str) -> list[dict[str, Any]]:
    normalized = normalize_query(query)
    ranked: list[dict[str, Any]] = []

    for memory in memories:
        score = score_memory_keyword_match(memory, normalized)
        ranked.append(
            {
                "memory": memory,
                "score": score,
                "matched_by": "keyword",
                "why_this_memory_matched": f"Matched query terms against content/summary for '{normalized}'.",
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked
