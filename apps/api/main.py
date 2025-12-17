from fastapi import FastAPI
from .ingest import router as ingest_router
from .beliefs import router as beliefs_router
from .portfolio import router as portfolio_router
from .alerts import router as alerts_router
from apps.changes import router as changes_router

app = FastAPI(title="DII API")


@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(ingest_router)
app.include_router(beliefs_router)
app.include_router(portfolio_router)
app.include_router(alerts_router)
app.include_router(changes_router)