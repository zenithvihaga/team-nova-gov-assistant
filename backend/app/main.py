
"""Main entry point for the government assistant backend application."""

from fastapi import FastAPI

from app.api.service_catalog import router as service_catalog_router


app = FastAPI(
    title="MAGA AI Backend",
    version="0.1.0",
    description="REST API for the government service assistant application.",
)


# Register the versioned government service catalog endpoints.
app.include_router(service_catalog_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return the backend application welcome message."""

    return {"message": "Welcome to MAGA AI Backend"}


@app.get("/health")
def read_health() -> dict[str, str]:
    """Report whether the backend application is responding."""

    return {"status": "ok"}
