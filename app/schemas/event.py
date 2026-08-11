import base64
import binascii
from datetime import date, time

from pydantic import BaseModel, Field, HttpUrl, field_validator


class EventCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str

    photos: list[str] = Field(default_factory=list)

    student_coordinators: list[str] = Field(default_factory=list)
    staff_coordinators: list[str] = Field(default_factory=list)

    chief_guest: str

    chief_guest_profile_urls: list[HttpUrl] = Field(default_factory=list)

    date: date
    time: time

    venue: str

    registration_form_link: HttpUrl

    @field_validator("photos")
    @classmethod
    def validate_photos(cls, photos: list[str]) -> list[str]:
        for photo in photos:
            try:
                base64.b64decode(
                    photo,
                    validate=True,
                )
            except (ValueError, binascii.Error):
                raise ValueError(
                    "Each photo must be a valid Base64-encoded string"
                )

        return photos


class EventResponse(EventCreate):
    pass