from fastapi import FastAPI

from app.routes.events import router as events_router


app = FastAPI(
    title="Event Management API",
    description=(
        "Microservice for creating and retrieving "
        "college events."
    ),
    version="1.0.0",
)


app.include_router(events_router)


@app.get(
    "/health",
    tags=["Health"],
)
def health() -> dict[str, str]:
    return {
        "status": "ok"
    }