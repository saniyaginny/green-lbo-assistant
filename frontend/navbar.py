# frontend/navbar.py
import streamlit as st

def apply_page_chrome():
    # Wide layout; we'll also fully hide the sidebar + toolbar via CSS below
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

    st.markdown(
        """
        <style>
          /* Hide sidebar, hamburger, top toolbar, and footer */
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
            background: #bad4a6;            /* light green */
            z-index: 1000;
            box-shadow: 0 1px 0 rgba(0,0,0,0.06);
          }

          /* Push page content below the fixed bar */
          .stApp { margin-top: 60px; }

          /* Place next Streamlit block INSIDE the green bar (top-right) */
          #gb-spot + div {
            position: fixed !important;
            top: 8px;
            right: 20px;
            z-index: 1001;
            background: transparent !important;
          }

          /* Make buttons appear inline and pill-styled */
          #gb-spot + div .stButton { display: inline-block; margin-left: 10px; }
          #gb-spot + div .stButton > button {
            background: #ffffff !important;
            color: #102015 !important;
            border: 1px solid #7ea86a !important;
            border-radius: 999px !important;
            padding: 4px 14px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
          }
          #gb-spot + div .stButton > button:hover {
            background: #7ea86a !important;
            color: #ffffff !important;
          }
        </style>

        <!-- The fixed green background bar -->
        <div class="gb-bar"></div>
        """,
        unsafe_allow_html=True,
    )


def render_navbar():
    # Anchor the next Streamlit container so CSS can position it inside the bar
    st.markdown('<div id="gb-spot"></div>', unsafe_allow_html=True)

    # The very next block becomes the button row INSIDE the bar (top-right)
    nav = st.container()

    with nav:
        # Order: Home, Chatbot, Industry Multiples, Meet the Team
        if st.button("Home"):
            try:
                st.switch_page("app.py")
            except Exception:
                st.switch_page("frontend/app.py")  # fallback if your main path differs

        if st.button("Chatbot"):
            st.switch_page("pages/1_Chatbot.py")

        if st.button("Industry Multiples"):
            st.switch_page("pages/3_Industry_Peer_Multiples.py")

        if st.button("Meet the Team"):
            st.switch_page("pages/2_Meet_the_Team.py")
