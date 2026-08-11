from fastapi import APIRouter, Depends, HTTPException, status

from app.database import events_collection
from app.dependencies.auth import verify_api_key
from app.schemas.event import EventCreate, EventResponse


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_event(event: EventCreate) -> EventResponse:
    """
    Create a new event.
    """

    event_data = event.model_dump(mode="json")

    result = events_collection.insert_one(event_data)

    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event",
        )

    return EventResponse(**event_data)


@router.get(
    "",
    response_model=list[EventResponse],
    dependencies=[Depends(verify_api_key)],
)
def get_events() -> list[EventResponse]:
    """
    Return all events.
    """

    events = events_collection.find(
        {},
        {"_id": 0},
    )

    return [
        EventResponse(**event)
        for event in events
    ]