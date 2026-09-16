"""Contract tests for the Student VISOLACE Agent."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_identity() -> None:
    response = client.get("/identity")
    assert response.status_code == 200
    assert response.json() == {
        "agent_id": "student-agent",
        "name": "Student VISOLACE Agent",
        "version": "0.1.0",
    }


def test_task_returns_structured_result() -> None:
    response = client.post(
        "/task", json={"task_id": "task-001", "text": "Hello VISOLACE"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "task_id": "task-001",
        "status": "completed",
        "result": {
            "original_text": "Hello VISOLACE",
            "word_count": 2,
            "character_count": 14,
        },
    }


def test_task_counts_words_across_extra_whitespace() -> None:
    text = "One   two\nthree"
    response = client.post("/task", json={"task_id": "task-002", "text": text})
    assert response.status_code == 200
    assert response.json()["result"] == {
        "original_text": text,
        "word_count": 3,
        "character_count": len(text),
    }


def test_task_rejects_missing_text() -> None:
    response = client.post("/task", json={"task_id": "task-003"})
    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"
    assert body["message"] == "Invalid request"
    assert body["errors"][0]["field"] == "text"


def test_task_rejects_whitespace_only_text() -> None:
    response = client.post("/task", json={"task_id": "task-004", "text": "   "})
    assert response.status_code == 400
    assert response.json()["status"] == "error"


def test_task_rejects_wrong_types() -> None:
    response = client.post("/task", json={"task_id": 123, "text": ["hello"]})
    assert response.status_code == 400
    assert len(response.json()["errors"]) == 2
