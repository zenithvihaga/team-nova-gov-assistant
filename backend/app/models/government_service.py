
"""Data models for the government service knowledge base.

These models validate individual service records, government service
groups, and relationships within the complete service catalog.
"""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator


# Reject empty text values and remove unnecessary surrounding whitespace.
NonEmptyText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

# Restrict verification status to supported values.
VerificationStatus = Literal["pending", "verified"]


class ServiceGroup(BaseModel):
    """Represent a government institution or service category."""

    model_config = ConfigDict(extra="forbid", strict=True)

    group_id: NonEmptyText
    name: NonEmptyText


class GovernmentService(BaseModel):
    """Represent an individual government service and its information."""

    model_config = ConfigDict(extra="forbid", strict=True)

    service_id: str = Field(pattern=r"^SVC-[0-9]{3,}$")
    group_id: NonEmptyText
    name: NonEmptyText
    description: NonEmptyText | None = None

    # Unknown requirements must remain None until reliable data is available.
    # An empty list must not be used to represent unknown requirements.
    required_documents: list[NonEmptyText] | None = None
    eligibility: list[NonEmptyText] | None = None
    procedure: list[NonEmptyText] | None = None
    fees: NonEmptyText | None = None

    sources: list[NonEmptyText] = Field(default_factory=list)
    verification_status: VerificationStatus = "pending"

    @model_validator(mode="after")
    def validate_verification_sources(self) -> Self:
        """Require supporting sources for records marked as verified."""

        if self.verification_status == "verified" and not self.sources:
            raise ValueError(
                "Verified service records must include supporting sources."
            )

        return self


class ServiceCatalog(BaseModel):
    """Represent and validate the complete government service catalog."""

    model_config = ConfigDict(extra="forbid", strict=True)

    schema_version: Literal["1.0.0"]
    service_groups: list[ServiceGroup]
    services: list[GovernmentService]

    @model_validator(mode="after")
    def validate_catalog_relationships(self) -> Self:
        """Prevent duplicate identifiers and invalid group references."""

        group_ids = [group.group_id for group in self.service_groups]
        service_ids = [service.service_id for service in self.services]

        # Every service group must have a unique identifier.
        if len(group_ids) != len(set(group_ids)):
            raise ValueError("Duplicate service group IDs are not allowed.")

        # Every government service must have a unique identifier.
        if len(service_ids) != len(set(service_ids)):
            raise ValueError("Duplicate service IDs are not allowed.")

        valid_group_ids = set(group_ids)

        # Each service must reference an existing government service group.
        for service in self.services:
            if service.group_id not in valid_group_ids:
                raise ValueError(
                    f"Service '{service.service_id}' references "
                    f"an unknown group: '{service.group_id}'."
                )

        return self
