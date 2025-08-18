# frontend/navbar.py
import streamlit as st
from pathlib import Path

def apply_page_chrome():
    # Wide layout, collapse sidebar
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

    # Full-width green bar + hide sidebar/hamburger/toolbar/footer
    st.markdown(
        """
        <style>
          /* Hide sidebar + hamburger + toolbar + footer */
          [data-testid="stSidebar"] { display: none !important; }
          [data-testid="collapsedControl"] { display: none !important; }
          [data-testid="stToolbar"] { display: none !important; }
          footer { visibility: hidden; }
          .viewerBadge_container__1QSob { display: none !important; }

          /* The green bar itself */
          .gb-bar {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 56px;
            background: #bad4a6;        /* your light green */
            z-index: 1000;
            box-shadow: 0 1px 0 rgba(0,0,0,0.06);
          }

          /* Push all page content below the fixed bar */
          .stApp { margin-top: 60px; }

          /* Trick: place the links row INSIDE the bar */
          #gb-links-anchor + div {
            position: fixed !important;
            top: 8px;                   /* vertical padding inside bar */
            right: 20px;                 /* right-align */
            z-index: 1001;
            background: transparent !important;
          }

          /* Tight horizontal spacing between link "buttons" */
          #gb-links-anchor + div .stButton, 
          #gb-links-anchor + div .stPageLink {
            margin-left: 18px !important;
          }
        </style>

        <!-- The fixed green bar -->
        <div class="gb-bar"></div>
        """,
        unsafe_allow_html=True,
    )

def _page_exists(rel_path: str) -> bool:
    base = Path(__file__).resolve().parent
    return (base / rel_path).exists()

def render_navbar():
    # Anchor that the CSS targets; the NEXT sibling becomes the fixed links row
    st.markdown('<div id="gb-links-anchor"></div>', unsafe_allow_html=True)

    # The links row (now positioned inside the green bar by CSS above)
    cols = st.columns([0.25, 0.15, 0.22, 0.20, 0.18])  # adjust to taste
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
