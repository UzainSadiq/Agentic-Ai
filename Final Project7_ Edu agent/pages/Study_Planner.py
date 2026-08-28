import streamlit as st

from tools.study_tools import (
    generate_study_plan
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 EduAgent")

    st.caption(
        "Smart Study Planner"
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

st.title("🎯 Smart Study Planner")

st.write(
    """
Create a personalized study plan based on your
subject, topic, difficulty and available time.
"""
)

st.divider()


# =========================================================
# INPUTS
# =========================================================

st.subheader("📝 Create Your Study Plan")


col1, col2 = st.columns(2)


with col1:

    subject = st.selectbox(
        "📚 Subject",
        [
            "Agentic AI",
            "Operating Systems",
            "Database Systems",
            "Software Testing",
            "Virtual Systems"
        ]
    )

    topic = st.text_input(
        "📖 Topic",
        placeholder=(
            "Example: LangGraph Agents"
        )
    )


with col2:

    study_date = st.date_input(
        "📅 Study Date"
    )

    duration = st.slider(
        "⏱️ Available Study Time",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )


difficulty = st.select_slider(
    "🎯 Difficulty",
    options=[
        "Easy",
        "Medium",
        "Hard"
    ],
    value="Medium"
)


st.divider()


# =========================================================
# PLAN GENERATION
# =========================================================

if st.button(
    "🚀 Generate Study Plan",
    type="primary",
    use_container_width=True
):

    if not topic:

        st.warning(
            "Please enter a topic first."
        )

    else:

        user_request = f"""
Create a study plan.

Subject: {subject}
Topic: {topic}
Date: {study_date}
Available study time: {duration} hours
Difficulty: {difficulty}
"""

        with st.spinner(
            "🧠 EduAgent is creating your plan..."
        ):

            try:

                plan = generate_study_plan(
                    user_request
                )

                st.divider()

                st.subheader(
                    "🎯 Your Personalized Study Plan"
                )

                st.success(
                    f"Plan created for {study_date}"
                )

                st.write(plan)

            except Exception as e:

                st.error(
                    "Could not generate the study plan."
                )

                st.exception(e)


# =========================================================
# STUDY METHOD
# =========================================================

st.divider()

st.subheader("📖 Recommended Study Method")


tab1, tab2, tab3 = st.tabs(
    [
        "📚 Learn",
        "🧠 Practice",
        "🔁 Review"
    ]
)


with tab1:

    st.info(
        """
        **Learn**

        Study the core concepts and understand
        the important ideas before moving to practice.
        """
    )


with tab2:

    st.warning(
        """
        **Practice**

        Solve questions, write code or work through
        practical examples related to the topic.
        """
    )


with tab3:

    st.success(
        """
        **Review**

        Use active recall and review your mistakes
        before finishing the study session.
        """
    )