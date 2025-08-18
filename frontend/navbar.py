# frontend/navbar.py
import streamlit as st

def apply_page_chrome():
    # Wide layout, collapse sidebar (we also hide it with CSS below)
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

    # Full-width green bar with links inside; hide sidebar + toolbar + footer
    st.markdown(
        """
        <style>
          /* Hide sidebar + hamburger + toolbar + footer */
          [data-testid="stSidebar"] { display: none !important; }
          [data-testid="collapsedControl"] { display: none !important; }
          [data-testid="stToolbar"] { display: none !important; }
          footer { visibility: hidden; }
          .viewerBadge_container__1QSob { display: none !important; }

          /* Full width sticky navbar */
          .gb-bar {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 56px;
            background: #bad4a6; /* light green */
            z-index: 1000;
            box-shadow: 0 1px 0 rgba(0,0,0,0.06);
            display: flex;
            align-items: center;
          }

          /* Inner row: right aligned, tighter spacing */
          .gb-links {
            margin-left: auto;
            margin-right: 24px;
            display: inline-flex;
            gap: 14px;                 /* closer spacing */
          }

          .gb-link {
            color: #102015;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
          }
          .gb-link:hover { text-decoration: underline; }

          /* Push app content below the fixed bar */
          .stApp { margin-top: 60px; }
        </style>

        <div class="gb-bar">
          <div class="gb-links">
            <a class="gb-link" href="app.py">Home</a>
            <a class="gb-link" href="pages/1_Chatbot.py">Chatbot</a>
            <a class="gb-link" href="pages/3_Industry_Peer_Multiples.py">Industry Multiples</a>
            <a class="gb-link" href="pages/2_Meet_the_Team.py">Meet the Team</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_navbar():
    # No Streamlit widgets here—links are already inside the green bar above.
    # This keeps things predictable across pages & deployments.
    pass
