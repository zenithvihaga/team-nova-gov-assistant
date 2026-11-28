
"""Dependency providers for the backend REST API.

These providers manage shared application components and allow API
endpoints to access them without creating their own instances.
"""

import logging
from functools import lru_cache

from fastapi import HTTPException, status

from app.repositories.service_repository import (
    CatalogLoadError,
    ServiceRepository,
)


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_service_repository() -> ServiceRepository:
    """Provide a reusable and validated service repository instance."""

    try:
        # Reuse the repository instead of loading the JSON file
        # separately for every API request.
        return ServiceRepository()

    except CatalogLoadError as exc:
        # Record technical details in server logs without exposing
        # internal file paths or errors to API clients.
        logger.exception("Failed to initialize the service repository.")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Government service information is temporarily unavailable.",
        ) from exc
