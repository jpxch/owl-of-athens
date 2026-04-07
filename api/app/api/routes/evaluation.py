from fastapi import APIRouter

from app.api.errors import api_error_response
from app.api.models.requests import EvaluateRequest
from app.services.provider import (
    OpenAIContractProvider,
    ProviderConfigurationError,
    ProviderResponseError,
    ProviderSchemaError,
)

router = APIRouter(prefix="", tags=["evaluation"])


@router.post("/evaluate-response", response_model=None)
def evaluate_response(req: EvaluateRequest):
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
    except ValueError as exc:
        return api_error_response(
            status_code=400,
            message=str(exc),
            error_type="invalid_input",
            source="request",
            retryable=False,
        )
    except ProviderConfigurationError as exc:
        return api_error_response(
            status_code=500,
            message=str(exc),
            error_type="provider_configuration_error",
            source="provider",
            retryable=False,
        )
    except ProviderResponseError as exc:
        return api_error_response(
            status_code=502,
            message=str(exc),
            error_type="provider_response_error",
            source="provider",
            retryable=True,
        )
    except ProviderSchemaError as exc:
        return api_error_response(
            status_code=502,
            message=str(exc),
            error_type="provider_schema_error",
            source="provider",
            retryable=True,
        )

    return evaluation
