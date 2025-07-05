from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3  # default: return top 3 relevant chunks
