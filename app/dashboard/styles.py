import streamlit as st


def load_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(
                    circle at 10% 0%,
                    rgba(37, 99, 235, 0.12),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(16, 185, 129, 0.08),
                    transparent 30%
                ),
                #0b1120;
            color: #e5e7eb;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .hero {
            padding: 2.5rem;
            border-radius: 24px;
            background: linear-gradient(
                135deg,
                rgba(30, 41, 59, 0.95),
                rgba(15, 23, 42, 0.95)
            );
            border: 1px solid rgba(148, 163, 184, 0.15);
            margin-bottom: 1.5rem;
        }

        .hero-badge {
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.25);
            color: #86efac;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }

        .hero-title {
            font-size: 3.2rem;
            font-weight: 800;
            margin: 0.8rem 0 0.5rem 0;
            color: #f8fafc;
        }

        .hero-subtitle {
            font-size: 1.25rem;
            color: #94a3b8;
            max-width: 850px;
            line-height: 1.6;
        }

        .section-title {
            font-size: 1.7rem;
            font-weight: 750;
            color: #f8fafc;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }

        .card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 18px;
            padding: 1.25rem;
            min-height: 150px;
        }

        .card-title {
            color: #f8fafc;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .card-text {
            color: #94a3b8;
            line-height: 1.55;
            font-size: 0.92rem;
        }

        .pipeline {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            overflow-x: auto;
            padding: 1.25rem 0.25rem;
        }

        .pipeline-step {
            min-width: 145px;
            padding: 1rem;
            border-radius: 14px;
            background: #111827;
            border: 1px solid #263244;
            text-align: center;
        }

        .pipeline-number {
            font-size: 0.75rem;
            color: #60a5fa;
            font-weight: 700;
        }

        .pipeline-name {
            color: #f8fafc;
            font-weight: 700;
            margin-top: 0.25rem;
        }

        .pipeline-arrow {
            color: #64748b;
            font-size: 1.3rem;
        }

        .architecture {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 20px;
            padding: 1.5rem;
        }

        .arch-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.7rem;
            flex-wrap: wrap;
            margin: 0.8rem 0;
        }

        .arch-node {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            background: #111827;
            border: 1px solid #334155;
            color: #e2e8f0;
            font-weight: 650;
        }

        .arch-arrow {
            color: #64748b;
            font-size: 1.2rem;
        }

        .security-box {
            padding: 1.2rem;
            border-radius: 16px;
            background: rgba(30, 41, 59, 0.65);
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .status-good {
            color: #86efac;
            font-weight: 700;
        }

        .status-bad {
            color: #fca5a5;
            font-weight: 700;
        }

        .footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(148, 163, 184, 0.12);
            color: #64748b;
            text-align: center;
            font-size: 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )