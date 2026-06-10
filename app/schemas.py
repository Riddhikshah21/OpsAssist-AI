from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=3, ge=1, le=10)


class Source(BaseModel):
    document: str
    chunk_id: str | None = None
    score: float | None = None
    content_preview: str


class ChatResponse(BaseModel):
    answer: str
    confidence: str
    sources: list[Source]
    recommended_actions: list[str] = []
    escalation: str | None = None