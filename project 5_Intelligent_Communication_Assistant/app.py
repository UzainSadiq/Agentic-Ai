import streamlit as st
from dotenv import load_dotenv

from agent.communication_agent import CommunicationAgent
from ui.styles import load_css

load_dotenv()
load_css()

st.set_page_config(
    page_title="CommAgent AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<div class="hero">
  <div class="kicker">AGENTIC AI • PROJECT 5</div>
  <h1>Intelligent Communication Assistant</h1>
  <p>Analyze a request, decide the appropriate communication tool, execute it, and record the result.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ System")
    st.caption("Gemini + Tool Calling")
    st.markdown("---")
    st.markdown("**Available tools**")
    st.caption("Send Email • Push Notification • Action Log")
    st.markdown("**Delivery mode**")
    st.caption("Demo mode by default; optional SendGrid/Pushover delivery.")

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown("### 01 · Communication request")

    request = st.text_area(
        "Describe what should happen",
        placeholder=(
            "Example: Send an email to ali@example.com telling them that "
            "the project submission is due tomorrow."
        ),
        height=145,
        label_visibility="collapsed",
    )

    recipient = st.text_input(
        "Recipient email (optional)",
        placeholder="ali@example.com",
    )

    priority = st.selectbox(
        "Priority",
        ["Normal", "High", "Urgent"],
        index=0,
    )

    examples = {
        "Email": "Send an email to student@example.com reminding them that the project is due tomorrow.",
        "Notification": "Send me a high-priority notification that the project deadline is tomorrow.",
        "Both": "Send an email to student@example.com and a notification because the project deadline is tomorrow.",
    }

    e1, e2, e3 = st.columns(3)
    if e1.button("Email example", use_container_width=True):
        st.session_state["request"] = examples["Email"]
        st.rerun()
    if e2.button("Notification example", use_container_width=True):
        st.session_state["request"] = examples["Notification"]
        st.rerun()
    if e3.button("Both example", use_container_width=True):
        st.session_state["request"] = examples["Both"]
        st.rerun()

    if "request" in st.session_state and not request:
        request = st.session_state["request"]

    if st.button("Analyze & Execute", type="primary", use_container_width=True):
        if not request.strip():
            st.warning("Enter a communication request first.")
        else:
            try:
                with st.status("Agent is analyzing the request…", expanded=True) as status:
                    st.write("Analyzing intent and communication conditions")
                    agent = CommunicationAgent()
                    result = agent.run(
                        request=request,
                        recipient=recipient.strip(),
                        priority=priority,
                    )
                    st.write("Executing selected communication tool")
                    st.write("Recording confirmation and action log")
                    status.update(label="Agent workflow complete", state="complete")

                st.session_state["result"] = result
            except Exception as exc:
                st.error(f"Agent error: {exc}")

with right:
    st.markdown("### 02 · Agent decision")

    if "result" not in st.session_state:
        st.markdown(
            """
            <div class="empty-card">
              <div class="empty-icon">◎</div>
              <b>Waiting for a request</b>
              <p>The agent's decision, tool calls, and delivery status will appear here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        result = st.session_state["result"]

        st.markdown(
            f"""
            <div class="decision-card">
              <div class="label">AGENT DECISION</div>
              <h2>{result["decision"].replace("_", " ").title()}</h2>
              <p>{result["reason"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Tool execution")
        for item in result["actions"]:
            state_class = "success" if item["success"] else "warning"
            icon = "✓" if item["success"] else "!"
            st.markdown(
                f"""
                <div class="action {state_class}">
                  <span class="action-icon">{icon}</span>
                  <div><b>{item["tool"].replace("_", " ").title()}</b>
                  <small>{item["message"]}</small></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### Confirmation")
        st.info(result["confirmation"])

        with st.expander("View action log"):
            for line in result["logs"]:
                st.code(line, language="text")

st.markdown(
    '<div class="pipeline">REQUEST <span>→</span> GEMINI AGENT <span>→</span> TOOL CALL <span>→</span> CONFIRMATION / LOG</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="footer">CommAgent AI · Intelligent Communication Assistant</div>', unsafe_allow_html=True)
