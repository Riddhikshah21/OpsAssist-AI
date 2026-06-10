from fastapi import FastAPI

from app.config import settings
from app.rag_pipeline import answer_question
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "qdrant_url": settings.qdrant_url,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return answer_question(
        question=request.question,
        top_k=request.top_k,
    )