from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_document(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.create_documents([text])
