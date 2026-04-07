from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.evaluation import router as evaluation_router
from app.api.routes.lesson import router as lesson_router
from app.core.config import settings

app = FastAPI(
    title="owl-of-athens",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = []

    for error in exc.errors():
        location = ".".join(str(part) for part in error.get("loc", []))
        errors.append(
            {
                "location": location,
                "message": error.get("msg", "Invalid value."),
                "type": error.get("type", "validation_error"),
            }
        )

    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request payload.",
            "errors": errors,
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(lesson_router)
app.include_router(evaluation_router)
