
"""Automated tests for the government service catalog REST API.

These tests verify HTTP responses, service retrieval, department
filtering, request validation, and controlled error handling.
"""

from collections.abc import Iterator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_service_repository
from app.main import app
from app.repositories.service_repository import CatalogLoadError


# Keep the API version prefix consistent across all test requests.
API_PREFIX = "/api/v1"


@pytest.fixture(name="client")
def make_client() -> Iterator[TestClient]:
    """Provide an isolated HTTP test client for each test."""

    with TestClient(app) as test_client:
        yield test_client


def test_list_service_groups(client: TestClient) -> None:
    """Verify that all government service groups are returned."""

    response = client.get(f"{API_PREFIX}/service-groups")

    assert response.status_code == 200

    groups = response.json()

    assert len(groups) == 3
    assert {group["group_id"] for group in groups} == {
        "Department of Motor Traffic",
        "Department of Immigration and Emigration",
        "Divisional Secretariat and Grama Niladhari",
    }


def test_list_all_services(client: TestClient) -> None:
    """Verify that all initial government service records are returned."""

    response = client.get(f"{API_PREFIX}/services")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    services = response.json()

    assert len(services) == 7
    assert {service["service_id"] for service in services} == {
        f"SVC-{number:03d}" for number in range(1, 8)
    }


@pytest.mark.parametrize(
    "group_id,expected_count",
    [
        ("Department of Motor Traffic", 2),
        ("Department of Immigration and Emigration", 3),
        ("Divisional Secretariat and Grama Niladhari", 2),
    ],
)
def test_filter_services_by_group(
    client: TestClient,
    group_id: str,
    expected_count: int,
) -> None:
    """Verify that filtering returns only the requested group's services."""

    response = client.get(
        f"{API_PREFIX}/services",
        params={"group_id": group_id},
    )

    assert response.status_code == 200

    services = response.json()

    assert len(services) == expected_count
    assert all(
        service["group_id"] == group_id
        for service in services
    )


def test_get_service_by_id(client: TestClient) -> None:
    """Verify that a specific service can be retrieved by its ID."""

    response = client.get(f"{API_PREFIX}/services/SVC-001")

    assert response.status_code == 200

    service = response.json()

    assert service["service_id"] == "SVC-001"
    assert service["name"] == "Driving Licence Renewal"
    assert service["group_id"] == "Department of Motor Traffic"


def test_unknown_service_returns_404(
    client: TestClient,
) -> None:
    """Return a controlled error for a nonexistent service."""

    response = client.get(f"{API_PREFIX}/services/SVC-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Government service not found."
    }


def test_unknown_group_returns_404(
    client: TestClient,
) -> None:
    """Return a controlled error for an unknown service group."""

    response = client.get(
        f"{API_PREFIX}/services",
        params={"group_id": "Unknown Department"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Government service group not found."
    }


def test_empty_group_id_returns_422(
    client: TestClient,
) -> None:
    """Reject an explicitly empty service group query parameter."""

    response = client.get(
        f"{API_PREFIX}/services",
        params={"group_id": ""},
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert any(
        error["loc"] == ["query", "group_id"]
        and error["type"] == "string_too_short"
        for error in errors
    )


def test_catalog_unavailable_returns_503(
    client: TestClient,
) -> None:
    """Return a safe HTTP response when the catalog cannot be loaded."""

    # Clear cached data so the simulated failure reaches the provider.
    get_service_repository.cache_clear()

    try:
        with patch(
            "app.api.dependencies.ServiceRepository",
            side_effect=CatalogLoadError(
                "Simulated catalog loading failure"
            ),
        ) as mocked_repository:
            response = client.get(f"{API_PREFIX}/services")

            mocked_repository.assert_called_once()

        assert response.status_code == 503
        assert response.json() == {
            "detail": (
                "Government service information is "
                "temporarily unavailable."
            )
        }

    finally:
        # Prevent the simulated failure from affecting other tests.
        get_service_repository.cache_clear()
def test_pending_verification_status_is_preserved(
    client: TestClient,
) -> None:
    """Expose pending verification status without claiming validity."""

    response = client.get(f"{API_PREFIX}/services/SVC-001")

    assert response.status_code == 200

    service = response.json()

    assert service["verification_status"] == "pending"
    assert service["sources"] == []


def test_unknown_requirements_are_returned_as_null(
    client: TestClient,
) -> None:
    """Preserve unknown government information in API responses."""

    response = client.get(f"{API_PREFIX}/services/SVC-001")

    assert response.status_code == 200

    service = response.json()

    assert service["required_documents"] is None
    assert service["eligibility"] is None
    assert service["procedure"] is None
    assert service["fees"] is None
