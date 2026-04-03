from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.is_sqlite else {}
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args=connect_args,
)


def init_db() -> None:
    """
    Bootstrap database tables for early local development.

    Later, Alembic migrations will become the primary schema management path.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
