from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(title="Recommender API with LLM")
app.include_router(api_router)
