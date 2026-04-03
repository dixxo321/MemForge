from typing import Generic, Optional, Type, TypeVar

from sqlmodel import Session, select

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: Type[ModelT]):
        self.model = model

    def get(self, session: Session, object_id: str) -> Optional[ModelT]:
        return session.get(self.model, object_id)

    def list(self, session: Session, limit: int = 100, offset: int = 0) -> list[ModelT]:
        statement = select(self.model).offset(offset).limit(limit)
        return list(session.exec(statement).all())

    def create(self, session: Session, obj: ModelT) -> ModelT:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def save(self, session: Session, obj: ModelT) -> ModelT:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, obj: ModelT) -> None:
        session.delete(obj)
        session.commit()
