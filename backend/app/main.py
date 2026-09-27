from app.core.config import FRONTEND_URL

print("STARTUP 1: main.py loading", flush=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("STARTUP 2: FastAPI imported", flush=True)

from app.api.router import api_router

print("STARTUP 3: api_router imported", flush=True)


app = FastAPI(
    title="SellX API",
    version="1.0.0",
)

print("STARTUP 4: FastAPI app created", flush=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)