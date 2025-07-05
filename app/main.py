from fastapi import FastAPI

app = FastAPI(title="Document QA API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Welcome to the Document QA API"}
