from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.errors import api_error_response
from app.api.models.requests import GenerateLessonRequest
from app.services.provider import (
    OpenAIContractProvider,
    ProviderConfigurationError,
    ProviderResponseError,
    ProviderSchemaError,
)

router = APIRouter(prefix="", tags=["lesson"])


@router.post("/generate-lesson")
def generate_lesson(req: GenerateLessonRequest) -> dict | JSONResponse:
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

    return lesson
