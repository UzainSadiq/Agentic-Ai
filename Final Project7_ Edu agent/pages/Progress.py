import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Progress Analytics",
    page_icon="📈",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 EduAgent")

    st.caption(
        "Progress Analytics"
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

st.title("📈 Progress Analytics")

st.write(
    """
Understand your academic growth and identify
subjects that need more attention.
"""
)

st.divider()


# =========================================================
# METRICS
# =========================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "📈 Overall Progress",
        "69%",
        "+8%"
    )


with c2:

    st.metric(
        "⏱️ Study Hours",
        "42.5h",
        "This month"
    )


with c3:

    st.metric(
        "✅ Tasks Done",
        "37",
        "+12 this week"
    )


with c4:

    st.metric(
        "🔥 Streak",
        "7 days",
        "Personal best"
    )


st.divider()


# =========================================================
# SUBJECT PERFORMANCE
# =========================================================

st.subheader("📚 Subject Performance")


subjects = [
    ("🤖 Agentic AI", 72),
    ("💻 Operating Systems", 55),
    ("🗄️ Database Systems", 76),
    ("🧪 Software Testing", 68),
    ("☁️ Virtual Systems", 81),
]


for subject, score in subjects:

    with st.container(border=True):

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.write(
                f"**{subject}**"
            )

            st.progress(
                score / 100
            )

        with col2:

            st.metric(
                "Score",
                f"{score}%"
            )


# =========================================================
# PERFORMANCE CATEGORIES
# =========================================================

st.divider()

st.subheader("📊 Performance Summary")

col1, col2, col3 = st.columns(3)


with col1:

    st.success(
        "🟢 Strong Areas"
    )

    st.write(
        """
        • Virtual Systems — 81%

        • Database Systems — 76%
        """
    )


with col2:

    st.info(
        "🔵 Improving Areas"
    )

    st.write(
        """
        • Agentic AI — 72%

        • Software Testing — 68%
        """
    )


with col3:

    st.warning(
        "🟠 Needs Attention"
    )

    st.write(
        """
        • Operating Systems — 55%
        """
    )


# =========================================================
# AI ANALYSIS
# =========================================================

st.divider()

st.subheader("🤖 AI Progress Analysis")

st.info(
    """
EduAgent detected **Operating Systems** as your
highest-priority subject.
"""
)

st.write(
    """
Your current mastery is **55%**, while your target
is **80%**.
"""
)

st.warning(
    """
Recommended action:

• 2 sessions on memory management

• 1 session on process scheduling

• 1 practice test

• Review mistakes with EduAgent
"""
)