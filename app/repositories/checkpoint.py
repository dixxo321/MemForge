from typing import Optional

from sqlmodel import Session, desc, select

from app.models import Checkpoint
from app.repositories.base import BaseRepository


class CheckpointRepository(BaseRepository[Checkpoint]):
    def __init__(self) -> None:
        super().__init__(Checkpoint)

    def latest_for_session(
        self,
        session: Session,
        session_id: str,
    ) -> Optional[Checkpoint]:
        statement = (
            select(Checkpoint)
            .where(Checkpoint.session_id == session_id)
            .order_by(desc(Checkpoint.created_at))
            .limit(1)
        )
        return session.exec(statement).first()

    def latest_stable_for_session(
        self,
        session: Session,
        session_id: str,
    ) -> Optional[Checkpoint]:
        statement = (
            select(Checkpoint)
            .where(Checkpoint.session_id == session_id)
            .where(Checkpoint.is_latest_stable == True)
            .order_by(desc(Checkpoint.created_at))
            .limit(1)
        )
        return session.exec(statement).first()
