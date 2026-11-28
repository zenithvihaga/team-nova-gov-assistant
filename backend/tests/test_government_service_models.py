
"""Automated validation tests for government service data models.

These tests protect the integrity of the knowledge base and prevent
invalid service records from entering the application.
"""

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from app.models.government_service import (
    GovernmentService,
    ServiceCatalog,
)


# Resolve the catalog path independently of the working directory.
CATALOG_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "service_catalog.json"
)


def load_catalog_data() -> dict[str, Any]:
    """Load a fresh copy of the catalog for each validation test."""

    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def test_valid_service_catalog() -> None:
    """Verify that the initial government service catalog is valid."""

    catalog = ServiceCatalog.model_validate(load_catalog_data())

    assert len(catalog.service_groups) == 3
    assert len(catalog.services) == 7


def test_valid_service_record() -> None:
    """Verify that a valid government service record is accepted."""

    data = load_catalog_data()["services"][0]
    service = GovernmentService.model_validate(data)

    assert service.service_id == "SVC-001"
    assert service.name == "Driving Licence Renewal"
    assert service.group_id == "Department of Motor Traffic"


@pytest.mark.parametrize(
    "field,value",
    [
        ("service_id", "INVALID-ID"),
        ("name", "   "),
        ("verification_status", "invalid"),
    ],
)
def test_invalid_service_fields(
    field: str,
    value: str,
) -> None:
    """Reject service records containing invalid field values."""

    data = load_catalog_data()["services"][0]
    data[field] = value

    with pytest.raises(ValidationError):
        GovernmentService.model_validate(data)


def test_duplicate_service_ids() -> None:
    """Reject catalogs containing duplicate service identifiers."""

    data = load_catalog_data()

    data["services"].append(data["services"][0].copy())

    with pytest.raises(ValidationError):
        ServiceCatalog.model_validate(data)


def test_duplicate_service_groups() -> None:
    """Reject catalogs containing duplicate service group identifiers."""

    data = load_catalog_data()

    data["service_groups"].append(
        data["service_groups"][0].copy()
    )

    with pytest.raises(ValidationError):
        ServiceCatalog.model_validate(data)


def test_unknown_service_group_reference() -> None:
    """Reject services referencing a nonexistent government group."""

    data = load_catalog_data()

    data["services"][0]["group_id"] = "Unknown Department"

    with pytest.raises(ValidationError):
        ServiceCatalog.model_validate(data)
def test_verified_service_requires_sources() -> None:
    """Reject verified records without supporting sources."""

    data = load_catalog_data()["services"][0]
    data["verification_status"] = "verified"
    data["sources"] = []

    with pytest.raises(
        ValidationError,
        match="Verified service records must include supporting sources",
    ):
        GovernmentService.model_validate(data)


def test_verified_service_with_sources() -> None:
    """Accept a verified record containing supporting sources."""

    data = load_catalog_data()["services"][0]
    data["verification_status"] = "verified"

    # Use a synthetic source for structural validation only.
    data["sources"] = ["https://example.com/test-source"]

    service = GovernmentService.model_validate(data)

    assert service.verification_status == "verified"
    assert service.sources == ["https://example.com/test-source"]


def test_unknown_requirements_remain_none() -> None:
    """Preserve unknown information without inventing requirements."""

    service = GovernmentService(
        service_id="SVC-999",
        group_id="Test Department",
        name="Synthetic Test Service",
    )

    assert service.required_documents is None
    assert service.eligibility is None
    assert service.procedure is None
    assert service.fees is None
    assert service.verification_status == "pending"
    assert service.sources == []
