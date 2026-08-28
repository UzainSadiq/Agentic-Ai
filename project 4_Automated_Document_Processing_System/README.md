# Automated Document Processing System

Agentic AI Project 4 — a Streamlit application that processes PDF, DOCX and TXT documents, retrieves relevant context with ChromaDB, extracts structured information using Groq, and validates the result with Pydantic.

## Architecture

Streamlit UI
→ Document Agent
→ Text Extraction
→ Chunk / Process
→ ChromaDB + Local Embeddings
→ Retriever
→ Groq LLM Agent
→ Pydantic Validation
→ Valid Output / Re-process

## API key

Only one API key is required:

```env
GROQ_API_KEY=your_key
```

Embeddings are local using `sentence-transformers/all-MiniLM-L6-v2`.

## Setup

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and add your Groq API key.

### Run

```bash
streamlit run app.py
```

## Supported documents

- PDF
- DOCX
- TXT

## Project structure

```text
Automated_Document_Processing_System/
├── app.py
├── agents/
│   └── document_agent.py
├── core/
│   ├── document_loader.py
│   ├── chunker.py
│   ├── vectorstore.py
│   └── validator.py
├── schemas/
│   └── document_schema.py
├── ui/
│   └── styles.py
├── data/
│   └── chroma_db/
├── sample_documents/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Teacher demonstration

1. Upload a document.
2. Click **Process Document**.
3. Show the processing stages in the Streamlit status panel.
4. Explain ChromaDB retrieval.
5. Explain the Groq extraction agent.
6. Show the **VALID** Pydantic result.
7. Expand **View raw structured JSON**.
8. Explain that invalid results are sent through one controlled re-processing attempt.

## Notes

The first run may download the local embedding model. No OpenAI or OpenRouter API key is used.
