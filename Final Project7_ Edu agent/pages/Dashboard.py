import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EduAgent Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 EduAgent")

    st.caption(
        "Student Dashboard"
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

st.title("📊 Student Dashboard")

st.write(
    "Your academic command center."
)

st.divider()


# =========================================================
# METRICS
# =========================================================

st.subheader("📌 Academic Overview")

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "🎯 Overall Mastery",
        "69%",
        "+8%"
    )


with c2:

    st.metric(
        "⏱️ Study This Week",
        "14.5h",
        "+2.5h"
    )


with c3:

    st.metric(
        "📚 Subjects",
        "6",
        "2 need attention"
    )


with c4:

    st.metric(
        "🔥 Study Streak",
        "7 days",
        "Personal best"
    )


st.divider()


# =========================================================
# SUBJECT PERFORMANCE
# =========================================================

st.subheader("🎯 Academic Priorities")


subjects = [
    ("🤖", "Agentic AI", 72),
    ("💻", "Operating Systems", 55),
    ("🗄️", "Database Systems", 76),
    ("🧪", "Software Testing", 68),
]


for icon, subject, score in subjects:

    with st.container(border=True):

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.markdown(
                f"### {icon} {subject}"
            )

            st.progress(
                score / 100
            )

        with col2:

            st.metric(
                "Mastery",
                f"{score}%"
            )

        if score < 60:

            st.warning(
                "Needs Attention"
            )

        elif score >= 75:

            st.success(
                "Good Performance"
            )

        else:

            st.info(
                "Improving"
            )


# =========================================================
# AI INSIGHT
# =========================================================

st.divider()

st.subheader("🤖 EduAgent Insight")

st.info(
    """
**Operating Systems** is currently your biggest
opportunity for improvement.

Current mastery: **55%**

Target mastery: **80%**
"""
)

st.warning(
    """
💡 Recommendation: Spend your next 3 study sessions
on memory management and process scheduling.
"""
)


# =========================================================
# TODAY'S FOCUS
# =========================================================

st.divider()

st.subheader("📅 Today's Focus")


today = [
    (
        "09:00",
        "💻",
        "Operating Systems",
        "Memory Management",
        "1.5 hrs"
    ),
    (
        "11:00",
        "🤖",
        "Agentic AI",
        "LangGraph Agents",
        "1 hr"
    ),
    (
        "15:00",
        "🗄️",
        "Database Systems",
        "Normalization",
        "45 min"
    ),
]


for time, icon, subject, topic, duration in today:

    with st.container(border=True):

        col1, col2, col3, col4 = st.columns(
            [1, 1, 3, 1]
        )

        with col1:
            st.write(f"**{time}**")

        with col2:
            st.write(icon)

        with col3:
            st.write(
                f"**{subject}**"
            )

            st.caption(topic)

        with col4:
            st.write(
                f"⏱️ {duration}"
            )