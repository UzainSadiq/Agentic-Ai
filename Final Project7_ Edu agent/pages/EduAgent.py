import streamlit as st

from agent import run_agent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EduAgent AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 EduAgent")

    st.caption(
        "AI Student Success Assistant"
    )

    st.divider()

    st.page_link(
        "app.py",
        label="🏠 Home"
    )

    st.page_link(
        "pages/eduagent.py",
        label="🤖 AI Assistant"
    )

    st.page_link(
        "pages/dashboard.py",
        label="📊 Dashboard"
    )

    st.page_link(
        "pages/progress.py",
        label="📈 Progress"
    )

    st.page_link(
        "pages/resources.py",
        label="📚 Resources"
    )

    st.page_link(
        "pages/study_planner.py",
        label="🎯 Study Planner"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.title("🤖 EduAgent AI Assistant")

st.write(
    """
Ask EduAgent anything about your studies. It can create
study plans, analyze your progress, search your notes,
find resources and help you make academic decisions.
"""
)

st.divider()


# =========================================================
# AI STATUS
# =========================================================

st.success(
    "🟢 EduAgent is online and ready."
)


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.subheader("💡 Try asking")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🎯 Create a study plan for my AI exam",
        use_container_width=True
    ):
        st.session_state.prompt = (
            "Create a study plan for my AI exam."
        )


with col2:

    if st.button(
        "📊 Analyze my academic progress",
        use_container_width=True
    ):
        st.session_state.prompt = (
            "Analyze my academic progress."
        )


col3, col4 = st.columns(2)

with col3:

    if st.button(
        "📚 Explain A* using my course notes",
        use_container_width=True
    ):
        st.session_state.prompt = (
            "Explain A* using my course notes."
        )


with col4:

    if st.button(
        "🌐 Find resources to learn LangGraph",
        use_container_width=True
    ):
        st.session_state.prompt = (
            "Find resources to learn LangGraph."
        )


# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Ask EduAgent anything about your studies..."
)


# =========================================================
# BUTTON PROMPT
# =========================================================

if (
    "prompt" in st.session_state
    and not prompt
):

    prompt = st.session_state.pop(
        "prompt"
    )


# =========================================================
# PROCESS MESSAGE
# =========================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 EduAgent is thinking..."
        ):

            try:

                response = run_agent(
                    prompt
                )

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:

                st.error(
                    "EduAgent could not complete "
                    "the request."
                )

                st.exception(e)