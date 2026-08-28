from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    content = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        return _extract_pdf(content)
    if name.endswith(".docx"):
        return _extract_docx(content)
    if name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")


def _extract_pdf(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages).strip()


def _extract_docx(content: bytes) -> str:
    document = Document(BytesIO(content))
    return "\n".join(
        p.text for p in document.paragraphs if p.text.strip()
    ).strip()
