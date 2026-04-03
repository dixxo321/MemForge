from __future__ import annotations

from typing import Any


def build_prompt_context(results: list[dict[str, Any]], max_items: int = 5) -> str:
    lines: list[str] = []
    lines.append("Relevant memory context:")

    for idx, item in enumerate(results[:max_items], start=1):
        memory = item["memory"]
        reason = item.get("why_this_memory_matched", "relevant match")
        lines.append(f"{idx}. [{memory.memory_type}] {memory.content}")
        lines.append(f"   Why: {reason}")
        if memory.summary:
            lines.append(f"   Summary: {memory.summary}")

    return "\n".join(lines)
