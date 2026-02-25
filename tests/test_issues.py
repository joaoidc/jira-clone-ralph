import pytest
from fastapi.testclient import TestClient
from main import app
from utils.status_transitions import Status, Transition, ALLOWED_TRANSITIONS

client = TestClient(app)

def test_update_issue_status_valid_transition():
    response = client.patch("/issues/123/status", json={"new_status": "In Progress"})
    assert response.status_code == 200
    assert response.json() == {"message": "Status updated successfully"}

def test_update_issue_status_invalid_status():
    response = client.patch("/issues/123/status", json={"new_status": "Invalid Status"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid status"}

def test_update_issue_status_invalid_transition():
    response = client.patch("/issues/123/status", json={"new_status": "Done"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid transition"}
