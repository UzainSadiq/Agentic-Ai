from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import CHROMA_DIR, DATA_DIR, COLLECTION_NAME, EMBEDDING_MODEL

_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={'device':'cpu'}, encode_kwargs={'normalize_embeddings': True})

def _load_documents() -> List[Document]:
    documents=[]
    for path in sorted(DATA_DIR.iterdir()):
        if path.suffix.lower() in {'.txt','.md'}:
            text=path.read_text(encoding='utf-8')
            if text.strip(): documents.append(Document(page_content=text, metadata={'source':path.name}))
    if not documents: raise RuntimeError('No .txt or .md files were found in data/.')
    return RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150).split_documents(documents)

def get_vectorstore():
    return Chroma(collection_name=COLLECTION_NAME, embedding_function=_embeddings, persist_directory=str(CHROMA_DIR))

def build_index(force_rebuild=False):
    if force_rebuild and CHROMA_DIR.exists():
        import shutil; shutil.rmtree(CHROMA_DIR); CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore=get_vectorstore()
    existing=vectorstore.get(limit=1)
    if not (existing and existing.get('ids')):
        vectorstore.add_documents(_load_documents())
    return vectorstore

def retrieve(query, k=4):
    return build_index().similarity_search_with_score(query, k=k)
