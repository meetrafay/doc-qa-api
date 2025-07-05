from fastapi import APIRouter
from app.models.query import QueryRequest
from app.services.embeding import EmbeddingService
from app.services.vector_store import FAISSService
from app.services.llm import AnswerService

router = APIRouter()

embedding_service = EmbeddingService()
vector_store = FAISSService()
answer_service = AnswerService()

@router.post("/query")
def query_docs(payload: QueryRequest):
    query_vec = embedding_service.embed([payload.question])[0]
    top_chunks = vector_store.search(query_vec, top_k=payload.top_k)

    if not top_chunks:
        return {
            "question": payload.question,
            "answer": "Sorry, I couldn't find relevant information in the documents.",
            "sources": []
        }

    combined_context = "\n".join([c["chunk"] for c in top_chunks])
    
    if not combined_context.strip():
        return {
            "question": payload.question,
            "answer": "The context retrieved was empty or irrelevant.",
            "sources": top_chunks
        }

    answer = answer_service.generate_answer(payload.question, combined_context)

    return {
        "question": payload.question,
        "answer": answer,
        "sources": top_chunks
    }

