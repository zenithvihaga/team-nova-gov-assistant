
# TEAM NOVA — Government Service Assistant Backend

FastAPI backend for the TEAM NOVA government digitalisation project,
developed for the DevFest Sri Lanka 2026 AI Kasthiram competition.

> The final application name is pending confirmation.

## Current Development Status

- Backend version: 0.1.0
- Development stage: Prototype
- Knowledge base schema version: 1.0.0
- Government service groups: 3
- Government service records: 7
- Automated tests: 40 passing
- Government information verification: Pending

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14.6 | Backend programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Pydantic | Data validation and serialization |
| JSON | Initial government service knowledge base |
| pytest | Automated testing |
| HTTPX2 | HTTP test client support |
| Git and GitHub | Version control and collaboration |

## Backend Architecture

The backend follows a layered, API-first architecture with separation
of concerns, dependency injection, and the Repository Design Pattern.

```text
Client Application
        |
        v
REST API Layer
        |
        v
Dependency Injection
        |
        v
Repository Layer
        |
        v
Pydantic Data Models
        |
        v
JSON Knowledge Base
```

The repository loads and validates the knowledge base during
initialization. A cached dependency provider allows API endpoints
to reuse the repository.

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── service_catalog.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── government_service.py
│   └── repositories/
│       ├── __init__.py
│       └── service_repository.py
├── data/
│   └── service_catalog.json
├── tests/
│   ├── test_government_service_models.py
│   ├── test_service_repository.py
│   ├── test_service_catalog_api.py
│   └── test_health.py
├── requirements.txt
└── README.md
```

## Component Responsibilities

| Component | Responsibility |
|---|---|
| main.py | Application initialization and router registration |
| dependencies.py | Shared repository provider and error handling |
| service_catalog.py | Versioned government service REST endpoints |
| government_service.py | Data models and validation rules |
| service_repository.py | Validated catalog loading and retrieval |
| service_catalog.json | Government service knowledge base |
| requirements.txt | Pinned Python dependencies |
| tests/ | Automated validation and regression tests |

## Setup

Use Python 3.14.6 to match the current development environment.

From the repository root, navigate to the backend directory:

```powershell
cd backend
```

Create a virtual environment if one does not already exist:

```powershell
python -m venv .venv
```

Install the pinned dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Verify installed dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

## Start the API

From the backend directory:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Local development URLs:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application welcome message |
| GET | `/health` | Application liveness check |
| GET | `/api/v1/service-groups` | List government service groups |
| GET | `/api/v1/services` | List government services |
| GET | `/api/v1/services/{service_id}` | Retrieve a service by ID |

### Filter Services

The services endpoint supports an optional `group_id` query parameter.

The full service group identifier must be supplied.

Example:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/services?group_id=Department%20of%20Motor%20Traffic"
```

### Retrieve an Individual Service

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/services/SVC-001"
```

### HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 404 | Requested service or service group not found |
| 422 | Request validation failed |
| 503 | Government service catalog unavailable |

## Government Service Knowledge Base

The initial knowledge base contains the following service groups
and service records.

| ID | Service |
|---|---|
| SVC-001 | Driving Licence Renewal |
| SVC-002 | Duplicate Driving Licence |
| SVC-003 | Passport Application |
| SVC-004 | Passport Renewal |
| SVC-005 | Lost Passport Request Letter |
| SVC-006 | Residence Certificate Assistance |
| SVC-007 | General Certification Assistance |

Service groups:

- Department of Motor Traffic
- Department of Immigration and Emigration
- Divisional Secretariat and Grama Niladhari

The catalog is stored in `data/service_catalog.json`.

Restart the backend after updating the catalog to refresh cached data.

## Data Integrity and Responsible AI

The backend implements the following safeguards:

- Strict data type validation.
- Rejection of unexpected data fields.
- Duplicate service and group identifier prevention.
- Validation of service-to-group relationships.
- Defensive copying of repository data.
- Supporting source requirements for records marked as verified.
- Controlled API error responses.
- Preservation of unknown government information as JSON `null`.

Unknown document requirements, eligibility criteria, procedures,
and fees must not be invented.

All initial government service records remain pending verification.
The existence of a source reference alone does not establish its
authenticity or authority.

## Automated Testing

Run all tests from the backend directory:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Latest recorded full regression result:

| Test module | Passed tests |
|---|---:|
| Government service models | 11 |
| Service repository | 15 |
| Service catalog API | 12 |
| Health and root endpoints | 2 |
| Total | 40 |

Recorded on 2026-11-28: 40 passed in 0.86 seconds.

Tests cover data validation, repository retrieval, defensive copying,
API filtering, HTTP error handling, verification status, and
preservation of unknown information.

## Privacy and Security

- Do not commit API keys, credentials, or environment secrets.
- Do not commit virtual environments or generated cache files.
- Use synthetic data for automated testing.
- Do not store personal government documents in the knowledge base.
- Verify government information against authoritative sources before use.

## Current Limitations

- Official government information verification is pending.
- The knowledge base currently uses local JSON storage.
- Cached catalog data does not automatically refresh.
- The health endpoint confirms application liveness only.
- Fresh environment installation has not yet been independently verified.
- Gemini AI integration is not implemented at this stage.
- Frontend integration is pending.
- Production deployment and security hardening are pending.

This backend is a development prototype and must not be treated
as an official government information system.

## Planned Development

- Government service advisor.
- Document checklist and readiness assessment.
- Business rules and validation engine.
- AI integration interfaces.
- Secure document processing.
- Privacy and redaction controls.
- Frontend integration.
- Final testing and deployment preparation.

## Team

TEAM NOVA

DevFest Sri Lanka 2026 — AI Kasthiram

Track 1 — Government Digitalisation
