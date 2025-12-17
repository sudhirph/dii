from fastapi import FastAPI
from ingest import router as ingest_router

app = FastAPI(title="DII API")


@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(ingest_router)