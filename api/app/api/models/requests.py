from pydantic import BaseModel, ConfigDict, Field

from app.api.models.lesson import LessonPayload


class GenerateLessonRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    goal: str = Field(min_length=1)


class EvaluateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    lesson: LessonPayload
    learner_response: str = Field(min_length=1)
