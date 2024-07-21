from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.router import router as core_router

app = FastAPI(
    title="Deepchecks Module",
    description="",
    version="0.0.1",
    contact={
        "name": "support",
        "email": "anon@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)
app.include_router(core_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
