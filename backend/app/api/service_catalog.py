
"""REST API endpoints for the government service catalog.

This module exposes validated government service information to
client applications through versioned, read-only REST endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_service_repository
from app.models.government_service import (
    GovernmentService,
    ServiceGroup,
)
from app.repositories.service_repository import ServiceRepository


# Group catalog endpoints under a versioned API prefix.
router = APIRouter(
    prefix="/api/v1",
    tags=["Government Service Catalog"],
    responses={
        503: {"description": "Government service catalog unavailable"}
    },
)


# Inject the repository rather than creating it inside each endpoint.
RepositoryDependency = Annotated[
    ServiceRepository,
    Depends(get_service_repository),
]


@router.get(
    "/service-groups",
    response_model=list[ServiceGroup],
    summary="List government service groups",
)
def list_service_groups(
    repository: RepositoryDependency,
) -> list[ServiceGroup]:
    """Return all available government service groups."""

    return repository.list_service_groups()


@router.get(
    "/services",
    response_model=list[GovernmentService],
    summary="List government services",
    responses={
        404: {"description": "Service group not found"}
    },
)
def list_services(
    repository: RepositoryDependency,
    group_id: Annotated[
        str | None,
        Query(
            min_length=1,
            description="Filter services by the full service group name.",
        ),
    ] = None,
) -> list[GovernmentService]:
    """Return all services or filter them by their government service group."""

    # Reject unknown groups instead of returning misleading empty results.
    if group_id is not None:
        if repository.get_service_group(group_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Government service group not found.",
            )

    return repository.list_services(group_id=group_id)


@router.get(
    "/services/{service_id}",
    response_model=GovernmentService,
    summary="Get a government service by ID",
    responses={
        404: {"description": "Government service not found"}
    },
)
def get_service(
    service_id: str,
    repository: RepositoryDependency,
) -> GovernmentService:
    """Return the service record associated with the supplied identifier."""

    service = repository.get_service(service_id)

    # Return a controlled HTTP error when the requested service is absent.
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Government service not found.",
        )

    return service
