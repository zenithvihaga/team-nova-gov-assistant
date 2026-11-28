
"""Repository for accessing government service catalog data.

This module separates data storage and retrieval from the API layer,
allowing the storage implementation to evolve independently.
"""

from pathlib import Path

from pydantic import ValidationError

from app.models.government_service import (
    GovernmentService,
    ServiceCatalog,
    ServiceGroup,
)


# Resolve the data file relative to the backend directory.
# This avoids machine-specific absolute paths.
DEFAULT_CATALOG_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "service_catalog.json"
)


class CatalogLoadError(RuntimeError):
    """Indicate that the government service catalog could not be loaded."""


class ServiceRepository:
    """Provide read-only access to validated government service records."""

    def __init__(self, catalog_path: Path | None = None) -> None:
        """Initialize the repository using the default or supplied data file."""

        self._catalog_path = (
            catalog_path if catalog_path is not None
            else DEFAULT_CATALOG_PATH
        )

        self._catalog = self._load_catalog()

        # Index services by ID for efficient individual service retrieval.
        self._services_by_id = {
            service.service_id: service
            for service in self._catalog.services
        }

    def _load_catalog(self) -> ServiceCatalog:
        """Load the JSON knowledge base and validate its complete structure."""

        try:
            raw_data = self._catalog_path.read_bytes()
        except OSError as exc:
            raise CatalogLoadError(
                "Unable to read the government service catalog."
            ) from exc

        try:
            return ServiceCatalog.model_validate_json(raw_data)
        except ValidationError as exc:
            raise CatalogLoadError(
                "The government service catalog contains invalid data."
            ) from exc

    def list_service_groups(self) -> list[ServiceGroup]:
        """Return all available government service groups."""

        # Return copies to protect the internal validated catalog.
        return [
            group.model_copy(deep=True)
            for group in self._catalog.service_groups
        ]

    def list_services(
        self,
        group_id: str | None = None,
    ) -> list[GovernmentService]:
        """Return all services or filter them by their full group identifier."""

        services = self._catalog.services

        if group_id is not None:
            services = [
                service
                for service in services
                if service.group_id == group_id
            ]

        return [
            service.model_copy(deep=True)
            for service in services
        ]

    def get_service(
        self,
        service_id: str,
    ) -> GovernmentService | None:
        """Retrieve a service by ID or return None when it does not exist."""

        service = self._services_by_id.get(service_id)

        if service is None:
            return None

        return service.model_copy(deep=True)

    def get_service_group(
        self,
        group_id: str,
    ) -> ServiceGroup | None:
        """Retrieve a service group using its full identifier."""

        for group in self._catalog.service_groups:
            if group.group_id == group_id:
                return group.model_copy(deep=True)

        return None
