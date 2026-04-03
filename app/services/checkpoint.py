from __future__ import annotations

from typing import Optional

from sqlmodel import Session

from app.models import Checkpoint, CheckpointKind
from app.repositories import CheckpointRepository


class CheckpointService:
    def __init__(self, repository: Optional[CheckpointRepository] = None) -> None:
        self.repository = repository or CheckpointRepository()

    def save_checkpoint(
        self,
        session: Session,
        *,
        user_id: str,
        agent_id: str,
        state_json: str,
        kind: CheckpointKind = CheckpointKind.AUTO,
        session_id: Optional[str] = None,
        project_id: Optional[str] = None,
        name: Optional[str] = None,
        planner_state_json: Optional[str] = None,
        tool_state_json: Optional[str] = None,
        partial_output: Optional[str] = None,
        parent_checkpoint_id: Optional[str] = None,
        is_latest_stable: bool = False,
    ) -> Checkpoint:
        checkpoint = Checkpoint(
            user_id=user_id,
            agent_id=agent_id,
            session_id=session_id,
            project_id=project_id,
            kind=kind,
            name=name,
            state_json=state_json,
            planner_state_json=planner_state_json,
            tool_state_json=tool_state_json,
            partial_output=partial_output,
            parent_checkpoint_id=parent_checkpoint_id,
            is_latest_stable=is_latest_stable,
        )
        return self.repository.create(session, checkpoint)

    def restore_latest(
        self,
        session: Session,
        *,
        session_id: str,
        stable_only: bool = False,
    ) -> Optional[Checkpoint]:
        if stable_only:
            return self.repository.latest_stable_for_session(session, session_id)
        return self.repository.latest_for_session(session, session_id)
