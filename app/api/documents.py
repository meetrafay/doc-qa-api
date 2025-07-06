import uuid
from fastapi import APIRouter, HTTPException
from app.models.document import Document
from app.services.vector_store import VectorStoreService
from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.doc_parser import parse_document_input
from fastapi import UploadFile, File, HTTPException, APIRouter
from typing import List

router = APIRouter()
vector_store = VectorStoreService()

@router.post("/documents")
def upload_documents(doc_list: Document):
    # for doc in doc_list.documents:
    doc = doc_list
    if not doc.content.strip():
        raise HTTPException(status_code=400, detail=f"Document {doc.id} has empty content.")
    
    doc_id = str(uuid.uuid4())
    if any(d["doc_id"] == doc_id for d in vector_store.list_documents()):
        raise HTTPException(status_code=409, detail=f"Document with ID '{doc.id}' already exists.")

    # LangChain handles chunking + embedding internally
    try:
        vector_store.add_document(doc_id=doc_id, title=doc.title, content=doc.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index document: {str(e)}")

    return {"message": "Documents indexed successfully"}


@router.post("/documents/pdf-batch")
def upload_multiple_pdfs(files: List[UploadFile] = File(...)):
    uploaded_docs = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a valid PDF file.")

        try:
            text = extract_text_from_pdf(file)
            if not text.strip():
                continue  # Skip empty documents

            doc = parse_document_input(title=file.filename.replace(".pdf", ""), content=text)
            vector_store.add_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                content=doc["content"]
            )

            uploaded_docs.append({"doc_id": doc["doc_id"], "title": doc["title"]})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process '{file.filename}': {str(e)}")

    if not uploaded_docs:
        raise HTTPException(status_code=400, detail="No valid PDFs were uploaded.")

    # vector_store.print_all_documents()
    return {
        "message": f"{len(uploaded_docs)} document(s) indexed successfully.",
        "documents": uploaded_docs
    }



@router.get("/documents")
def list_documents():
    return vector_store.list_documents()

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    success = vector_store.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": f"Document '{doc_id}' deleted successfully"}
