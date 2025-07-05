from fastapi import APIRouter
from fastapi import HTTPException
from app.models.document import DocumentList
from app.services.embeding import EmbeddingService
from app.services.vector_store import FAISSService
from app.utils.chunker import chunk_text

router = APIRouter()
embedding_service = EmbeddingService()
vector_store = FAISSService()

@router.post("/documents")
def upload_documents(doc_list: DocumentList):
    for doc in doc_list.documents:
        if not doc.content.strip():
            raise HTTPException(status_code=400, detail=f"Document {doc.id} has empty content.")
        
        if any(d["doc_id"] == doc.id for d in vector_store.list_documents()):
            raise HTTPException(status_code=409, detail=f"Document with ID '{doc.id}' already exists.")

        chunks = chunk_text(doc.content)

        if len(chunks) > 100:
            raise HTTPException(status_code=413, detail=f"Document '{doc.title}' too large. Try splitting into parts.")

        embeddings = embedding_service.embed(chunks)
        metadatas = [
            {"doc_id": doc.id, "title": doc.title, "chunk": chunk, "chunk_id": i}
            for i, chunk in enumerate(chunks)
        ]
        vector_store.add_embeddings(embeddings, metadatas)

    return {"message": "Documents indexed successfully"}



@router.get("/documents")
def list_documents():
    return vector_store.list_documents()


@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    success = vector_store.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": f"Document {doc_id} deleted successfully"}

