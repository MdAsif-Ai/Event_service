import hashlib
import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config import settings


api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def verify_api_key(
    x_api_key: str | None = Security(api_key_header),
) -> None:
    """
    Verify the API key supplied in the X-API-Key header.

    The API key itself is never stored.
    Its SHA-256 hash is compared with API_KEY_HASH.
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