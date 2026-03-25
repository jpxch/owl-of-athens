from fastapi import APIRouter, HTTPException

from app.api.models.requests import GenerateLessonRequest
from app.services.provider import (
    OpenAIContractProvider,
    ProviderConfigurationError,
    ProviderResponseError,
    ProviderSchemaError,
)

router = APIRouter(prefix="", tags=["lesson"])


@router.post("/generate-lesson")
def generate_lesson(req: GenerateLessonRequest) -> dict:
    """
    Temporary Phase 1 route.

    Expected incoming shape for now:
    {
        "goal": "learn python loops"
    }

    Request schema formalization can be added next as Pydantic request models,
    but the provider contract remains JSON Schema-based for model output.
    """
    try:
        provider = OpenAIContractProvider()
        lesson = provider.generate_lesson(goal=req.goal)
    except ProviderConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ProviderResponseError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ProviderSchemaError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return lesson