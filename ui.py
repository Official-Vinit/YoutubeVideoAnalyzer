import os
import re
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from ytVideoAnalyzer import build_youtube_agent


load_dotenv()


st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="🎥",
    layout="centered",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 0% 0%, rgba(255, 174, 0, 0.28), transparent 42%),
            radial-gradient(circle at 100% 20%, rgba(13, 180, 165, 0.24), transparent 38%),
            linear-gradient(145deg, #f8fafc 0%, #eef6ff 45%, #fff7ed 100%);
    }

    .main * {
        font-family: 'Space Grotesk', sans-serif;
    }

    .hero {
        padding: 1.15rem 1.2rem;
        border-radius: 16px;
        border: 1px solid rgba(25, 35, 55, 0.1);
        background: linear-gradient(120deg, rgba(255,255,255,0.96), rgba(255,255,255,0.78));
        box-shadow: 0 12px 36px rgba(15, 23, 42, 0.08);
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(1.5rem, 2.4vw, 2rem);
        line-height: 1.25;
        letter-spacing: -0.02em;
        color: #0f172a;
    }

    .hero p {
        margin: 0.5rem 0 0;
        color: #334155;
        font-size: 0.98rem;
    }

    .status-pill {
        display: inline-block;
        margin-top: 0.8rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.76rem;
        background: #0f766e;
        color: white;
        padding: 0.28rem 0.52rem;
        border-radius: 999px;
        letter-spacing: 0.01em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


YOUTUBE_URL_RE = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com/watch\?v=[\w-]{11}([&?].*)?|youtu\.be/[\w-]{11}([?].*)?)$",
    re.IGNORECASE,
)


def _get_groq_api_key() -> str:
    secret_key = ""
    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key.strip() or os.getenv("GROQ_API_KEY", "").strip()


def _is_valid_youtube_url(url: str) -> bool:
    return bool(YOUTUBE_URL_RE.match(url.strip()))


def _extract_response_text(result) -> str:
    content = getattr(result, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(str(item) for item in content)
    if content is not None:
        return str(content)
    return str(result)


@st.cache_resource
def _get_agent():
    return build_youtube_agent()


@st.cache_data(show_spinner=False, ttl=3600)
def _analyze_video(url: str) -> str:
    result = _get_agent().run(f"Analyze this video: {url}")
    report = _extract_response_text(result)
    if not report.strip():
        raise RuntimeError("The model returned an empty response. Try again in a few seconds.")
    return report


st.markdown(
    """
    <div class="hero">
      <h1>AI YouTube Video Analyzer</h1>
      <p>Get structured chapter-by-chapter insights, clean timestamps, and key learning highlights from any public YouTube video.</p>
      <span class="status-pill">GROQ + AGNO + STREAMLIT</span>
    </div>
    """,
    unsafe_allow_html=True,
)


api_key = _get_groq_api_key()
with st.sidebar:
    st.subheader("Runtime Status")
    if api_key:
        st.success("GROQ_API_KEY detected")
    else:
        st.warning("GROQ_API_KEY missing")
        st.caption("Set it in Streamlit secrets for cloud deploy or in a local .env file.")

    st.subheader("Tips")
    st.caption("Use public videos with transcripts for best timestamp quality.")
    st.caption("Results are cached for 1 hour per URL to speed up repeated requests.")


video_url = st.text_input(
    "YouTube video URL",
    placeholder="https://www.youtube.com/watch?v=JkaxUblCGz0",
)
analyze_clicked = st.button("Analyze Video", type="primary", use_container_width=True)


if analyze_clicked:
    cleaned_url = video_url.strip()

    if not cleaned_url:
        st.error("Paste a YouTube URL first.")
    elif not _is_valid_youtube_url(cleaned_url):
        st.error("That does not look like a valid YouTube video URL.")
    elif not api_key:
        st.error("Missing GROQ_API_KEY. Add it to your environment or Streamlit secrets.")
    else:
        os.environ["GROQ_API_KEY"] = api_key
        with st.spinner("Analyzing transcript, structure, and topic flow..."):
            try:
                analysis_report = _analyze_video(cleaned_url)
            except Exception as exc:
                st.exception(exc)
            else:
                st.success("Analysis complete")
                st.markdown("### Analysis Report")
                st.markdown(analysis_report)

                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                st.download_button(
                    "Download report (.md)",
                    data=analysis_report,
                    file_name=f"youtube-analysis-{timestamp}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )