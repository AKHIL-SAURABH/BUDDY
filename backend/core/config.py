import os
from pydantic_settings import BaseSettings
from groq import AsyncGroq

class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = "Catalyst AI Assessment"
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Database Configs
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend/db/catalyst_state.db")
    
    # Vector Store Configs
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "./backend/services/vector_store/index.faiss")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    # FastAPI Configs
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: str = os.getenv("PORT", "8000")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore" # Ignore extra fields in .env

# Instantiate the settings so other files can just import `settings`
settings = Settings()

# Configure the Groq SDK globally with the API key
groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)