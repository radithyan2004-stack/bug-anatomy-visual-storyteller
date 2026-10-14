import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

API_KEY_ENV_VAR = "GROQ_API_KEY"

st.set_page_config(
    page_title="Bug Anatomy Visual Storyteller",
    page_icon="🐛",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --glass-border: rgba(255, 255, 255, 0.16);
        --text-muted: #b9c5dc;
        --cyan: #8be9ff;
        --violet: #b9a3ff;
    }

    .stApp {
        color: #f5f7ff;
        background:
            radial-gradient(ellipse at 12% 8%, rgba(70, 102, 206, 0.32), transparent 35%),
            radial-gradient(ellipse at 88% 17%, rgba(117, 65, 190, 0.28), transparent 32%),
            radial-gradient(ellipse at 54% 100%, rgba(24, 150, 170, 0.18), transparent 42%),
            #080d1b;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {
        position: fixed;
        z-index: 0;
        width: 22rem;
        height: 22rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(139, 233, 255, 0.08), rgba(185, 163, 255, 0.025));
        box-shadow: inset 0 0 70px rgba(139, 233, 255, 0.045), 0 0 90px rgba(110, 101, 226, 0.08);
        content: '';
        pointer-events: none;
        animation: liquid-drift 18s ease-in-out infinite alternate;
    }

    [data-testid="stAppViewContainer"]::before {
        top: 18%;
        left: -12rem;
    }

    [data-testid="stAppViewContainer"]::after {
        right: -13rem;
        bottom: 4%;
        animation-delay: -8s;
    }

    @keyframes liquid-drift {
        from { transform: translate3d(0, -10px, 0) scale(0.96); }
        to { transform: translate3d(18px, 16px, 0) scale(1.04); }
    }

    [data-testid="stHeader"] {
        background: rgba(8, 13, 27, 0.4);
    }

    [data-testid="stMain"] {
        position: relative;
        z-index: 1;
    }

    .main .block-container {
        max-width: 1120px;
        padding: 3.5rem 2rem 2rem;
    }

    .st-key-hero {
        text-align: center;
    }

    .st-key-hero [data-testid="stMarkdownContainer"] p {
        max-width: 720px;
        margin: 0 auto;
    }

    h1, h2, h3 {
        color: #f7f8ff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        letter-spacing: -0.035em;
    }

    h1 {
        margin-bottom: 0.5rem;
        text-align: center;
        background: linear-gradient(100deg, #fff 15%, var(--cyan) 52%, var(--violet) 90%);
        background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 24px rgba(139, 233, 255, 0.18));
    }

    .main .block-container [data-testid="stMarkdownContainer"] p {
        color: var(--text-muted);
        line-height: 1.75;
    }

    .st-key-input_panel {
        margin: 1.6rem 0 1.2rem;
        padding: 1.25rem 1.4rem 0.35rem;
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.095), rgba(255, 255, 255, 0.035));
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.09), 0 22px 60px rgba(0, 0, 0, 0.18);
        backdrop-filter: blur(24px) saturate(145%);
        -webkit-backdrop-filter: blur(24px) saturate(145%);
    }

    hr {
        height: 1px;
        margin: 1.8rem 0;
        border: 0;
        background: linear-gradient(90deg, transparent, rgba(139, 233, 255, 0.42), rgba(185, 163, 255, 0.42), transparent);
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(13, 19, 38, 0.56);
        backdrop-filter: blur(28px) saturate(150%);
        -webkit-backdrop-filter: blur(28px) saturate(150%);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #eef2ff;
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        border: 1px solid var(--glass-border);
        border-radius: 18px;
        color: #f7f8ff;
        background: rgba(14, 21, 41, 0.64);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.055), 0 12px 35px rgba(0, 0, 0, 0.14);
        transition: border-color 180ms ease, box-shadow 180ms ease, background 180ms ease;
    }

    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: #8d9ab4;
    }

    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: rgba(139, 233, 255, 0.72);
        background: rgba(17, 26, 49, 0.82);
        box-shadow: 0 0 0 3px rgba(139, 233, 255, 0.12), 0 0 28px rgba(86, 192, 229, 0.11);
    }

    [data-testid="stButton"] button {
        min-height: 3.15rem;
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 999px;
        color: #08101e;
        background: linear-gradient(110deg, #9af0ff, #c2b1ff 58%, #e3c4ff);
        box-shadow: 0 8px 28px rgba(112, 151, 255, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.72);
        font-weight: 700;
        transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
    }

    [data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        filter: brightness(1.06);
        box-shadow: 0 12px 34px rgba(112, 151, 255, 0.34), inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }

    [data-testid="stButton"] button:focus-visible {
        outline: 2px solid var(--cyan);
        outline-offset: 3px;
    }

    [data-testid="stAlert"], [data-testid="stStatusWidget"] {
        border: 1px solid var(--glass-border);
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.075);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }

    [data-testid="stCaptionContainer"] {
        color: #8f9bb5;
        text-align: center;
    }

    @media (max-width: 640px) {
        .main .block-container {
            padding: 2rem 1rem 1.5rem;
        }
        .st-key-input_panel {
            padding: 1rem 0.9rem 0.25rem;
            border-radius: 20px;
        }
        h1 {
            font-size: 2rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            scroll-behavior: auto !important;
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container(key="hero"):
    st.title("🐛 The Bug Anatomy Visual Storyteller")
    st.markdown(
        "**Master's Portfolio Project:** Turn ugly error logs and stack traces into a humorous 'Detective Dossier' and visual breakdown instantly!"
    )

st.markdown("---")

st.sidebar.header("⚙️ Configuration")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    value=os.getenv(API_KEY_ENV_VAR, "").strip(),
)

if api_key_input:
    api_key_input = api_key_input.strip()
    os.environ[API_KEY_ENV_VAR] = api_key_input
elif os.getenv(API_KEY_ENV_VAR):
    api_key_input = os.getenv(API_KEY_ENV_VAR, "").strip()

with st.container(key="input_panel"):
    error_input = st.text_area(
        "Paste your stack trace, crash log, or error message below:",
        placeholder="e.g., ConnectionRefusedError: [Errno 61] Connection refused at socket.connect(sa)...",
        height=160,
    )
    run_analysis = st.button("Autopsy This Bug 🕵️‍♂️", type="primary")

if run_analysis:
    api_key = (os.getenv(API_KEY_ENV_VAR) or api_key_input or "").strip()

    if not api_key:
        st.error("⚠️ Please enter your Groq API Key in the sidebar or `.env` file.")
    elif not error_input.strip():
        st.warning("⚠️ Please paste an error log before running the analysis.")
    else:
        with st.spinner("Summoning the software detective and mapping crash anatomy..."):
            try:
                llm = ChatGroq(
                    model="openai/gpt-oss-20b",
                    temperature=0.3,
                    api_key=api_key,
                )

                prompt = f"""
                You are a sarcastic, brilliant software detective and senior site reliability engineer.
                Analyze the following error log or stack trace. Provide your response in clear Markdown with these three sections:

                ### 🕵️‍♂️ Detective Dossier
                A witty, engaging, and clear explanation of *why* the crash happened. Use a creative real-world analogy (like a plumbing disaster, traffic jam, or crossed wires) to explain the root cause.

                ### 🛠️ How to Solve It
                Give a practical, step-by-step fix for the root cause. When the log includes enough context, show a corrected code snippet in a fenced code block with the appropriate language tag and explain what changed. If the exact source code or relevant context is missing, say what you are assuming and show a clearly labeled illustrative example instead of presenting guessed code as the exact fix. Include a brief way to verify the fix.

                ### 🗺️ Failure Flowchart Sequence
                Provide a Mermaid.js flowchart code block (wrapped inside ```mermaid and ```) mapping out the step-by-step failure chain so a developer can trace the bug instantly.

                Error Log to Analyze:
                {error_input}
                """

                response = llm.invoke(prompt)
                output = getattr(response, "content", str(response)).strip()

                if not output:
                    raise ValueError("The AI returned an empty response.")

                st.markdown("### 📊 Autopsy Results")
                st.markdown(output)
            except Exception as exc:
                st.error(f"❌ Error communicating with AI pipeline: {exc}")

st.markdown("---")
st.caption(
    "Built for AI & Big Data Portfolios | Zero Database Infrastructure | Powered by Streamlit & Groq"
)