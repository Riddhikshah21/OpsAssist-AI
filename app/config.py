from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OpsAssist AI"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "opsassist_docs"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ollama_model: str = "llama3.1"
    ollama_base_url: str = "http://localhost:11434"

    class Config:
        env_file = ".env"


settings = Settings()