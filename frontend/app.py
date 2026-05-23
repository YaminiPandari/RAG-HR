"""
HR Assistant — Professional WhatsApp-style chat UI
Runs on top of the existing RAGService defined in main.py.
Backend code is intentionally NOT modified.
"""

import os
import sys
from datetime import datetime

import streamlit as st

# Make project root importable so we can reuse RAGService from main.py as-is.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from main import RAGService  # noqa: E402


# ---------- Brand tokens ----------
BRAND_GREEN = "#00E676"
BRAND_PURPLE = "#8A5CF6"
BRAND_PINK = "#FF2D95"
BRAND_GRADIENT = f"linear-gradient(135deg, {BRAND_GREEN} 0%, {BRAND_PURPLE} 50%, {BRAND_PINK} 100%)"


# ---------- Page config ----------
st.set_page_config(
    page_title="HR Assistant",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ---------- Global styling ----------
def inject_css() -> None:
    st.markdown(
        f"""
        <style>
            /* ---------- Base ---------- */
            html, body, [data-testid="stAppViewContainer"], .main, .block-container {{
                background: #FFFFFF !important;
            }}
            [data-testid="stHeader"] {{
                background: transparent !important;
            }}
            .block-container {{
                padding-top: 1.2rem;
                padding-bottom: 7rem;
                max-width: 820px;
            }}
            * {{
                font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            }}

            /* ---------- Sidebar ---------- */
            [data-testid="stSidebar"] {{
                background: #FFFFFF !important;
                border-right: 1px solid #F0F0F4;
            }}
            [data-testid="stSidebar"] .sidebar-brand {{
                display: flex; align-items: center; gap: 12px;
                padding: 8px 4px 18px 4px;
                border-bottom: 1px solid #F2F2F6;
                margin-bottom: 16px;
            }}
            [data-testid="stSidebar"] .sidebar-brand .logo {{
                width: 38px; height: 38px; border-radius: 12px;
                background: {BRAND_GRADIENT};
                box-shadow: 0 6px 18px rgba(138,92,246,0.25);
            }}
            [data-testid="stSidebar"] .sidebar-brand .brand-name {{
                font-weight: 700; font-size: 17px; color: #14141A;
                letter-spacing: -0.01em;
            }}
            [data-testid="stSidebar"] .sidebar-brand .brand-tag {{
                font-size: 11.5px; color: #6E6E80; margin-top: 2px;
            }}
            [data-testid="stSidebar"] .side-section-title {{
                text-transform: uppercase; letter-spacing: 0.08em;
                font-size: 11px; color: #8A8A99; font-weight: 600;
                margin: 14px 0 8px 0;
            }}
            [data-testid="stSidebar"] .side-card {{
                background: #FAFAFC;
                border: 1px solid #EFEFF4;
                border-radius: 14px;
                padding: 12px 14px;
                font-size: 13px; color: #3A3A48;
                line-height: 1.5;
            }}
            [data-testid="stSidebar"] .pill {{
                display: inline-block;
                padding: 4px 10px;
                border-radius: 999px;
                background: rgba(0,230,118,0.10);
                color: #009A52;
                font-size: 11.5px; font-weight: 600;
                margin-right: 6px; margin-top: 6px;
            }}
            [data-testid="stSidebar"] .pill.purple {{
                background: rgba(138,92,246,0.10); color: #6A3FE0;
            }}
            [data-testid="stSidebar"] .pill.pink {{
                background: rgba(255,45,149,0.10); color: #D81B73;
            }}

            /* Sidebar button */
            [data-testid="stSidebar"] .stButton > button {{
                width: 100%;
                border-radius: 12px;
                border: 1px solid #EFEFF4;
                background: #FFFFFF;
                color: #14141A;
                font-weight: 600; font-size: 13px;
                padding: 10px 12px;
                transition: all 0.15s ease;
            }}
            [data-testid="stSidebar"] .stButton > button:hover {{
                border-color: transparent;
                background: {BRAND_GRADIENT};
                color: #FFFFFF;
                box-shadow: 0 8px 22px rgba(138,92,246,0.25);
            }}

            /* ---------- Chat header ---------- */
            .chat-header {{
                position: relative;
                display: flex; align-items: center; gap: 12px;
                padding: 14px 18px;
                border-radius: 18px;
                background: {BRAND_GRADIENT};
                box-shadow: 0 10px 30px rgba(138,92,246,0.22);
                margin-bottom: 18px;
            }}
            .chat-header .avatar {{
                width: 44px; height: 44px;
                border-radius: 50%;
                background: #FFFFFF;
                display: flex; align-items: center; justify-content: center;
                font-weight: 700; color: #6A3FE0; font-size: 17px;
                box-shadow: inset 0 0 0 2px rgba(255,255,255,0.8);
            }}
            .chat-header .meta .name {{
                color: #FFFFFF; font-weight: 700; font-size: 16px;
                letter-spacing: -0.01em;
            }}
            .chat-header .meta .status {{
                display: flex; align-items: center; gap: 6px;
                color: rgba(255,255,255,0.92); font-size: 12px; margin-top: 2px;
            }}
            .chat-header .meta .status .dot {{
                width: 8px; height: 8px; border-radius: 50%;
                background: #FFFFFF;
                box-shadow: 0 0 0 3px rgba(255,255,255,0.35);
            }}
            .chat-header .actions {{
                margin-left: auto;
                display: flex; gap: 8px;
            }}
            .chat-header .actions .icon-btn {{
                width: 34px; height: 34px; border-radius: 10px;
                background: rgba(255,255,255,0.18);
                display: flex; align-items: center; justify-content: center;
                color: #FFFFFF; font-size: 15px;
            }}

            /* ---------- Chat area ---------- */
            .chat-area {{
                background: #FFFFFF;
                padding: 8px 4px 24px 4px;
            }}
            .day-divider {{
                text-align: center;
                margin: 18px 0 14px 0;
            }}
            .day-divider span {{
                background: #F4F4F8;
                color: #6E6E80;
                font-size: 11.5px; font-weight: 600;
                padding: 5px 12px;
                border-radius: 999px;
            }}

            /* Bubble rows */
            .row {{
                display: flex; width: 100%; margin: 6px 0;
            }}
            .row.user {{ justify-content: flex-end; }}
            .row.bot  {{ justify-content: flex-start; }}

            .bubble {{
                max-width: 78%;
                padding: 10px 14px 8px 14px;
                font-size: 14.5px; line-height: 1.5;
                position: relative;
                word-wrap: break-word;
                box-shadow: 0 1px 1px rgba(20,20,26,0.04);
            }}
            .bubble .time {{
                display: block;
                font-size: 10.5px;
                margin-top: 4px;
                opacity: 0.75;
                text-align: right;
            }}

            /* User bubble — brand green, WhatsApp-style right tail */
            .bubble.user {{
                background: {BRAND_GREEN};
                color: #052E16;
                border-radius: 16px 16px 4px 16px;
            }}
            .bubble.user::after {{
                content: "";
                position: absolute;
                right: -6px; bottom: 0;
                width: 12px; height: 14px;
                background: {BRAND_GREEN};
                clip-path: polygon(0 0, 0% 100%, 100% 100%);
                border-bottom-right-radius: 2px;
            }}
            .bubble.user .time {{ color: #064E2A; }}

            /* Bot bubble — soft white card with purple accent rail */
            .bubble.bot {{
                background: #F7F6FC;
                color: #14141A;
                border-radius: 16px 16px 16px 4px;
                border: 1px solid #ECEAF8;
                border-left: 3px solid {BRAND_PURPLE};
            }}
            .bubble.bot::after {{
                content: "";
                position: absolute;
                left: -6px; bottom: 0;
                width: 12px; height: 14px;
                background: #F7F6FC;
                clip-path: polygon(100% 0, 0% 100%, 100% 100%);
                border-bottom-left-radius: 2px;
            }}
            .bubble.bot .time {{ color: #6E6E80; }}

            /* Typing indicator */
            .typing {{
                display: inline-flex; align-items: center; gap: 4px;
                padding: 6px 2px;
            }}
            .typing span {{
                width: 7px; height: 7px; border-radius: 50%;
                background: {BRAND_PURPLE};
                opacity: 0.4;
                animation: blink 1.2s infinite ease-in-out;
            }}
            .typing span:nth-child(2) {{ background: {BRAND_PINK}; animation-delay: 0.15s; }}
            .typing span:nth-child(3) {{ background: {BRAND_GREEN}; animation-delay: 0.3s; }}
            @keyframes blink {{
                0%, 80%, 100% {{ opacity: 0.25; transform: translateY(0); }}
                40%           {{ opacity: 1;    transform: translateY(-2px); }}
            }}

            /* Empty state */
            .empty-state {{
                text-align: center;
                padding: 38px 14px 24px 14px;
                color: #6E6E80;
            }}
            .empty-state .badge {{
                width: 64px; height: 64px; border-radius: 20px;
                background: {BRAND_GRADIENT};
                display: inline-flex; align-items: center; justify-content: center;
                color: #FFFFFF; font-size: 28px;
                box-shadow: 0 14px 36px rgba(138,92,246,0.28);
                margin-bottom: 14px;
            }}
            .empty-state h3 {{
                color: #14141A; margin: 0 0 6px 0; font-size: 20px; font-weight: 700;
                letter-spacing: -0.01em;
            }}
            .empty-state p {{ font-size: 13.5px; margin: 0 0 18px 0; }}
            .suggestions {{
                display: flex; flex-wrap: wrap; gap: 8px;
                justify-content: center;
                margin-top: 6px;
            }}
            .suggestion {{
                font-size: 12.5px;
                color: #3A3A48;
                background: #FAFAFC;
                border: 1px solid #EDEDF3;
                padding: 8px 14px;
                border-radius: 999px;
            }}

            /* ---------- Composer (chat input) ---------- */
            /* Streamlit wraps the chat input in several outer containers that
               default to a dark colour — whiten every one of them. */
            [data-testid="stBottom"],
            [data-testid="stBottom"] > div,
            [data-testid="stBottomBlockContainer"],
            [data-testid="stChatInputContainer"],
            [data-testid="stChatInput"],
            [data-testid="stChatInput"] > div,
            [data-testid="stChatInput"] > div > div {{
                background: #FFFFFF !important;
            }}
            [data-testid="stBottom"] {{
                border-top: 1px solid #F0F0F4 !important;
                box-shadow: 0 -8px 24px rgba(20,20,26,0.04) !important;
            }}
            [data-testid="stBottomBlockContainer"] {{
                padding-top: 14px !important;
                padding-bottom: 14px !important;
                max-width: 820px;
            }}
            [data-testid="stChatInput"] textarea {{
                background: #FAFAFC !important;
                border: 1px solid #ECECF2 !important;
                border-radius: 16px !important;
                color: #14141A !important;
                padding: 12px 14px !important;
                font-size: 14.5px !important;
            }}
            [data-testid="stChatInput"] textarea:focus {{
                border-color: {BRAND_PURPLE} !important;
                box-shadow: 0 0 0 3px rgba(138,92,246,0.15) !important;
            }}
            [data-testid="stChatInput"] button {{
                background: {BRAND_GRADIENT} !important;
                border-radius: 12px !important;
                color: #FFFFFF !important;
                box-shadow: 0 6px 18px rgba(138,92,246,0.30) !important;
            }}
            [data-testid="stChatInput"] button:hover {{
                filter: brightness(1.05);
            }}

            /* Hide default Streamlit chrome we don't need */
            #MainMenu, footer {{ visibility: hidden; }}

            /* Spinner color */
            .stSpinner > div > div {{
                border-top-color: {BRAND_PURPLE} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------- Backend wiring ----------
@st.cache_resource(show_spinner="Warming up the HR knowledge base…")
def get_rag_service() -> RAGService:
    """Initialize the RAGService once and reuse across reruns."""
    return RAGService()


# ---------- UI helpers ----------
def render_header() -> None:
    st.markdown(
        """
        <div class="chat-header">
            <div class="avatar">HR</div>
            <div class="meta">
                <div class="name">HR Assistant</div>
                <div class="status"><span class="dot"></span> Online · Replies powered by your Employee Handbook</div>
            </div>
            <div class="actions">
                <div class="icon-btn" title="Secure">🔒</div>
                <div class="icon-btn" title="Verified">✓</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="logo"></div>
                <div>
                    <div class="brand-name">HR Assistant</div>
                    <div class="brand-tag">Enterprise · Knowledge Copilot</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-section-title">About</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="side-card">
                Ask anything about policies, leave, benefits, or onboarding.
                Answers are grounded in your Employee Handbook.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-section-title">Capabilities</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div>
                <span class="pill">Policy lookup</span>
                <span class="pill purple">Leave &amp; benefits</span>
                <span class="pill pink">Onboarding</span>
                <span class="pill">Compliance</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-section-title">Session</div>', unsafe_allow_html=True)
        if st.button("🧹  Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown(
            """
            <div style="position:absolute; bottom:18px; left:18px; right:18px;
                        font-size:11px; color:#9B9BAC; text-align:center;">
                © HR Assistant · Confidential
            </div>
            """,
            unsafe_allow_html=True,
        )


def now_hm() -> str:
    return datetime.now().strftime("%I:%M %p").lstrip("0")


def render_message(role: str, text: str, ts: str) -> None:
    """role ∈ {'user', 'bot'}"""
    safe = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
    )
    st.markdown(
        f"""
        <div class="row {role}">
            <div class="bubble {role}">
                {safe}
                <span class="time">{ts}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-state">
            <div class="badge">💬</div>
            <h3>Hi, I'm your HR Assistant</h3>
            <p>Ask me anything about your Employee Handbook — policies, leave, benefits, and more.</p>
            <div class="suggestions">
                <div class="suggestion">What is the leave policy?</div>
                <div class="suggestion">How does the probation period work?</div>
                <div class="suggestion">Explain the code of conduct.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- App ----------
def main() -> None:
    inject_css()
    render_sidebar()
    render_header()

    if "messages" not in st.session_state:
        st.session_state.messages = []  # list of {role, text, ts}

    rag = get_rag_service()

    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-area">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="day-divider"><span>{datetime.now().strftime("%A, %d %b %Y")}</span></div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.messages:
            render_empty_state()
        else:
            for m in st.session_state.messages:
                render_message(m["role"], m["text"], m["ts"])

        st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Type a message…")
    if user_input:
        st.session_state.messages.append(
            {"role": "user", "text": user_input, "ts": now_hm()}
        )
        render_message("user", user_input, now_hm())

        typing_slot = st.empty()
        typing_slot.markdown(
            """
            <div class="row bot">
                <div class="bubble bot">
                    <div class="typing"><span></span><span></span><span></span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            answer = rag.ask(user_input)
        except Exception as exc:  # surface backend errors gracefully in the bubble
            answer = f"Sorry, I hit an error while answering: {exc}"

        typing_slot.empty()

        st.session_state.messages.append(
            {"role": "bot", "text": str(answer), "ts": now_hm()}
        )
        render_message("bot", str(answer), now_hm())


if __name__ == "__main__":
    main()
