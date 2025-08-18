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
            gap: 30px;
            margin-top: 5px;
            margin-bottom: 25px;
          }

          /* Navbar buttons */
          .nav-btn {
            font-weight: 600;
            font-size: 15px;
            text-decoration: none;
            color: black;
            padding: 6px 14px;
            border-radius: 4px;
            transition: background-color 0.2s ease;
          }

          /* Hover and active state use Streamlit's secondary background */
          .nav-btn:hover, .nav-btn.active {
            background-color: var(--secondary-background-color);
          }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_navbar(active="Home"):
    st.markdown(
        f"""
        <div class="nav-container">
          <a class="nav-btn {'active' if active=='Home' else ''}" href="./">Home</a>
          <a class="nav-btn {'active' if active=='Chatbot' else ''}" href="./?page=Chatbot">Chatbot</a>
          <a class="nav-btn {'active' if active=='Industry Multiples' else ''}" href="./?page=Industry%20Multiples">Industry Multiples</a>
          <a class="nav-btn {'active' if active=='Meet the Team' else ''}" href="./?page=Meet%20the%20Team">Meet the Team</a>
        </div>
        """,
        unsafe_allow_html=True
    )
