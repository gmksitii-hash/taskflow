from fastapi import FastAPI
from app.tasks.api import router as tasks_router

app = FastAPI(title="TaskFlow API", version="0.1.0")
app.include_router(tasks_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
