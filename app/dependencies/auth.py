import hashlib
import secrets

from fastapi import Header, HTTPException, status

from app.config import settings


def verify_api_key(
    x_api_key: str | None = Header(default=None),
) -> None:
    """
    Verify the API key provided in the X-API-Key header.

    The received API key is hashed with SHA-256 and
    compared against the configured API_KEY_HASH.
    """

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )

    received_key_hash = hashlib.sha256(
        x_api_key.encode("utf-8")
    ).hexdigest()

    if not secrets.compare_digest(
        received_key_hash,
        settings.api_key_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )