import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
CHROMA_DIR = BASE_DIR / 'chroma_db'
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
CHAT_MODEL = os.getenv('CHAT_MODEL', 'nvidia/nemotron-3.5-lightning:free')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'edu_agent_knowledge')
TOP_K = int(os.getenv('TOP_K', '4'))
if not OPENROUTER_API_KEY:
    raise RuntimeError('OPENROUTER_API_KEY is missing. Create a .env file from .env.example and add your OpenRouter API key.')
