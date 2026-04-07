from __future__ import annotations

from fastapi.responses import JSONResponse


def api_error_response(
    *,
    status_code: int,
    message: str,
    error_type: str,
    source: str,
    retryable: bool,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": message,
            "error": {
                "type": error_type,
                "source": source,
                "retryable": retryable,
            },
        },
    )
