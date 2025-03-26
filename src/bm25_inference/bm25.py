from fastapi import APIRouter, Request

from bm25_inference.model import (
    CreateSparseEmbeddingInput,
    CreateSparseEmbeddingResponse,
    SparseEmbedding,
)

from fastembed import SparseEmbedding as FastEmbedSparseEmbedding

router = APIRouter(prefix="/bm25", tags=["bm25"])


@router.post("/", operation_id="create_bm25_embeddings")
async def create_bm25_embeddings(
    input: CreateSparseEmbeddingInput,
    request: Request,
) -> CreateSparseEmbeddingResponse:
    model = request.state.model

    embeddings: list[FastEmbedSparseEmbedding] = list(model.embed(input.documents))

    return CreateSparseEmbeddingResponse(
        embeddings=[
            SparseEmbedding.model_validate(embedding) for embedding in embeddings
        ]
    )
