import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


from typing import List, Dict

VECTOR_DB_PATH = "app/vector_store/index"

class VectorStoreService:
    def __init__(self):
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding = HuggingFaceEmbeddings(model_name=model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

        if os.path.exists(VECTOR_DB_PATH):
            # self.db = FAISS.load_local(VECTOR_DB_PATH, self.embedding)

            self.db = FAISS.load_local(
                VECTOR_DB_PATH,
                self.embedding,
                allow_dangerous_deserialization=True
            )
        else:
            self.db = None

    
    def print_all_documents(self):
        if not self.db:
            print("No documents in the vector store.")
            return

        print("\n📄 Stored Documents in FAISS:\n")
        for doc_id, doc in self.db.docstore._dict.items():
            metadata = doc.metadata
            title = metadata.get("title", "Untitled")
            chunk_id = metadata.get("chunk_id", "N/A")
            print(f"→ [{title}] (chunk {chunk_id}):\n{doc.page_content[:300]}...\n")

    
    def add_document(self, doc_id: str, title: str, content: str):
        # Step 1: Split content into chunks
        chunks_raw = self.text_splitter.split_text(content)

        # Step 2: Convert to Document objects with metadata
        from langchain.schema import Document
        chunks = [
            Document(
                page_content=chunk,
                metadata={"doc_id": doc_id, "title": title, "chunk_id": idx}
            )
            for idx, chunk in enumerate(chunks_raw)
        ]

        # Step 3: Add to vectorstore
        if self.db:
            self.db.add_documents(chunks)
        else:
            self.db = FAISS.from_documents(chunks, self.embedding)

        self.db.save_local(VECTOR_DB_PATH)


    def search(self, query: str, k: int = 3) -> List[Dict]:
        
        if not self.db:
            return []

        docs = self.db.similarity_search(query, k=k)

        results = []
        for doc in docs:
            metadata = doc.metadata
            results.append({
                "doc_id": metadata.get("doc_id"),
                "title": metadata.get("title"),
                "chunk": doc.page_content,
            })
        return results

    def list_documents(self) -> List[Dict]:
        if not self.db:
            return []
        return list({doc.metadata["doc_id"]: doc.metadata for doc in self.db.docstore._dict.values()}.values())

    def delete_document(self, doc_id: str) -> bool:
        if not self.db or not self.db.docstore:
            return False

        # Filter only documents that don't match the doc_id
        all_docs = list(self.db.docstore._dict.values())
        remaining_docs = [
            doc for doc in all_docs if doc.metadata.get("doc_id") != doc_id
        ]

        if len(remaining_docs) == len(all_docs):
            return False  # nothing matched

        # Reset FAISS and delete old files
        import shutil
        if os.path.exists(VECTOR_DB_PATH):
            shutil.rmtree(VECTOR_DB_PATH)

        if not remaining_docs:
            self.db = None
            return True

        # Rebuild and save
        self.db = FAISS.from_documents(remaining_docs, self.embedding)
        self.db.save_local(VECTOR_DB_PATH)
        return True

