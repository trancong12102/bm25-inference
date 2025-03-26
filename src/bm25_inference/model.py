from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    """Base class for API schemas."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class SparseEmbedding(BaseModel):
    """Sparse embedding."""

    """Indices of the non-zero values in the embedding."""
    indices: list[int]

    """Values of the non-zero values in the embedding."""
    values: list[float]


class CreateSparseEmbeddingInput(BaseModel):
    """Input for creating a sparse embedding."""

    """Documents to embed."""
    documents: list[str]


class CreateSparseEmbeddingResponse(BaseModel):
    """Response for creating a sparse embedding."""

    """Sparse embeddings."""
    embeddings: list[SparseEmbedding]
