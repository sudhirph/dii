from fastapi import FastAPI

app = FastAPI(title="DII API")


@app.get("/health")
def health():
    return {"status": "ok"}

