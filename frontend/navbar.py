import streamlit as st
from pathlib import Path

# ---- Page chrome: hide sidebar, hamburger, Streamlit toolbar/badges, and push content below navbar
def apply_page_chrome():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.markdown(
        """
        <style>
          /* Hide Streamlit's default sidebar & hamburger */
          [data-testid="stSidebar"] { display: none !important; }
          [data-testid="collapsedControl"] { display: none !important; }

          /* Hide Streamlit toolbar (Share, Rerun, etc.) and viewer badge */
          [data-testid="stToolbar"] { display: none !important; }
          .viewerBadge_container__1QSob { display: none !important; }  /* legacy selector */
          footer { visibility: hidden; } /* optional: hide footer */

          /* Full-width top navbar container */
          .gb-navbar {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            z-index: 1000;
            background: #bad4a6;            /* your light green */
            box-shadow: 0 1px 0 rgba(0,0,0,0.06);
          }
          .gb-inner {
            max-width: 1200px;               /* content width; change if you want tighter/wider */
            margin: 0 auto;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: flex-end;       /* right-align links */
            gap: 24px;                       /* space between links */
          }

          /* Links */
          .gb-link {
            color: #102015;                  /* dark text for contrast on light green */
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
          }
          .gb-link:hover { text-decoration: underline; }

          /* Push app content below the fixed navbar */
          .stApp { margin-top: 60px; }       /* adjust if you change navbar height */
        </style>
        """,
        unsafe_allow_html=True,
    )


# Optional: only render links that actually exist (helps on case-sensitive Linux)
def _page_exists(rel_path: str) -> bool:
    base = Path(__file__).resolve().parent          # .../frontend/
    return (base / rel_path).resolve().exists()


def render_navbar():
    # HTML shell for the full-width green bar
    st.markdown(
        """
        <div class="gb-navbar">
          <div class="gb-inner" id="gb-links"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Put the actual links using Streamlit's page_link (works with multipage routing)
    # We place them in columns so they render inside the top area we reserved.
    cols = st.columns([0.55, 0.15, 0.15, 0.15])
    with cols[1]:
        st.page_link("app.py", label="Home")
    with cols[2]:
        if _page_exists("pages/3_Industry_Peer_Multiples.py"):
            st.page_link("pages/3_Industry_Peer_Multiples.py", label="Industry Multiples")
    with cols[3]:
        if _page_exists("pages/2_Meet_the_Team.py"):
            st.page_link("pages/2_Meet_the_Team.py", label="Meet the Team")
    # If you also want Chatbot up top, shrink the ratios and add another column:
    # cols = st.columns([0.45, 0.14, 0.14, 0.14, 0.13])
    # with cols[4]:
    #     if _page_exists("pages/1_Chatbot.py"):
    #         st.page_link("pages/1_Chatbot.py", label="Chatbot")
