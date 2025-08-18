# frontend/navbar.py
import streamlit as st

def apply_page_chrome():
    # Wide layout; collapse sidebar
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

    st.markdown(
        """
        <style>
          /* Hide sidebar + hamburger + toolbar + footer */
          [data-testid="stSidebar"] { display: none !important; }
          [data-testid="collapsedControl"] { display: none !important; }
          [data-testid="stToolbar"] { display: none !important; }
          footer { visibility: hidden; }
          .viewerBadge_container__1QSob { display: none !important; }

          /* Full-width sticky green bar */
          .gb-bar {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 56px;
            background: #bad4a6;
            z-index: 1000;
            box-shadow: 0 1px 0 rgba(0,0,0,0.06);
            display: flex;
            align-items: center;
          }

          /* Right-aligned, tight row */
          .gb-links {
            margin-left: auto;
            margin-right: 20px;
            display: inline-flex;
            gap: 12px; /* tighter spacing */
          }

          /* Pill-style buttons */
          .gb-pill {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 999px;
            border: 1px solid #7ea86a;
            background: #ffffff;
            color: #102015;
            font-weight: 600;
            font-size: 15px;
            text-decoration: none;
            line-height: 1;
          }
          .gb-pill:hover {
            background: #7ea86a;
            color: #ffffff;
          }

          /* Push content below fixed bar */
          .stApp { margin-top: 60px; }
        </style>

        <!-- Green bar with links INSIDE -->
        <div class="gb-bar">
          <div class="gb-links">
            <!-- Home goes to root (no query) -->
            <a class="gb-pill" href="./">Home</a>

            <!-- Query-parameter navigation to pages -->
            <a class="gb-pill" href="./?page=Chatbot">Chatbot</a>
            <a class="gb-pill" href="./?page=Industry%20Peer%20Multiples">Industry Multiples</a>
            <a class="gb-pill" href="./?page=Meet%20the%20Team">Meet the Team</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_navbar():
    # Nothing else to draw; the HTML above is the whole navbar.
    pass
