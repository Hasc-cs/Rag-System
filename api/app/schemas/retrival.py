from pydantic import BaseModel, Field


class Source(BaseModel):
    """A document chunk that a handbook search result came from."""

    source: str = Field(default="unknown", description="File name or path of the source document")
    page: int | None = Field(default=None, description="Page number in the source, if available")
    score: float = Field(description="Similarity score returned by the vector store")
