import streamlit as st

from tools.resource_tools import (
    search_learning_resources
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Learning Resources",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 EduAgent")

    st.caption(
        "Learning Resources"
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


# =========================================================
# HEADER
# =========================================================

st.title("📚 Learning Resources")

st.write(
    """
Find tutorials, documentation, articles and videos
for the topics you are currently studying.
"""
)

st.divider()


# =========================================================
# SEARCH
# =========================================================

st.subheader("🔎 Search Resources")

query = st.text_input(
    "What do you want to learn?",
    placeholder=(
        "Example: LangGraph tool calling tutorial"
    )
)


resource_type = st.selectbox(
    "📂 Resource Type",
    [
        "All",
        "Tutorials",
        "Documentation",
        "Videos",
        "Articles"
    ]
)


search_button = st.button(
    "🔎 Search",
    type="primary",
    use_container_width=True
)


# =========================================================
# SEARCH RESULTS
# =========================================================

if search_button:

    if not query:

        st.warning(
            "Please enter a topic to search."
        )

    else:

        with st.spinner(
            "🔎 Searching for learning resources..."
        ):

            try:

                result = search_learning_resources(
                    query
                )

                st.divider()

                st.subheader(
                    "🔎 Search Results"
                )

                st.write(result)

            except Exception as e:

                st.error(
                    "Unable to search resources."
                )

                st.exception(e)


# =========================================================
# POPULAR TOPICS
# =========================================================

st.divider()

st.subheader("🔥 Popular Learning Topics")


topics = [
    "LangGraph",
    "Artificial Intelligence",
    "Operating Systems",
    "Database Systems",
    "Python",
    "Machine Learning"
]


cols = st.columns(3)


for index, topic in enumerate(topics):

    with cols[index % 3]:

        if st.button(
            f"📚 {topic}",
            use_container_width=True
        ):

            st.session_state.resource_query = topic

            st.rerun()


# =========================================================
# HANDLE POPULAR TOPIC
# =========================================================

if "resource_query" in st.session_state:

    selected_topic = (
        st.session_state.resource_query
    )

    st.info(
        f"Selected topic: **{selected_topic}**"
    )