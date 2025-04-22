from fastapi import FastAPI
from routes.api import router as api_router

app = FastAPI(title="Backend Web Interface API")

app.include_router(api_router)


@app.get("/health-check")
def health_check():
    return {"status": "ok"}
