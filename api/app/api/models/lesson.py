from typing import List
from uuid import UUID

from pydantic import BaseModel


class Scope(BaseModel):
    prerequisite_concepts: List[str]
    out_of_scope: List[str]

class Concept(BaseModel):
    explanation: str
    key_points: List[str]

class Example(BaseModel):
    input: str
    output: str
    explanation: str

class Task(BaseModel):
    prompt: str
    instructions: str
    response_type: str
    expected_format: str

class LessonPayload(BaseModel):
    lesson_id: UUID
    goal: str
    title: str
    scope: Scope
    concept: Concept
    example: Example
    task: Task
