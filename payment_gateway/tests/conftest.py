import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Database
from app.config import get_settings

@pytest.fixture(scope="session")
def settings():
    return get_settings()

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup e cleanup de banco de dados de teste"""
    # Setup
    Database.connect()
    db = Database.get_db()
    
    yield db
    
    # Cleanup
    db.client.drop_database(db.name)