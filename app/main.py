from fastapi import FastAPI

from app.routes.events import router as events_router


app = FastAPI(
    title="Event Management API",
    description="Microservice for managing college events",
    version="1.0.0",
)


app.include_router(events_router)


@app.get("/health")
def health():
    return {"status": "ok"}