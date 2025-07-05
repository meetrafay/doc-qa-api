from fastapi import FastAPI
from app.api import documents, query

app = FastAPI(title="Free Document QA API", version="1.0")

app.include_router(documents.router, prefix="")
app.include_router(query.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FREE Document QA API"}
