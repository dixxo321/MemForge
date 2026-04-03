import argparse
import json
from typing import Optional

from sqlmodel import Session

from app.core.config import get_settings
from app.core.database import engine, init_db
from app.services import MemoryService, RetrievalService


def cmd_initdb(args: argparse.Namespace) -> None:
    init_db()
    print("Database initialized.")


def cmd_doctor(args: argparse.Namespace) -> None:
    settings = get_settings()
    print("MemForge Doctor")
    print(f"App: {settings.app_name}")
    print(f"Env: {settings.env}")
    print(f"Database: {settings.database_url}")
    print(f"Vector backend: {settings.vector_backend}")
    print(f"Vector dir: {settings.vector_dir}")
    print(f"Embedding provider: {settings.embedding_provider}")
    print(f"Embedding model: {settings.embedding_model}")


def cmd_add_memory(args: argparse.Namespace) -> None:
    service = MemoryService()
    with Session(engine) as session:
        memory = service.add_memory(
            session=session,
            user_id=args.user_id,
            agent_id=args.agent_id,
            content=args.content,
            memory_type=args.memory_type,
            summary=args.summary,
            project_id=args.project_id,
            session_id=args.session_id,
        )
        print(json.dumps({"id": memory.id, "content": memory.content}, indent=2))


def cmd_list_memories(args: argparse.Namespace) -> None:
    service = MemoryService()
    with Session(engine) as session:
        memories = service.list_memories(
            session=session,
            user_id=args.user_id,
            agent_id=args.agent_id,
            limit=args.limit,
        )
        for memory in memories:
            print(
                json.dumps(
                    {
                        "id": memory.id,
                        "memory_type": str(memory.memory_type),
                        "content": memory.content,
                        "summary": memory.summary,
                    },
                    indent=2,
                )
            )


def cmd_search_memory(args: argparse.Namespace) -> None:
    service = RetrievalService()
    with Session(engine) as session:
        results = service.search(
            session=session,
            query=args.query,
            user_id=args.user_id,
            agent_id=args.agent_id,
            limit=args.limit,
        )
        for item in results:
            memory = item["memory"]
            print(
                json.dumps(
                    {
                        "id": memory.id,
                        "score": item["score"],
                        "matched_by": item["matched_by"],
                        "why": item["why_this_memory_matched"],
                        "content": memory.content,
                        "summary": memory.summary,
                    },
                    indent=2,
                )
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="memforge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("doctor")
    p.set_defaults(func=cmd_doctor)

    p = subparsers.add_parser("initdb")
    p.set_defaults(func=cmd_initdb)

    p = subparsers.add_parser("add-memory")
    p.add_argument("user_id")
    p.add_argument("agent_id")
    p.add_argument("content")
    p.add_argument("--memory-type", default="semantic")
    p.add_argument("--summary", default=None)
    p.add_argument("--project-id", default=None)
    p.add_argument("--session-id", default=None)
    p.set_defaults(func=cmd_add_memory)

    p = subparsers.add_parser("list-memories")
    p.add_argument("--user-id", default=None)
    p.add_argument("--agent-id", default=None)
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_list_memories)

    p = subparsers.add_parser("search-memory")
    p.add_argument("query")
    p.add_argument("--user-id", default=None)
    p.add_argument("--agent-id", default=None)
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search_memory)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
