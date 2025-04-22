from fastapi import FastAPI
from routes.api import router as api_router

app = FastAPI(title="Frontend BFF API")

app.include_router(api_router)


@app.get("/health-check")
def health_check():
    return {"status": "ok"}
