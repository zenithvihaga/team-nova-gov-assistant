
"""Automated tests for the government service repository.

These tests verify catalog loading, service retrieval, filtering,
data isolation, and controlled handling of catalog loading failures.
"""

from pathlib import Path

import pytest

from app.repositories.service_repository import (
    CatalogLoadError,
    ServiceRepository,
)


@pytest.fixture(name="repository")
def make_repository() -> ServiceRepository:
    """Provide a fresh repository instance for each test."""

    return ServiceRepository()


def test_repository_loads_catalog(
    repository: ServiceRepository,
) -> None:
    """Verify that the initial service catalog loads successfully."""

    assert len(repository.list_service_groups()) == 3
    assert len(repository.list_services()) == 7


def test_get_service_by_id(
    repository: ServiceRepository,
) -> None:
    """Retrieve the correct government service using its unique ID."""

    service = repository.get_service("SVC-001")

    assert service is not None
    assert service.service_id == "SVC-001"
    assert service.name == "Driving Licence Renewal"


def test_unknown_service_returns_none(
    repository: ServiceRepository,
) -> None:
    """Return None when the requested service does not exist."""

    assert repository.get_service("SVC-999") is None


@pytest.mark.parametrize(
    "group_id,expected_count",
    [
        ("Department of Motor Traffic", 2),
        ("Department of Immigration and Emigration", 3),
        ("Divisional Secretariat and Grama Niladhari", 2),
    ],
)
def test_filter_services_by_group(
    repository: ServiceRepository,
    group_id: str,
    expected_count: int,
) -> None:
    """Return only services belonging to the requested group."""

    services = repository.list_services(group_id=group_id)

    assert len(services) == expected_count
    assert all(service.group_id == group_id for service in services)


def test_get_service_group(
    repository: ServiceRepository,
) -> None:
    """Retrieve a government service group by its full identifier."""

    group = repository.get_service_group(
        "Department of Motor Traffic"
    )

    assert group is not None
    assert group.name == "Department of Motor Traffic"


def test_unknown_service_group(
    repository: ServiceRepository,
) -> None:
    """Return None when the requested service group does not exist."""

    assert repository.get_service_group("Unknown Department") is None


def test_repository_protects_internal_data(
    repository: ServiceRepository,
) -> None:
    """Prevent changes to returned records from affecting stored data."""

    service = repository.get_service("SVC-001")

    assert service is not None

    original_sources = service.sources.copy()

    # Modify the returned copy without changing the repository.
    service.sources.append("https://example.com/test")

    original_service = repository.get_service("SVC-001")

    assert original_service is not None
    assert original_service.sources == original_sources


def test_missing_catalog_file(tmp_path: Path) -> None:
    """Raise a controlled error when the catalog file is missing."""

    missing_file = tmp_path / "missing_catalog.json"

    with pytest.raises(CatalogLoadError):
        ServiceRepository(missing_file)


def test_invalid_catalog_json(tmp_path: Path) -> None:
    """Reject catalog files containing malformed JSON."""

    invalid_file = tmp_path / "invalid_catalog.json"

    invalid_file.write_text(
        "{invalid json}",
        encoding="utf-8",
    )

    with pytest.raises(CatalogLoadError):
        ServiceRepository(invalid_file)


def test_invalid_catalog_schema(tmp_path: Path) -> None:
    """Reject valid JSON that does not satisfy the catalog schema."""

    invalid_file = tmp_path / "invalid_schema.json"

    invalid_file.write_text(
        "{}",
        encoding="utf-8",
    )

    with pytest.raises(CatalogLoadError):
        ServiceRepository(invalid_file)
def test_service_list_protects_internal_data(
    repository: ServiceRepository,
) -> None:
    """Prevent changes to listed services from affecting stored data."""

    services = repository.list_services()
    original_name = services[0].name

    services[0].name = "Modified Test Service"
    services[0].sources.append("https://example.com/test")

    fresh_services = repository.list_services()

    assert fresh_services[0].name == original_name
    assert "https://example.com/test" not in fresh_services[0].sources


def test_group_list_protects_internal_data(
    repository: ServiceRepository,
) -> None:
    """Prevent changes to listed groups from affecting stored data."""

    groups = repository.list_service_groups()
    original_name = groups[0].name

    groups[0].name = "Modified Test Department"

    assert repository.list_service_groups()[0].name == original_name


def test_group_lookup_protects_internal_data(
    repository: ServiceRepository,
) -> None:
    """Protect stored group data from changes to returned records."""

    group_id = "Department of Motor Traffic"
    group = repository.get_service_group(group_id)

    assert group is not None

    original_name = group.name
    group.name = "Modified Test Department"

    fresh_group = repository.get_service_group(group_id)

    assert fresh_group is not None
    assert fresh_group.name == original_name
