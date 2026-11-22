import os

os.environ.setdefault("POSTGRES_USER", "postgres_user_test")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres_password_test")
os.environ.setdefault("POSTGRES_DB", "postgres_db_test")
os.environ.setdefault("SECRET_TOKEN", "token_test")
os.environ.setdefault("MAX_HOURS_LIMIT", "250")
os.environ.setdefault("REDIS_URL", "redis://redis:6379/0")
os.environ.setdefault("POSTGRES_HOST", "db")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.celery_app import run_heavy_task
from app.db.session import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_celery_delay(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(run_heavy_task, "delay", mock)
    return mock
