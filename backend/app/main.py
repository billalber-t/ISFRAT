from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="ISFRAT API",
    description="REST API for ISFRAT framework",
    version="1.0.0"
)

app.include_router(endpoints.router)
