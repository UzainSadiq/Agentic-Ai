from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
DB_DIR = BASE_DIR / "chroma_db"

def build_index():
    documents = []
    for path in KNOWLEDGE_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        documents.append({"text": text, "source": path.name})

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    texts, metadatas = [], []
    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        texts.extend(chunks)
        metadatas.extend([{"source": doc["source"]}] * len(chunks))

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(
        collection_name="edulearn_notes",
        embedding_function=embeddings,
        persist_directory=str(DB_DIR),
    )
    vectorstore.add_texts(texts=texts, metadatas=metadatas)
    print(f"Indexed {len(texts)} chunks into {DB_DIR}")

if __name__ == "__main__":
    build_index()
