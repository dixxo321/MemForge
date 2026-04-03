from app.models import RetrievalLog
from app.repositories.base import BaseRepository


class RetrievalLogRepository(BaseRepository[RetrievalLog]):
    def __init__(self) -> None:
        super().__init__(RetrievalLog)
