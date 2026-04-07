from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from app.services.provider import (
    OpenAIContractProvider,
    ProviderResponseError,
    ProviderSchemaError,
)


ROOT = Path(__file__).resolve().parents[2]

LESSON_MODEL_PAYLOAD: dict[str, Any] = {
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

LESSON_PAYLOAD = {
    "lesson_id": "123e4567-e89b-42d3-a456-426614174000",
    **LESSON_MODEL_PAYLOAD,
}


class FakeProvider(OpenAIContractProvider):
    def __init__(self, content: str) -> None:
        self._content = content
        self._model = "test-model"
        self._lesson_schema = self._load_test_schema("lesson.schema.json")
        self._evaluation_schema = self._load_test_schema("evaluation.schema.json")
        self._lesson_prompt_schema = self._build_lesson_prompt_schema()

    def _call_model(self, prompt: str) -> str:
        return self._content

    def _load_test_schema(self, filename: str) -> dict[str, Any]:
        path = ROOT / "core" / "contracts" / filename
        return json.loads(path.read_text(encoding="utf-8"))


def test_generate_lesson_rejects_non_json_model_output() -> None:
    provider = FakeProvider("definitely not json")

    with pytest.raises(ProviderResponseError, match="not valid JSON"):
        provider.generate_lesson(goal="learn python loops")


def test_generate_lesson_rejects_schema_invalid_model_output() -> None:
    provider = FakeProvider(json.dumps({"title": "Incomplete lesson"}))

    with pytest.raises(ProviderSchemaError, match="lesson.schema.json"):
        provider.generate_lesson(goal="learn python loops")


def test_evaluate_response_rejects_schema_invalid_model_output() -> None:
    provider = FakeProvider(
        json.dumps(
            {
                "score": 1.4,
                "feedback": "Too high to be valid",
                "correct": True,
                "next_action": "continue",
            }
        )
    )

    with pytest.raises(ProviderSchemaError, match="evaluation.schema.json"):
        provider.evaluate_response(
            lesson_payload=LESSON_PAYLOAD,
            learner_response="for n in range(1, 4): print(n)",
        )


def test_evaluate_response_injects_nullable_misconception() -> None:
    provider = FakeProvider(
        json.dumps(
            {
                "score": 0.8,
                "feedback": "Mostly right, but tighten the explanation.",
                "correct": False,
                "next_action": "review",
            }
        )
    )

    evaluation = provider.evaluate_response(
        lesson_payload=LESSON_PAYLOAD,
        learner_response="Loops run while the condition is true.",
    )

    assert evaluation["misconception"] is None
    assert evaluation["lesson_id"] == LESSON_PAYLOAD["lesson_id"]
