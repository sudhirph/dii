from fastapi import FastAPI
from .ingest import router as ingest_router
from .beliefs import router as beliefs_router

app = FastAPI(title="DII API")


@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(ingest_router)
app.include_router(beliefs_router)