import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        .stApp { background: #f5f7fb; }
        .block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 3rem; }

        .hero {
            background: linear-gradient(135deg, #0b1220, #312e81);
            color: white; padding: 34px 38px; border-radius: 20px;
            margin-bottom: 28px; box-shadow: 0 15px 40px rgba(15,23,42,.12);
        }
        .kicker { color: #c4b5fd; font-size: 11px; font-weight: 800; letter-spacing: 2px; margin-bottom: 8px; }
        .hero h1 { font-size: 34px; margin: 0 0 8px; line-height: 1.15; }
        .hero p { margin: 0; color: #e0e7ff; font-size: 15px; max-width: 780px; }

        .empty-card, .decision-card {
            background: white; border: 1px solid #e2e8f0; border-radius: 15px;
            padding: 22px; margin-top: 5px;
        }
        .empty-card { min-height: 220px; text-align: center; padding-top: 55px; color: #64748b; }
        .empty-icon { font-size: 36px; color: #94a3b8; margin-bottom: 10px; }
        .empty-card p { font-size: 13px; }

        .decision-card h2 { margin: 5px 0 7px; color: #111827; font-size: 23px; }
        .decision-card p { margin: 0; color: #64748b; line-height: 1.55; }
        .label { font-size: 10px; letter-spacing: 1.2px; font-weight: 800; color: #64748b; }

        .action {
            display: flex; gap: 12px; align-items: center; background: white;
            border: 1px solid #e2e8f0; border-radius: 11px; padding: 12px 13px; margin: 8px 0;
        }
        .action-icon {
            width: 27px; height: 27px; border-radius: 50%; display: flex;
            align-items: center; justify-content: center; font-weight: 800;
        }
        .action.success .action-icon { background: #dcfce7; color: #166534; }
        .action.warning .action-icon { background: #fef3c7; color: #92400e; }
        .action b, .action small { display: block; }
        .action small { color: #64748b; margin-top: 2px; }

        .pipeline {
            margin-top: 35px; padding: 14px; text-align: center; border-top: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0; color: #64748b; font-size: 11px; letter-spacing: .8px;
        }
        .pipeline span { color: #6366f1; padding: 0 7px; font-weight: 800; }
        .footer { text-align: center; color: #94a3b8; font-size: 11px; margin-top: 24px; }

        div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
            border-radius: 11px;
        }
        button[kind="primary"] { border-radius: 10px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
