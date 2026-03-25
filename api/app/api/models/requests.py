from pydantic import BaseModel

from app.api.models.lesson import LessonPayload


class GenerateLessonRequest(BaseModel):
    goal: str


class EvaluateRequest(BaseModel):
    lesson: LessonPayload
    learner_response: str