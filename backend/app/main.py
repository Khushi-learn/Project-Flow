
from fastapi import FastAPI

app = FastAPI(
    title="ProjectFlow API",
    description="Project and task management system",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ProjectFlow API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
