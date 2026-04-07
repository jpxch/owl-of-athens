from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

import app.api.routes.evaluation as evaluation_routes
import app.api.routes.lesson as lesson_routes
from main import app
from app.services.provider import ProviderResponseError, ProviderSchemaError


client = TestClient(app)


LESSON_PAYLOAD: dict[str, Any] = {
    "lesson_id": "123e4567-e89b-42d3-a456-426614174000",
    "goal": "learn python loops",
    "title": "Python loops basics",
    "scope": {
        "prerequisite_concepts": ["variables"],
        "out_of_scope": ["list comprehensions"],
    },
    "concept": {
        "explanation": "Loops repeat an action until a condition changes.",
        "key_points": ["for iterates", "while repeats on condition"],
    },
    "example": {
        "input": "for n in range(3): print(n)",
        "output": "0\n1\n2",
        "explanation": "The loop prints each integer in the range.",
    },
    "task": {
        "prompt": "Write a loop that prints numbers 1 to 3.",
        "instructions": "Use a for loop.",
        "response_type": "code",
        "expected_format": "Python code block or plain Python code.",
    },
}

EVALUATION_PAYLOAD: dict[str, Any] = {
    "lesson_id": LESSON_PAYLOAD["lesson_id"],
    "response_type": "code",
    "learner_response": "for n in range(1, 4): print(n)",
    "score": 1.0,
    "feedback": "This is correct and uses the right range boundaries.",
    "correct": True,
    "next_action": "continue",
    "misconception": None,
}


class StubLessonProvider:
    def generate_lesson(self, goal: str) -> dict[str, Any]:
        assert goal == "learn python loops"
        return LESSON_PAYLOAD


class StubEvaluationProvider:
    def evaluate_response(
        self,
        lesson_payload: dict[str, Any],
        learner_response: str,
    ) -> dict[str, Any]:
        assert lesson_payload["lesson_id"] == LESSON_PAYLOAD["lesson_id"]
        assert learner_response == "for n in range(1, 4): print(n)"
        return EVALUATION_PAYLOAD


class StubBrokenLessonProvider:
    def generate_lesson(self, goal: str) -> dict[str, Any]:
        raise ProviderResponseError("Model output was not valid JSON: Expecting value")


class StubBrokenEvaluationProvider:
    def evaluate_response(
        self,
        lesson_payload: dict[str, Any],
        learner_response: str,
    ) -> dict[str, Any]:
        raise ProviderSchemaError(
            "Payload failed validation against evaluation.schema.json: 1.4 is greater than the maximum of 1"
        )


def test_generate_lesson_route_returns_provider_payload(monkeypatch) -> None:
    monkeypatch.setattr(lesson_routes, "OpenAIContractProvider", StubLessonProvider)

    response = client.post("/generate-lesson", json={"goal": "learn python loops"})

    assert response.status_code == 200
    assert response.json() == LESSON_PAYLOAD


def test_generate_lesson_invalid_payload_returns_400() -> None:
    response = client.post("/generate-lesson", json={"goal": "   "})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid request payload."
    assert response.json()["errors"][0]["location"] == "body.goal"


def test_generate_lesson_provider_response_error_returns_structured_502(monkeypatch) -> None:
    monkeypatch.setattr(lesson_routes, "OpenAIContractProvider", StubBrokenLessonProvider)

    response = client.post("/generate-lesson", json={"goal": "learn python loops"})

    assert response.status_code == 502
    assert response.json()["detail"].startswith("Model output was not valid JSON")
    assert response.json()["error"] == {
        "type": "provider_response_error",
        "source": "provider",
        "retryable": True,
    }


def test_evaluate_response_route_returns_provider_payload(monkeypatch) -> None:
    monkeypatch.setattr(
        evaluation_routes,
        "OpenAIContractProvider",
        StubEvaluationProvider,
    )

    response = client.post(
        "/evaluate-response",
        json={
            "lesson": LESSON_PAYLOAD,
            "learner_response": "for n in range(1, 4): print(n)",
        },
    )

    assert response.status_code == 200
    assert response.json() == EVALUATION_PAYLOAD


def test_evaluate_response_invalid_payload_returns_400() -> None:
    response = client.post(
        "/evaluate-response",
        json={
            "lesson": LESSON_PAYLOAD,
            "learner_response": "   ",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid request payload."
    assert response.json()["errors"][0]["location"] == "body.learner_response"


def test_evaluate_response_invalid_lesson_id_returns_400() -> None:
    bad_lesson = dict(LESSON_PAYLOAD)
    bad_lesson["lesson_id"] = "not-a-uuid"

    response = client.post(
        "/evaluate-response",
        json={
            "lesson": bad_lesson,
            "learner_response": "for n in range(1, 4): print(n)",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid request payload."
    assert response.json()["errors"][0]["location"] == "body.lesson.lesson_id"


def test_evaluate_response_provider_schema_error_returns_structured_502(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        evaluation_routes,
        "OpenAIContractProvider",
        StubBrokenEvaluationProvider,
    )

    response = client.post(
        "/evaluate-response",
        json={
            "lesson": LESSON_PAYLOAD,
            "learner_response": "for n in range(1, 4): print(n)",
        },
    )

    assert response.status_code == 502
    assert "evaluation.schema.json" in response.json()["detail"]
    assert response.json()["error"] == {
        "type": "provider_schema_error",
        "source": "provider",
        "retryable": True,
    }
