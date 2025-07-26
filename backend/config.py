import os
from dotenv import load_dotenv

HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")

load_dotenv()

class Config:
    # HuggingFace Configuration
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", HUGGINGFACE_TOKEN)
    MODEL_NAME = "google/flan-t5-base"  # More reliable base model
    
    # Vector Database Configuration
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # CORS Configuration
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # File Upload Configuration
    UPLOAD_DIR = "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {".pdf"}
    
    # LLM Configuration
    TEMPERATURE = 0.7
    MAX_TOKENS = 512  # Good for T5 model
    MAX_LENGTH = 512
    
    # Vector Database Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200 