import streamlit as st

from agent import run_agent


# =========================================================
# PAGE CONFIGURATION
# =========================================================

page_title="Intelligent Task Execution Agent",
page_icon="🤖",
layout="centered",


# =========================================================
# TITLE
# =========================================================

st.title("🤖 Intelligent Task Execution Agent")

st.write(
    "An Agentic AI system using LangChain, ReAct-style "
    "reasoning, tool calling, and Streamlit."
)


# =========================================================
# TOOL INFORMATION
# =========================================================

with st.sidebar:

    st.header("🛠️ Available Tools")

    st.write("🧮 Calculator")
    st.write("🌦️ Weather")
    st.write("🌐 Web Search")

    st.divider()

    st.write("Powered by:")
    st.write("• LangChain")
    st.write("• Groq")
    st.write("• Streamlit")


# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "Give me a task..."
)


# =========================================================
# PROCESS USER INPUT
# =========================================================

if user_input:

    # Display user message

    with st.chat_message("user"):

        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    # Run agent

    with st.chat_message("assistant"):

        with st.spinner("🤔 Agent is analyzing the task..."):

            try:

                response = run_agent(user_input)

                st.markdown(response)

            except Exception as e:

                response = (
                    "❌ An error occurred:\n\n"
                    f"`{str(e)}`"
                )

                st.error(response)


    # Save assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )