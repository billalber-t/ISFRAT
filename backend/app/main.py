from fastapi import FastAPI
from app.api import endpoints
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="ISFRAT API",
    description="REST API for ISFRAT framework",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)
