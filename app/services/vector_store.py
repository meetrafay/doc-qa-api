import faiss
import os
import json
import numpy as np

class FAISSService:
    def __init__(self, index_path="vectorstore/index.faiss", metadata_path="vectorstore/metadata.json", dim=384):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dim = dim
        self.index = self._load_index()
        self.metadata = self._load_metadata()

    def _load_index(self):
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        return faiss.IndexFlatL2(self.dim)

    def _load_metadata(self):
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r") as f:
                return json.load(f)
        return []

    def add_embeddings(self, embeddings: list[list[float]], metadatas: list[dict]):
        ids = list(range(len(self.metadata), len(self.metadata) + len(embeddings)))
        self.index.add(np.array(embeddings).astype("float32"))
        for i, meta in zip(ids, metadatas):
            meta["vector_id"] = i
            self.metadata.append(meta)
        self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f)


    def search(self, query_embedding: list[float], top_k: int = 3):
        import numpy as np
        query_vector = np.array([query_embedding]).astype("float32")
        
        if self.index.ntotal == 0:
            return []  # no vectors stored yet

        top_k = min(top_k, self.index.ntotal)  # avoid asking for more than available
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results


    def list_documents(self) -> list[dict]:
        # Get all unique doc_id-title pairs
        seen = {}
        for meta in self.metadata:
            if meta["doc_id"] not in seen:
                seen[meta["doc_id"]] = meta["title"]
        return [{"doc_id": k, "title": v} for k, v in seen.items()]


    def delete_document(self, doc_id: str):
        # Filter out chunks belonging to this document
        kept_meta = [m for m in self.metadata if m["doc_id"] != doc_id]
        delete_indices = [i for i, m in enumerate(self.metadata) if m["doc_id"] == doc_id]

        if not delete_indices:
            return False

        # Rebuild FAISS index with only kept vectors
        import numpy as np
        new_index = faiss.IndexFlatL2(self.dim)
        vectors = self.index.reconstruct_n(0, self.index.ntotal)
        new_vectors = np.delete(vectors, delete_indices, axis=0)
        new_index.add(new_vectors.astype("float32"))

        # Save updated index and metadata
        self.index = new_index
        self.metadata = kept_meta
        self._save()
        return True
