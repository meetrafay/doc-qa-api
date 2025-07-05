import os
from dotenv import load_dotenv

# Load .env file on startup
load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "vectorstore/index.faiss")
    METADATA_STORE: str = os.getenv("METADATA_STORE", "vectorstore/metadata.json")

settings = Settings()
