import logging

import uvicorn
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.v1.routes import routers as v1_routers
from core.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Coordinator Helper API",
)
app.include_router(v1_routers, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


logger = logging.getLogger(__name__)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
