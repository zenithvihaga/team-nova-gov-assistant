from fastapi import FastAPI

app = FastAPI(title="MAGA AI Backend", version="0.1.0")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to MAGA AI Backend"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
