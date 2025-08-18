# frontend/navbar.py
import streamlit as st

def apply_page_chrome():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

    st.markdown(
        """
        <style>
          /* Hide sidebar + hamburger + toolbar + footer */
          [data-testid="stSidebar"] { display: none !important; }
          [data-testid="collapsedControl"] { display: none !important; }
          [data-testid="stToolbar"] { display: none !important; }
          footer {visibility: hidden;}
          .viewerBadge_container__1QSob { display: none !important; }

          /* Navbar container */
          .nav-container {
            width: 100%;
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 10px;
            margin-bottom: 30px;
          }

          /* Navbar links */
          .nav-link {
            font-weight: 600;
            font-size: 16px;
            text-decoration: none;
            color: #222;  /* dark text */
          }
          .nav-link:hover {
            text-decoration: underline;
          }
        </style>

        <div class="nav-container">
          <a class="nav-link" href="./">Home</a>
          <a class="nav-link" href="./?page=Chatbot">Chatbot</a>
          <a class="nav-link" href="./?page=Industry%20Multiples">Industry Multiples</a>
          <a class="nav-link" href="./?page=Meet%20the%20Team">Meet the Team</a>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_navbar():
    pass
