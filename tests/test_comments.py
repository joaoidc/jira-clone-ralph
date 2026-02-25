import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Base, User, Issue, Comment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in test database
Base.metadata.create_all(bind=engine)

# Override dependency to use test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_user():
    # Create test user
    db = TestingSessionLocal()
    user = User(
        id="testuser123",
        email="test@example.com",
        hashed_password="testpassword"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_issue():
    # Create test issue
    db = TestingSessionLocal()
    issue = Issue(
        id="testissue456",
        title="Test Issue",
        description="This is a test issue",
        project_id="testproject789"
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue

def test_create_comment(test_user, test_issue):
    # Create test comment
    response = client.post(
        f"/comments/issues/{test_issue.id}",
        json={"content": "This is a test comment"},
        headers={"Authorization": f"Bearer testtoken"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert "id" in data
    assert data["content"] == "This is a test comment"
    assert data["user_id"] == test_user.id

def test_get_issue_with_comments(test_user, test_issue):
    # Create test comment
    client.post(
        f"/comments/issues/{test_issue.id}",
        json={"content": "This is a test comment"},
        headers={"Authorization": f"Bearer testtoken"}
    )
    
    # Get issue with comments
    response = client.get(f"/comments/issues/{test_issue.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "comments" in data
    assert len(data["comments"]) == 1
    assert data["comments"][0]["content"] == "This is a test comment"
