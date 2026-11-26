# MAGA AI Backend

FastAPI foundation for the MAGA AI government digitalisation project.

## Setup

From the `backend` directory, install the pinned dependencies into the existing
virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Start the API

From the `backend` directory:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive Swagger
documentation is at <http://127.0.0.1:8000/docs>, and the OpenAPI schema is at
<http://127.0.0.1:8000/openapi.json>.

## Run tests

From the `backend` directory:

```powershell
.\.venv\Scripts\python.exe -m pytest
```
