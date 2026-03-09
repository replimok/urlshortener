import pytest
import sys
import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["ENVIRONMENT"] = "test"

from src.main import app
from src.database import Base, get_db
from src.config import config



SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


def test_create_short_id(client):
    response = client.post("/shorten", json={"original_url": "https://example.com"})
    assert response.status_code == 200

    data = response.json()
    assert "short_id" in data
    assert len(data["short_id"]) == config.SHORT_ID_LENGTH


def test_redirect(client):
    original_url = "https://example.com/"
    create_response = client.post("/shorten", json={"original_url": original_url})
    short_id = create_response.json()["short_id"]

    redirect_response = client.get(f"/{short_id}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == original_url
