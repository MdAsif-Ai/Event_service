from datetime import date, time

from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import HttpUrl, TypeAdapter, ValidationError

from app.database import events_collection
from app.dependencies.auth import verify_api_key
from app.schemas.event import EventResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


http_url_adapter = TypeAdapter(HttpUrl)


def parse_comma_separated_urls(value: str) -> list[HttpUrl]:
    """
    Convert comma-separated URLs into a list of validated URLs.
    """

    if not value.strip():
        return []

    urls = []

    for item in value.split(","):
        item = item.strip()

        if not item:
            continue

        try:
            urls.append(
                http_url_adapter.validate_python(item)
            )
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid URL: {item}",
            )

    return urls


def parse_comma_separated_strings(value: str) -> list[str]:
    """
    Convert comma-separated text into a list of strings.
    """

    if not value.strip():
        return []

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_event(
    title: str = Form(...),
    description: str = Form(...),

    photos: str = Form(
        default="",
        description=(
            "Comma-separated image URLs. "
            "Example: https://example.com/image1.jpg,"
            "https://example.com/image2.jpg"
        ),
    ),

    student_coordinators: str = Form(
        default="",
        description="Comma-separated student coordinator names.",
    ),

    staff_coordinators: str = Form(
        default="",
        description="Comma-separated staff coordinator names.",
    ),

    chief_guest: str = Form(...),

    chief_guest_profile_urls: str = Form(
        default="",
        description="Comma-separated chief guest profile image URLs.",
    ),

    date: date = Form(...),

    time: time = Form(...),

    venue: str = Form(...),

    registration_form_link: HttpUrl | None = Form(
        default=None,
        description="Registration Form link optional"
    ),
) -> EventResponse:
    """
    Create a new event.

    Image files are NOT stored by this API.
    The API receives image URLs and stores those URLs in MongoDB.
    """

    photo_urls = parse_comma_separated_urls(photos)

    chief_guest_urls = parse_comma_separated_urls(
        chief_guest_profile_urls
    )

    student_list = parse_comma_separated_strings(
        student_coordinators
    )

    staff_list = parse_comma_separated_strings(
        staff_coordinators
    )

    event_data = {
        "title": title.strip(),
        "description": description.strip(),
        "photos": [
            str(url)
            for url in photo_urls
        ],
        "student_coordinators": student_list,
        "staff_coordinators": staff_list,
        "chief_guest": chief_guest.strip(),
        "chief_guest_profile_urls": [
            str(url)
            for url in chief_guest_urls
        ],
        "date": date.isoformat(),
        "time": time.isoformat(),
        "venue": venue.strip(),
        "registration_form_link": (
            str(registration_form_link)
            if registration_form_link is not None
            else None
        ),
    }

    try:
        result = events_collection.insert_one(
            event_data
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event.",
        ) from exc

    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event.",
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

    try:
        events = events_collection.find(
            {},
            {"_id": 0},
        )

        return [
            EventResponse(**event)
            for event in events
        ]

    except Exception as e:
        logger.exception("Failed to create event")
        raise HTTPException(
            status_code=500,
            detail=f"MongoDB error: {str(e)}"
        ) from e