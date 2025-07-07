from pydantic import BaseModel, Field
from typing import List

class Document(BaseModel):
    # id: str
    title: str = Field(..., max_length=200)
    content: str = Field(..., min_length=10, max_length=5000)

# class DocumentList(BaseModel):
#     documents: List[Document]
