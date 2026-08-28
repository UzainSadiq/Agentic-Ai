import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: #f5f7fb;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            background: linear-gradient(135deg, #0b1220 0%, #172554 100%);
            border-radius: 20px;
            padding: 34px 38px;
            margin-bottom: 28px;
            color: white;
            box-shadow: 0 14px 40px rgba(15, 23, 42, .12);
        }

        .hero-kicker {
            font-size: 12px;
            letter-spacing: 2px;
            font-weight: 700;
            color: #93c5fd;
            margin-bottom: 9px;
        }

        .hero h1 {
            font-size: 34px;
            line-height: 1.15;
            margin: 0 0 9px 0;
        }

        .hero p {
            margin: 0;
            max-width: 780px;
            color: #dbeafe;
            font-size: 15px;
        }

        .file-chip {
            display: flex;
            align-items: center;
            gap: 10px;
            background: white;
            border: 1px solid #e2e8f0;
            padding: 13px 16px;
            border-radius: 12px;
            margin: 10px 0 16px;
            color: #0f172a;
        }

        .file-chip span {
            margin-left: auto;
            color: #64748b;
            font-size: 13px;
        }

        .status {
            display: flex;
            align-items: center;
            gap: 13px;
            border-radius: 13px;
            padding: 14px 16px;
            margin-bottom: 22px;
            border: 1px solid;
        }

        .status > span {
            font-size: 21px;
            font-weight: 800;
        }

        .status b, .status small {
            display: block;
        }

        .status small {
            margin-top: 2px;
            font-size: 12px;
        }

        .status.valid {
            background: #ecfdf5;
            border-color: #a7f3d0;
            color: #065f46;
        }

        .status.invalid {
            background: #fef2f2;
            border-color: #fecaca;
            color: #991b1b;
        }

        .metric-card, .result-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 14px;
        }

        .metric-card span, .label {
            display: block;
            font-size: 10px;
            letter-spacing: 1.2px;
            font-weight: 800;
            color: #64748b;
        }

        .metric-card strong {
            display: block;
            margin-top: 5px;
            font-size: 23px;
            color: #0f172a;
        }

        .result-card h2 {
            margin: 5px 0 0;
            font-size: 22px;
            color: #0f172a;
        }

        .result-card p {
            margin: 8px 0 0;
            line-height: 1.65;
            color: #475569;
        }

        .list-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 10px 13px;
            margin: 7px 0;
            color: #334155;
        }

        .entity {
            display: flex;
            justify-content: space-between;
            gap: 15px;
            align-items: center;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 11px 13px;
            margin: 7px 0;
        }

        .entity span {
            color: #64748b;
            font-size: 12px;
            text-transform: capitalize;
        }

        .date-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 10px 13px;
            margin: 7px 0;
            color: #334155;
        }

        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 11px;
            margin-top: 45px;
        }

        section[data-testid="stFileUploaderDropzone"] {
            border: 1.5px dashed #94a3b8;
            border-radius: 15px;
            background: white;
        }

        button[kind="primary"] {
            border-radius: 11px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
