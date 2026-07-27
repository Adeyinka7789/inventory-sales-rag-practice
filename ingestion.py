"""
Ingestion, now with persistence. Building an embedding index costs real
time and real money on every run — this module only pays that cost once,
then loads the saved index from disk on every subsequent run.
"""
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import JinaEmbeddings
from langchain_community.vectorstores import FAISS
import config


def get_embeddings_model():
    return JinaEmbeddings(jina_api_key=config.JINA_API_KEY, model_name=config.EMBEDDING_MODEL_NAME)


def check_if_vector_store_exists() -> bool:
    return os.path.exists(os.path.join(config.VECTOR_STORE_PATH, "index.faiss"))


def build_vector_store():
    """Load, split, embed, and index from scratch — only called the
    first time, or if the saved index is missing/deleted."""
    loader = TextLoader(config.DATA_FILE_PATH, encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    vector_store = FAISS.from_documents(chunks, get_embeddings_model())
    save_vector_store(vector_store)
    return vector_store


def save_vector_store(vector_store):
    vector_store.save_local(config.VECTOR_STORE_PATH)


def load_vector_store():
    return FAISS.load_local(
        config.VECTOR_STORE_PATH, get_embeddings_model(),
        allow_dangerous_deserialization=True,
    )


def get_vector_store():
    """The one function everything else should call — handles the
    build-vs-load decision so callers never have to think about it."""
    if check_if_vector_store_exists():
        print("Found a saved vector store on disk — loading it (no re-embedding).")
        return load_vector_store()
    print("No saved vector store found — building one from scratch.")
    return build_vector_store()
