import streamlit as st
from graph import run_problem
from config import PROVIDER, MODEL_NAME, require_openrouter_key

st.set_page_config(
    page_title="Multi-Agent AI Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 48%, #f8fafc 100%);
    }
    [data-testid="stHeader"] { background: rgba(255,255,255,0.72); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    .hero {
        padding: 28px 32px;
        border-radius: 24px;
        background: linear-gradient(135deg, #111827, #312e81 55%, #4f46e5);
        color: white;
        box-shadow: 0 18px 50px rgba(49,46,129,.20);
        margin-bottom: 24px;
    }
    .hero h1 { margin: 0 0 8px 0; font-size: 2.2rem; }
    .hero p { margin: 0; color: #e0e7ff; font-size: 1.03rem; }
    .pill {
        display: inline-block;
        padding: 5px 11px;
        border-radius: 999px;
        background: rgba(255,255,255,.14);
        border: 1px solid rgba(255,255,255,.18);
        margin-right: 7px;
        margin-top: 14px;
        font-size: .82rem;
    }
    .agent-card {
        padding: 16px 18px;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        background: rgba(255,255,255,.86);
        min-height: 118px;
        box-shadow: 0 8px 25px rgba(15,23,42,.05);
    }
    .agent-icon { font-size: 1.65rem; }
    .agent-title { font-weight: 750; margin-top: 5px; color: #111827; }
    .agent-desc { color: #64748b; font-size: .88rem; line-height: 1.45; }
    .result-card {
        padding: 24px 28px;
        border-radius: 20px;
        background: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 12px 35px rgba(15,23,42,.07);
    }
    .mini-stat {
        padding: 12px 15px;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .mini-stat strong { display:block; font-size: 1.1rem; color:#111827; }
    .mini-stat span { color:#64748b; font-size:.76rem; }
    .footer-note { color:#64748b; font-size:.82rem; text-align:center; margin-top:24px; }
    div.stButton > button[kind="primary"] {
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
        box-shadow: 0 8px 20px rgba(79,70,229,.20);
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Session state ----------
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🤖 Multi-Agent AI Studio")
    st.caption("LangGraph-powered problem solving")
    st.divider()

    st.markdown("### 🔐 AI Configuration")
    st.success("OpenRouter connected")
    st.write(f"**Provider:** {PROVIDER.title()}")
    st.write("**Model:** OpenRouter Free Router")
    st.caption("Only one secret is required: OPENROUTER_API_KEY")

    st.divider()
    st.markdown("### 🧩 Agent Team")
    st.markdown("🔎 **Agent A — Research**  \nFinds facts and useful external context.")
    st.markdown("📊 **Agent B — Analysis**  \nCompares options, risks, and trade-offs.")
    st.markdown("🛠️ **Agent C — Execution**  \nTurns analysis into practical steps.")
    st.markdown("🧠 **Supervisor**  \nCombines everything into the final answer.")

    st.divider()
    st.markdown("### 💡 Good Demo Problems")
    demos = [
        "Compare AWS, Azure and Google Cloud for deploying an AI application.",
        "Create a low-cost deployment plan for a university AI chatbot.",
        "Design an implementation plan for a Streamlit AI application.",
    ]
    for demo in demos:
        if st.button(demo, key=f"demo_{demo}", use_container_width=True):
            st.session_state.problem = demo

    if st.button("🗑️ Clear session", use_container_width=True):
        st.session_state.last_result = None
        st.session_state.history = []
        st.session_state.problem = ""
        st.rerun()

# ---------- Header ----------
st.markdown(
    """
<div class="hero">
    <h1>🧠 Multi-Agent Problem Solving System</h1>
    <p>Give the AI team a complex problem. Four specialized agents collaborate to research, analyze, execute, and deliver a polished solution.</p>
    <span class="pill">⚡ LangGraph</span>
    <span class="pill">🔎 Research</span>
    <span class="pill">📊 Analysis</span>
    <span class="pill">🛠️ Execution</span>
    <span class="pill">🧠 Supervisor</span>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Agent overview ----------
cols = st.columns(4)
agent_cards = [
    ("🔎", "Research", "Collects useful facts and external context."),
    ("📊", "Analysis", "Breaks the problem down and compares choices."),
    ("🛠️", "Execution", "Builds practical steps and recommendations."),
    ("🧠", "Supervisor", "Synthesizes all agent outputs into one answer."),
]
for col, (icon, title, desc) in zip(cols, agent_cards):
    with col:
        st.markdown(
            f'<div class="agent-card"><div class="agent-icon">{icon}</div>'
            f'<div class="agent-title">{title}</div><div class="agent-desc">{desc}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Input ----------
problem = st.text_area(
    "🎯 What problem should the agent team solve?",
    value=st.session_state.get("problem", ""),
    height=170,
    placeholder="Example: Compare AWS, Azure and Google Cloud for deploying an AI application and recommend the best option for a university project.",
    key="problem_input",
)

c1, c2 = st.columns([4, 1])
with c1:
    solve = st.button("🚀  Solve with Agent Team", type="primary", use_container_width=True)
with c2:
    st.markdown('<div class="mini-stat"><strong>1 key</strong><span>OpenRouter only</span></div>', unsafe_allow_html=True)

# ---------- Run workflow ----------
if solve:
    if not problem.strip():
        st.warning("Please enter a problem first.")
        st.stop()

    try:
        require_openrouter_key()
    except Exception as e:
        st.error(str(e))
        st.info("Create a .env file beside app.py and add your OpenRouter key. Never paste the key into Python code.")
        st.stop()

    progress = st.progress(0, text="Starting the multi-agent workflow...")
    try:
        progress.progress(15, text="🔎 Agent A is researching...")
        result = run_problem(problem.strip())
        progress.progress(100, text="✅ All agents completed.")
        st.session_state.last_result = result
        st.session_state.history.insert(0, problem.strip())
        st.session_state.history = st.session_state.history[:5]
    except Exception as e:
        progress.empty()
        st.error(f"Application error: {e}")
        st.stop()

# ---------- Results ----------
result = st.session_state.last_result
if result:
    st.markdown("## ✨ Final Answer")
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(result.get("final_answer", "No final answer was returned."))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🔬 Agent Workspace")
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔎 Research",
        "📊 Analysis",
        "🛠️ Execution",
        "🧠 Supervisor Log",
    ])
    with tab1:
        st.markdown(result.get("research", "No research output."))
    with tab2:
        st.markdown(result.get("analysis", "No analysis output."))
    with tab3:
        st.markdown(result.get("execution", "No execution output."))
    with tab4:
        for item in result.get("supervisor_log", []):
            st.write("•", item)

    st.markdown("### 📌 Workflow Summary")
    a, b, c, d = st.columns(4)
    for col, value, label in [
        (a, "01", "Research"),
        (b, "02", "Analysis"),
        (c, "03", "Execution"),
        (d, "04", "Supervisor"),
    ]:
        with col:
            st.markdown(f'<div class="mini-stat"><strong>{value}</strong><span>{label}</span></div>', unsafe_allow_html=True)
else:
    st.info("👆 Enter a complex problem above and click **Solve with Agent Team** to start.")

st.markdown('<div class="footer-note">Built with Streamlit + LangGraph + OpenRouter • No Groq or OpenAI key required</div>', unsafe_allow_html=True)
