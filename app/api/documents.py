from fastapi import APIRouter, HTTPException
from app.models.document import DocumentList
from app.services.vector_store import VectorStoreService

router = APIRouter()
vector_store = VectorStoreService()

@router.post("/documents")
def upload_documents(doc_list: DocumentList):
    for doc in doc_list.documents:
        if not doc.content.strip():
            raise HTTPException(status_code=400, detail=f"Document {doc.id} has empty content.")
        
        existing_docs = vector_store.list_documents()
        if any(d.get("doc_id") == doc.id for d in existing_docs):
            raise HTTPException(status_code=409, detail=f"Document with ID '{doc.id}' already exists.")

        # LangChain handles chunking + embedding internally
        try:
            vector_store.add_document(doc_id=doc.id, title=doc.title, content=doc.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to index document: {str(e)}")
    
    return {"message": "Documents indexed successfully"}

@router.get("/documents")
def list_documents():
    return vector_store.list_documents()

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    success = vector_store.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": f"Document '{doc_id}' deleted successfully"}
