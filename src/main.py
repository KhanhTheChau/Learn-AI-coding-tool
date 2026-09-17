from fastapi import FastAPI

app = FastAPI(
    title="AI Chemistry Video Service",
    description="Backend service for generating chemistry videos using AI.",
    version="1.0.0"
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
