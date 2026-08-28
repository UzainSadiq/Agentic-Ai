import streamlit as st
from dotenv import load_dotenv

from agents.document_agent import DocumentAgent
from core.chunker import split_document
from core.document_loader import extract_text
from core.vectorstore import create_vectorstore, retrieve_documents
from ui.styles import load_css

load_dotenv()

st.set_page_config(
    page_title="DocuFlow AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()

st.markdown("""
<div class="hero">
    <div class="hero-kicker">AGENTIC AI • PROJECT 4</div>
    <h1>Automated Document Processing System</h1>
    <p>Extract relevant information, retrieve supporting context, validate the result, and produce structured output.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ System")
    st.caption("Groq + ChromaDB + Pydantic")
    st.markdown("---")
    st.markdown("**Supported files**")
    st.caption("PDF • DOCX • TXT")
    st.markdown("**Pipeline**")
    st.caption("Upload → Extract → Chunk → RAG → Groq → Validate → Output")

st.markdown("### 01 · Upload document")
uploaded_file = st.file_uploader(
    "Drop a document here",
    type=["pdf", "docx", "txt"],
    label_visibility="collapsed",
)

if uploaded_file:
    st.markdown(
        f'<div class="file-chip">📄 <b>{uploaded_file.name}</b><span>{uploaded_file.size / 1024:.1f} KB</span></div>',
        unsafe_allow_html=True,
    )

    if st.button("Process Document", type="primary", use_container_width=True):
        try:
            with st.status("Running document agent…", expanded=True) as status:
                st.write("Extracting document text")
                text = extract_text(uploaded_file)
                if not text.strip():
                    raise ValueError("No readable text was found in the uploaded document.")

                st.write("Splitting document into semantic chunks")
                documents = split_document(text)

                st.write("Indexing chunks in ChromaDB with local embeddings")
                vectorstore = create_vectorstore(documents)

                st.write("Retrieving relevant document context")
                retrieved_docs = retrieve_documents(
                    vectorstore,
                    "document title type summary key information entities dates",
                    k=min(5, len(documents)),
                )
                context = "\n\n".join(d.page_content for d in retrieved_docs)

                st.write("Running Groq extraction agent")
                agent = DocumentAgent()
                result = agent.process(context)

                status.update(label="Processing complete", state="complete")

            st.session_state["result"] = result
            st.session_state["file_name"] = uploaded_file.name
            st.rerun()

        except Exception as exc:
            st.error(f"Processing failed: {exc}")

if "result" in st.session_state:
    output = st.session_state["result"]

    st.markdown("### 02 · Agent validation")

    if output["status"] == "valid":
        st.markdown(
            '<div class="status valid"><span>✓</span><div><b>VALID</b><small>Pydantic validation passed successfully.</small></div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status invalid"><span>!</span><div><b>INVALID</b><small>Validation failed after the re-processing attempt.</small></div></div>',
            unsafe_allow_html=True,
        )
        st.error(output["error"])

    if output["result"]:
        result = output["result"]

        st.markdown("### 03 · Structured output")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="metric-card"><span>DOCUMENT TYPE</span><strong>{}</strong></div>'.format(result.document_type.title()), unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><span>CONFIDENCE</span><strong>{:.0f}%</strong></div>'.format(result.confidence * 100), unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card"><span>AGENT ATTEMPTS</span><strong>{}</strong></div>'.format(output["attempts"]), unsafe_allow_html=True)

        left, right = st.columns([1.05, 1])

        with left:
            st.markdown('<div class="result-card"><div class="label">DOCUMENT TITLE</div><h2>{}</h2></div>'.format(result.document_title), unsafe_allow_html=True)
            st.markdown('<div class="result-card"><div class="label">SUMMARY</div><p>{}</p></div>'.format(result.summary), unsafe_allow_html=True)

            st.markdown("#### Key information")
            for item in result.key_information:
                st.markdown(f'<div class="list-item">• {item}</div>', unsafe_allow_html=True)

        with right:
            st.markdown("#### Entities")
            if result.entities:
                for entity in result.entities:
                    st.markdown(
                        f'<div class="entity"><b>{entity.name}</b><span>{entity.type}</span></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No entities detected.")

            st.markdown("#### Dates")
            if result.dates:
                for date in result.dates:
                    st.markdown(f'<div class="date-item">◷ {date}</div>', unsafe_allow_html=True)
            else:
                st.caption("No dates detected.")

        with st.expander("View raw structured JSON"):
            st.json(result.model_dump())

st.markdown('<div class="footer">DocuFlow AI · Automated Document Processing · Groq + ChromaDB + Pydantic</div>', unsafe_allow_html=True)
