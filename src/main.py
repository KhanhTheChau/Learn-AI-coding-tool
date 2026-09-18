import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import job_router

os.makedirs("output/static/videos", exist_ok=True)

app = FastAPI(
    title="AI Chemistry Video Service",
    description="Backend service for generating chemistry videos using AI.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="output/static"), name="static")

app.include_router(job_router.router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
