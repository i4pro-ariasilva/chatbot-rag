import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Document Processing
    DOCUMENTS_DIR = os.getenv("DOCUMENTS_DIR", r"C:\Users\ariasilva\Documents\COPILOT\Semana_03\chatbot_rag\db_intern")
    
    # Groq API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Deprecated HF Configuration (keeping for backwards compatibility)
    API_PROVIDER = os.getenv("API_PROVIDER", "groq")
    HF_API_URL = os.getenv("HF_API_URL", "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium")
    HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
    
    # Vector Database (SQLite local)
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db/documents.db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "company_docs")
    
    # Server Configuration
    HOST = os.getenv("HOST", "localhost")
    PORT = int(os.getenv("PORT", 8000))
    
    # Processing Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 2000))
    
    # Supported file extensions
    SUPPORTED_HTML_EXTENSIONS = ['.html', '.htm']
    SUPPORTED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg']
    SUPPORTED_TEXT_EXTENSIONS = ['.txt', '.md']

config = Config()