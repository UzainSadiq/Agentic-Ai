import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EduAgent | Student Success AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
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

    st.info(
        "💡 Learn smarter, plan better and "
        "track your academic progress."
    )


# =========================================================
# HERO
# =========================================================

st.title("🎓 Welcome to EduAgent")

st.subheader(
    "Your AI-powered Student Success Assistant"
)

st.write(
    """
EduAgent helps students plan their studies, understand
their academic progress, find useful learning resources
and interact with an intelligent AI study assistant.
"""
)

st.divider()


# =========================================================
# STATUS
# =========================================================

st.success(
    "🤖 EduAgent is ready to help you!"
)


# =========================================================
# FEATURES
# =========================================================

st.subheader("✨ What can EduAgent do?")

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("### 🎯 Smart Study Planning")

    st.write(
        """
Create personalized study plans based on your
subject, topic, difficulty and available study time.
"""
    )

    st.info(
        "Plan your learning efficiently."
    )


with col2:

    st.markdown("### 📊 Progress Tracking")

    st.write(
        """
Monitor your subject mastery, study hours,
completed tasks and academic improvement.
"""
    )

    st.success(
        "Track your academic growth."
    )


with col3:

    st.markdown("### 🤖 Autonomous AI")

    st.write(
        """
Ask questions and let EduAgent decide which
tools, notes and resources can help you.
"""
    )

    st.warning(
        "Your intelligent study companion."
    )


# =========================================================
# QUICK START
# =========================================================

st.divider()

st.subheader("🚀 Quick Start")

col1, col2 = st.columns(2)

with col1:

    st.page_link(
        "pages/eduagent.py",
        label="🤖 Chat with EduAgent",
        icon="🤖"
    )

    st.page_link(
        "pages/study_planner.py",
        label="🎯 Create Study Plan",
        icon="🎯"
    )


with col2:

    st.page_link(
        "pages/dashboard.py",
        label="📊 Open Dashboard",
        icon="📊"
    )

    st.page_link(
        "pages/resources.py",
        label="📚 Find Learning Resources",
        icon="📚"
    )


st.divider()

st.caption(
    "EduAgent • AI Student Success & Study Planning System"
)