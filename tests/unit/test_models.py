from sqlmodel import SQLModel

from app.models import Memory, User


def test_models_import() -> None:
    assert User is not None
    assert Memory is not None
    assert SQLModel is not None
