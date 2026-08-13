from datetime import date, time

from pydantic import BaseModel, Field, HttpUrl


class EventResponse(BaseModel):
    """Event returned by the API."""

    title: str = Field(min_length=1)

    description: str

    photos: list[HttpUrl] = Field(
        default_factory=list
    )

    student_coordinators: list[str] = Field(
        default_factory=list
    )

    staff_coordinators: list[str] = Field(
        default_factory=list
    )

    chief_guest: str

    chief_guest_profile_urls: list[HttpUrl] = Field(
        default_factory=list
    )

    date: date

    time: time

    venue: str

    registration_form_link: HttpUrl