from fastapi import FastAPI
from routes.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Backend Web Interface API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou use ["http://localhost:5173"] se quiser limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/health-check")
def health_check():
    return {"status": "ok"}
