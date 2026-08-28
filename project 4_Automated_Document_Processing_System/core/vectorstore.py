from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = Path("data/chroma_db")


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vectorstore(documents):
    DB_PATH.mkdir(parents=True, exist_ok=True)

    return Chroma.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        persist_directory=str(DB_PATH),
        collection_name="document_collection",
    )


def retrieve_documents(vectorstore, query: str, k: int = 5):
    return vectorstore.similarity_search(query, k=k)
