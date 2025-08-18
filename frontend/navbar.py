# navbar.py
import streamlit as st

LINK_COLOR = "#000000"   # black text for links
NAV_BG     = "#bad4a6"   # light-mode navbar background

def render_navbar(logo_path: str = "FerneLogo.png"):
    """
    Renders the top navbar:
      - Full-width green bar in light mode (transparent in dark mode)
      - Logo aligned on the left
      - Navigation links to the right
    """
    st.markdown(
        f"""
        <style>
        /* Hide Streamlit's sidebar */
        [data-testid="stSidebar"] {{ display: none; }}

        /* Full-width background bar */
        html[data-theme="light"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel),
        body[data-theme="light"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          background-color: {NAV_BG} !important;
          width: 100% !important;
          max-width: 100% !important;
        }}
        html[data-theme="dark"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel),
        body[data-theme="dark"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          background-color: transparent !important;
          width: 100% !important;
          max-width: 100% !important;
        }}
        @media (prefers-color-scheme: light) {{
          div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
            background-color: {NAV_BG} !important;
          }}
        }}
        @media (prefers-color-scheme: dark) {{
          div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
            background-color: transparent !important;
          }}
        }}

        /* Navbar padding */
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          padding: 8px 16px;
          margin: 0 0 8px 0;
        }}

        /* Style the links as buttons */
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) .stPageLink > button {{
          background: transparent !important;
          border: none !important;
          box-shadow: none !important;
          padding: 6px 12px !important;
          margin: 0 6px !important;
          color: {LINK_COLOR} !important;
          font-weight: 600 !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) .stPageLink > button:hover {{
          background-color: rgba(0,0,0,0.05) !important;
          border-radius: 6px;
        }}

        /* Logo sizing */
        .nav-logo {{
          max-height: 40px;
          object-fit: contain;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Layout: logo left, links right
    col_logo, col_home, col_chat, col_mult, col_team, spacer = st.columns(
        [0.10, 0.10, 0.12, 0.18, 0.18, 0.32], gap="small"
    )

    # Sentinel
    with col_logo:
        st.markdown('<span class="nav-sentinel"></span>', unsafe_allow_html=True)
        st.markdown(
            f'<a href="./"><img src="{logo_path}" alt="Ferne" class="nav-logo" /></a>',
            unsafe_allow_html=True,
        )

    with col_home:
        st.page_link("app.py", label="Home")
    with col_chat:
        st.page_link("pages/1_Chatbot.py", label="Chatbot")
    with col_mult:
        st.page_link("pages/3_Industry_Peer_Multiples.py", label="Industry Multiples")
    with col_team:
        st.page_link("pages/2_Meet_the_Team.py", label="Meet the Team")
