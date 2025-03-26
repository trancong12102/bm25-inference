from contextlib import asynccontextmanager
from typing import AsyncGenerator, TypedDict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastembed import SparseTextEmbedding

from bm25_inference import bm25


class AppState(TypedDict):
    """Application state."""

    model: SparseTextEmbedding


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[AppState, None]:
    model = SparseTextEmbedding(model_name="Qdrant/bm25")

    yield {"model": model}


def create_app() -> FastAPI:
    app = FastAPI(
        title="BM25 Inference API",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/api-docs",
    )

    # middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # routers
    app.include_router(bm25.router)

    return app
