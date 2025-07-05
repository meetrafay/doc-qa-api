from fastapi import APIRouter
from app.models.query import QueryRequest
from app.services.vector_store import VectorStoreService
from app.services.llm import AnswerService

router = APIRouter()

vector_store = VectorStoreService()
answer_service = AnswerService()

@router.post("/query")
def query_docs(payload: QueryRequest):
    # Use LangChain's internal embedding + search
    top_chunks = vector_store.search(payload.question, k=payload.top_k)
    
    if not top_chunks:
        return {
            "question": payload.question,
            "answer": "Sorry, I couldn't find relevant information in the documents.",
            "sources": []
        }

    combined_context = "\n".join([chunk["chunk"] for chunk in top_chunks])

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
