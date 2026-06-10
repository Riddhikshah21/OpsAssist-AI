from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from app.config import settings
from app.retriever import retrieve_documents
from app.schemas import ChatResponse, Source


SYSTEM_PROMPT = """
You are OpsAssist AI, an engineering support assistant.

Use only the provided context to answer the user's question.
If the context is insufficient, say that you do not know based on the available documentation.
Do not invent system details.
Always provide a practical troubleshooting answer.
Keep the answer concise and operational.
"""


USER_PROMPT = """
Question:
{question}

Retrieved context:
{context}

Answer format:
- Likely cause:
- Evidence:
- Recommended checks:
- Escalation:
"""


def _format_context(retrieved_docs: list[dict]) -> str:
    context_blocks = []

    for index, item in enumerate(retrieved_docs, start=1):
        metadata = item["metadata"]
        document = metadata.get("document", "unknown")
        chunk_id = metadata.get("chunk_id", "unknown")

        context_blocks.append(
            f"[Source {index}]\n"
            f"Document: {document}\n"
            f"Chunk ID: {chunk_id}\n"
            f"Content:\n{item['content']}"
        )

    return "\n\n".join(context_blocks)


def _build_sources(retrieved_docs: list[dict]) -> list[Source]:
    sources = []

    for item in retrieved_docs:
        metadata = item["metadata"]

        sources.append(
            Source(
                document=metadata.get("document", "unknown"),
                chunk_id=metadata.get("chunk_id"),
                score=item.get("score"),
                content_preview=item["content"][:300],
            )
        )

    return sources


def _estimate_confidence(retrieved_docs: list[dict]) -> str:
    if len(retrieved_docs) >= 3:
        return "high"
    if len(retrieved_docs) >= 1:
        return "medium"
    return "low"


def answer_question(question: str, top_k: int = 3) -> ChatResponse:
    retrieved_docs = retrieve_documents(query=question, k=top_k)

    if not retrieved_docs:
        return ChatResponse(
            answer="I do not know based on the available documentation.",
            confidence="low",
            sources=[],
            recommended_actions=[],
            escalation="Escalate to the relevant engineering team.",
        )

    context = _format_context(retrieved_docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT),
        ]
    )

    llm = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    confidence = _estimate_confidence(retrieved_docs)

    return ChatResponse(
        answer=response.content,
        confidence=confidence,
        sources=_build_sources(retrieved_docs),
        recommended_actions=[],
        escalation=(
            "Review the cited sources and escalate if the issue affects production users."
            if confidence in {"medium", "high"}
            else "Escalate to the relevant engineering team."
        ),
    )