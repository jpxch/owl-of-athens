from fastapi import FastAPI

from app.api.routes.evaluation import router as evaluation_router
from app.api.routes.lesson import router as lesson_router

app = FastAPI(
    title="owl-of-athens",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(lesson_router)
app.include_router(evaluation_router)