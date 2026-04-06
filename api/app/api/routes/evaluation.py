from fastapi import APIRouter, HTTPException

from app.api.models.requests import EvaluateRequest
from app.services.provider import (
    OpenAIContractProvider,
    ProviderConfigurationError,
    ProviderResponseError,
    ProviderSchemaError,
)

router = APIRouter(prefix="", tags=["evaluation"])


@router.post("/evaluate-response")
def evaluate_response(req: EvaluateRequest) -> dict:
    """
    Temporary Phase 1 route.

    Expected incoming shape for now:
    {
        "lesson": { ...full lesson payload... },
        "learner_response": "..."
    }
    """
    try:
        provider = OpenAIContractProvider()
        evaluation = provider.evaluate_response(
            lesson_payload=req.lesson.model_dump(mode="json"),
            learner_response=req.learner_response,
        )
    except ProviderConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ProviderResponseError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ProviderSchemaError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return evaluation
