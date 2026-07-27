"""
Centralized configuration — one place for every setting, so nothing gets
edited in three files and forgotten in a fourth.
"""
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

DATA_FILE_PATH = os.path.join("data", "policies.txt")
VECTOR_STORE_PATH = os.path.join("faiss_index")

LLM_MODEL_NAME = "openai/gpt-oss-120b"
EMBEDDING_MODEL_NAME = "jina-embeddings-v2-base-en"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
RETRIEVAL_TOP_K = 3

SYSTEM_PROMPT = (
    "You are a friendly inventory & sales assistant. Always use the "
    "search_policy tool to look up facts before answering."
)


def check_api_keys():
    """Fail fast with a clear message if a required key is missing —
    there's no point loading data or building an index if we can't
    call the LLM or embeddings API at the end of the pipeline anyway."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file — "
            "get one free at console.groq.com"
        )
    if not JINA_API_KEY:
        raise ValueError(
            "JINA_API_KEY is missing. Add it to your .env file — "
            "get one free at jina.ai"
        )
