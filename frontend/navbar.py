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
            gap: 20px;
            margin-top: 10px;
            margin-bottom: 30px;
          }

          /* Pill-style buttons */
          .nav-pill {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 999px;
            border: 1px solid #4d9019;
            background: #fff;
            color: #000;
            font-weight: 600;
            font-size: 15px;
            text-decoration: none;
          }
          .nav-pill:hover {
            background: #4d9019;
            color: white;
          }
        </style>

        <div class="nav-container">
          <a class="nav-pill" href="./">Home</a>
          <a class="nav-pill" href="./?page=Chatbot">Chatbot</a>
          <a class="nav-pill" href="./?page=Industry%20Multiples">Industry Multiples</a>
          <a class="nav-pill" href="./?page=Meet%20the%20Team">Meet the Team</a>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_navbar():
    pass
