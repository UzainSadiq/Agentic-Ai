import os
import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="TeleAgent • Agentic AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background: radial-gradient(circle at 15% 5%, rgba(99,102,241,.18), transparent 28%),
                         radial-gradient(circle at 90% 10%, rgba(14,165,233,.14), transparent 25%),
                         #070b14; color: #f8fafc; }
.block-container { max-width: 1250px; padding-top: 2rem; }
.hero {
    padding: 28px 32px; border-radius: 24px;
    background: linear-gradient(135deg, rgba(30,41,59,.92), rgba(15,23,42,.76));
    border: 1px solid rgba(148,163,184,.16);
    box-shadow: 0 20px 70px rgba(0,0,0,.25);
}
.badge { display:inline-block; padding:6px 12px; border-radius:999px;
         background:rgba(34,197,94,.12); color:#86efac; font-size:12px;
         font-weight:700; letter-spacing:.04em; }
.hero h1 { font-size: 42px; margin: 12px 0 8px; }
.hero p { color:#cbd5e1; font-size:16px; max-width:820px; line-height:1.7; }
.card {
    padding: 18px 20px; border-radius: 18px;
    background: rgba(15,23,42,.72); border:1px solid rgba(148,163,184,.13);
}
.card h3 { margin: 0 0 8px; }
.muted { color:#94a3b8; font-size:13px; }
.flow {
    display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:10px;
}
.node {
    padding:9px 12px; border-radius:12px; background:#111827;
    border:1px solid rgba(99,102,241,.35); font-size:12px; font-weight:600;
}
.arrow { color:#64748b; }
.small { font-size:12px; color:#94a3b8; }
div[data-testid="stSidebar"] { background: #0a0f1c; border-right:1px solid rgba(148,163,184,.12); }
.stButton > button { border-radius:12px; border:1px solid rgba(148,163,184,.16); }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🤖 TeleAgent")
    st.caption("Telegram Agentic AI Assistant")
    st.divider()
    st.markdown("### System status")
    st.success("OpenRouter connected" if os.environ.get("OPENROUTER_API_KEY") else "Waiting for API key")
    st.markdown("### Included tools")
    for item in ["🧠 Knowledge Base / RAG", "🧮 Calculator", "🕒 Time Tool", "🧭 Agent Router", "✅ Result Validator"]:
        st.write(item)
    st.divider()
    st.markdown("**Demo tip**")
    st.caption("Try: “Explain LangGraph”, “calculate (25*8)/5”, or “what time is it?”")

st.markdown("""
<div class="hero">
  <span class="badge">PROJECT 6 • TELEGRAM + LANGGRAPH</span>
  <h1>TeleAgent — Agentic AI Assistant</h1>
  <p>
    A production-style Telegram chatbot prototype that receives a user request,
    analyzes intent, chooses the right tool or knowledge source, validates the result,
    and generates a clean final response.
  </p>
</div>
""", unsafe_allow_html=True)

st.write("")
c1, c2, c3, c4 = st.columns(4)
for col, value, label in [
    (c1, "1", "OpenRouter API"),
    (c2, "3", "Agent Tools"),
    (c3, "5", "LangGraph Nodes"),
    (c4, "∞", "Telegram Queries"),
]:
    with col:
        st.markdown(f'<div class="card"><div style="font-size:28px;font-weight:800">{value}</div><div class="muted">{label}</div></div>', unsafe_allow_html=True)

st.write("")
tab_chat, tab_flow, tab_about = st.tabs(["💬 Agent Playground", "🧩 Agent Workflow", "📘 Project Summary"])

with tab_chat:
    st.markdown("### Test the agent before connecting Telegram")
    prompt = st.chat_input("Ask the agent something…")
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Agent is reasoning and selecting an action…"):
                try:
                    result = run_agent(prompt)
                    st.markdown(result["answer"])
                    with st.expander("🔍 Agent trace"):
                        st.write(f"**Action:** {result['action']}")
                        st.write(f"**Tool:** {result.get('tool', 'none')}")
                        st.write(f"**Validation:** {result.get('validation', 'completed')}")
                        if result.get("evidence"):
                            st.write("**Evidence:**")
                            st.write(result["evidence"])
                    st.session_state.history.append({"role": "assistant", "content": result["answer"]})
                except Exception as exc:
                    st.error(f"Agent error: {exc}")

with tab_flow:
    st.markdown("### Design pattern required by the assignment")
    st.markdown("""
    <div class="card">
      <div class="flow">
        <span class="node">👤 User</span><span class="arrow">→</span>
        <span class="node">📨 Telegram Bot</span><span class="arrow">→</span>
        <span class="node">🧠 LangGraph</span><span class="arrow">→</span>
        <span class="node">🔎 Analyze</span><span class="arrow">→</span>
        <span class="node">🛠️ Tool / RAG</span><span class="arrow">→</span>
        <span class="node">✅ Validate</span><span class="arrow">→</span>
        <span class="node">✨ Final Reply</span><span class="arrow">→</span>
        <span class="node">📨 Telegram</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Agent nodes")
        for title, desc in [
            ("1. Analyze", "Classifies the request and selects direct answer, RAG, calculator, or time tool."),
            ("2. Execute", "Runs the selected local tool or retrieves relevant knowledge."),
            ("3. Validate", "Checks that the tool/RAG step returned usable evidence."),
            ("4. Generate", "Uses OpenRouter to create the final user-friendly answer."),
            ("5. Return", "Sends the final response back to the Telegram interface."),
        ]:
            st.markdown(f'<div class="card" style="margin-bottom:10px"><b>{title}</b><div class="muted">{desc}</div></div>', unsafe_allow_html=True)
    with right:
        st.markdown("#### Available tools")
        st.markdown("""
        - **Knowledge Search:** lightweight local RAG over `data/knowledge_base.md`
        - **Calculator:** safe arithmetic evaluator
        - **Time Tool:** returns the server's current date/time
        - **OpenRouter LLM:** reasoning + final response generation
        """)
        st.info("No separate search, database, or paid AI API is required for the included demo.")

with tab_about:
    st.markdown("### 🎓 What this project demonstrates")
    st.markdown("""
    **TeleAgent** is an Agentic AI system built around the assignment's Project 6 requirements.
    A Telegram user sends a normal-language request. The agent does not blindly answer:
    it first analyzes the request, decides whether a tool or knowledge source is needed,
    executes that action, validates the result, and then generates the final response.

    **Why it is agentic:** the workflow contains decision-making, tool use, state transitions,
    validation, and response generation instead of a single prompt → response call.

    **API design:** the project uses **one AI credential: `OPENROUTER_API_KEY`**.
    The default model is `openrouter/free`, which lets OpenRouter select from its currently
    available free models.
    """)
    st.markdown("### 🚀 Telegram setup")
    st.code("""
1. Create a Telegram bot with @BotFather and copy its bot token.
2. Copy .env.example → .env
3. Add OPENROUTER_API_KEY=your_openrouter_key
4. Add TELEGRAM_BOT_TOKEN=your_telegram_bot_token
5. Install requirements:
   pip install -r requirements.txt
6. Start the bot:
   python telegram_bot.py
7. Optional: run the visual demo:
   streamlit run app.py
""", language="text")
    st.markdown("### Suggested instructor demo")
    st.markdown("""
    1. Open the Streamlit dashboard and show the workflow.
    2. Ask **“Explain LangGraph in simple words.”** → Knowledge/RAG.
    3. Ask **“Calculate (125 * 8) / 5.”** → Calculator.
    4. Ask **“What time is it?”** → Time tool.
    5. Open Telegram and send the same questions to prove the agent is not limited to the dashboard.
    """)
