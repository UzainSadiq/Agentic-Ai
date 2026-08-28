from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "chroma_db"

def _store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(
        collection_name="edulearn_notes",
        embedding_function=embeddings,
        persist_directory=str(DB_DIR),
    )

@tool
def search_notes(query: str, k: int = 4) -> str:
    """Search the student's private course notes using RAG."""
    if not DB_DIR.exists():
        return "Knowledge base not indexed. Run: python rag/ingest.py"
    try:
        docs = _store().similarity_search(query, k=k)
        if not docs:
            return "No relevant notes found."
        parts = []
        for d in docs:
            parts.append(f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}")
        return "\n\n".join(parts)
    except Exception as e:
        return f"RAG search failed: {e}"
