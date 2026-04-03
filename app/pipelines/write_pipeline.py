from __future__ import annotations

from typing import Optional

from app.models import Memory


def normalize_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def is_memory_worthy(text: str) -> bool:
    normalized = normalize_text(text)
    if len(normalized) < 8:
        return False

    useful_markers = [
        "prefer",
        "likes",
        "dislikes",
        "always",
        "never",
        "project",
        "task",
        "important",
        "remember",
        "deadline",
        "use ",
        "uses ",
    ]
    return any(marker in normalized for marker in useful_markers) or len(normalized) >= 24


def estimate_importance(text: str) -> float:
    normalized = normalize_text(text)
    score = 0.45

    if "important" in normalized or "deadline" in normalized:
        score += 0.25
    if "prefer" in normalized or "likes" in normalized or "dislikes" in normalized:
        score += 0.20
    if len(normalized) > 120:
        score += 0.10

    return min(score, 1.0)


def estimate_salience(text: str) -> float:
    normalized = normalize_text(text)
    score = 0.40

    if "remember" in normalized:
        score += 0.20
    if "project" in normalized or "task" in normalized:
        score += 0.20
    if "prefer" in normalized or "likes" in normalized:
        score += 0.15

    return min(score, 1.0)


def find_duplicate_memory(existing: list[Memory], normalized_content: str) -> Optional[Memory]:
    for memory in existing:
        if (memory.normalized_content or "") == normalized_content:
            return memory
    return None


def detect_simple_contradiction(existing: list[Memory], normalized_content: str) -> Optional[Memory]:
    contradiction_pairs = [
        ("likes", "dislikes"),
        ("always", "never"),
        ("yes", "no"),
        ("enabled", "disabled"),
    ]

    for memory in existing:
        current = (memory.normalized_content or "")
        for a, b in contradiction_pairs:
            if a in normalized_content and b in current:
                return memory
            if b in normalized_content and a in current:
                return memory
    return None
