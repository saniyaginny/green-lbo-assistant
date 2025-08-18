import streamlit as st
from pathlib import Path

# Use this on every page BEFORE render_navbar()
def apply_page_chrome():
    # wide layout, collapse sidebar
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

    # hide sidebar + hamburger + Streamlit toolbar/badges/footer
    st.markdown(
        """
        <style>
          /* hide sidebar and its collapse button */
          [data-testid="stSidebar"] { display: none !important; }
          [data-testid="collapsedControl"] { display: none !important; }

          /* hide Streamlit top toolbar and viewer badge + footer */
          [data-testid="stToolbar"] { display: none !important; }
          .viewerBadge_container__1QSob { display: none !important; }
          footer { visibility: hidden; }

          /* full-width fixed top bar */
          .gb-bar {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 56px;
            background: #bad4a6; /* your green */
            z-index: 1000;
            box-shadow: 0 1px 0 rgba(0,0,0,0.06);
          }

          /* push app content below fixed bar */
          .stApp { margin-top: 60px; }
        </style>
        <div class="gb-bar"></div>
        """,
        unsafe_allow_html=True,
    )

def _page_exists(rel_path: str) -> bool:
    base = Path(__file__).resolve().parent
    return (base / rel_path).exists()

def render_navbar():
    # align links to the right in a single row
    cols = st.columns([0.45, 0.15, 0.15, 0.15, 0.10])
    with cols[1]:
        st.page_link("app.py", label="Home")
    with cols[2]:
        if _page_exists("pages/3_Industry_Peer_Multiples.py"):
            st.page_link("pages/3_Industry_Peer_Multiples.py", label="Industry Multiples")
    with cols[3]:
        if _page_exists("pages/2_Meet_the_Team.py"):
            st.page_link("pages/2_Meet_the_Team.py", label="Meet the Team")
    with cols[4]:
        if _page_exists("pages/1_Chatbot.py"):
            st.page_link("pages/1_Chatbot.py", label="Chatbot")
