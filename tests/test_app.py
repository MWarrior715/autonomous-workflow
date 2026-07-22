"""Tests for the optional FastAPI app."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_run_default():
    response = client.get("/run")
    assert response.status_code == 200
    data = response.json()
    assert data["workflow"] == "Autonomous Workflow Agent"
    assert "classification" in data
    assert "proposal" in data


def test_run_with_lead():
    payload = {
        "name": "API Test",
        "company": "API Corp",
        "need": "Test need",
        "budget": "$1k",
        "timeline": "1 semana",
        "source": "api-test",
    }
    response = client.post("/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["lead"]["company"] == "API Corp"
    assert data["proposal"]["subject"]
