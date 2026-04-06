from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.api.models.lesson import LessonPayload


def build_lesson_payload(*, lesson_id: str) -> dict:
    return {
        "lesson_id": lesson_id,
        "goal": "learn python loops",
        "title": "Intro to Python Loops",
        "scope": {
            "prerequisite_concepts": ["variables"],
            "out_of_scope": ["asyncio"],
        },
        "concept": {
            "explanation": "Loops repeat actions.",
            "key_points": ["for loops", "while loops"],
        },
        "example": {
            "input": "for i in range(3): print(i)",
            "output": "0\n1\n2",
            "explanation": "The loop prints three numbers.",
        },
        "task": {
            "prompt": "Write a loop that prints 1 through 3.",
            "instructions": "Use a for loop.",
            "response_type": "code",
            "expected_format": "Python code block",
        },
    }


def test_lesson_payload_accepts_uuid_lesson_id() -> None:
    lesson = LessonPayload(**build_lesson_payload(lesson_id=str(uuid4())))

    dumped = lesson.model_dump(mode="json")

    assert isinstance(dumped["lesson_id"], str)


def test_lesson_payload_rejects_non_uuid_lesson_id() -> None:
    with pytest.raises(ValidationError):
        LessonPayload(**build_lesson_payload(lesson_id="not-a-uuid"))
