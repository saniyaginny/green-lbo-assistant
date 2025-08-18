# navbar.py
import streamlit as st

# Keep your colors exactly as you set them
LINK_COLOR = "#bad4a6"   # link text
NAV_BG     = "#bad4a6"   # light-mode navbar background

def render_navbar(logo_path: str = "FerneLogo.png"):
    """
    Renders the top navbar:
      - Full-width green bar in light mode (transparent in dark mode)
      - Same st.page_link buttons and spacing you already use
      - Logo aligned at the far right (clickable -> Home)
    """
    st.markdown(
        f"""
        <style>
        /* Hide Streamlit's sidebar */
        [data-testid="stSidebar"] {{ display: none; }}

        /* Full-width background on the row that contains .nav-sentinel */
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
            width: 100% !important;
            max-width: 100% !important;
          }}
        }}
        @media (prefers-color-scheme: dark) {{
          div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
            background-color: transparent !important;
            width: 100% !important;
            max-width: 100% !important;
          }}
        }}

        /* Navbar padding so it reads like a bar */
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          padding: 8px 16px;
          margin: 0 0 8px 0;
        }}

        /* Tight, right-aligned page links (unchanged) */
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) .stPageLink > button {{
          background: transparent !important;
          border: none !important;
          box-shadow: none !important;
          padding: 0 !important;
          margin: 0 12px 0 0 !important;
          color: {LINK_COLOR} !important;
          text-decoration: underline !important;
          font-weight: 600 !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) .stPageLink > button:hover {{
          text-decoration: none !important;
        }}

        /* Make the logo image fit nicely in its small column */
        .nav-logo {{
          display: block;
          width: 100%;
          max-height: 40px;
          object-fit: contain;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Layout: spacer + your 4 links + a logo at far right
    spacer, col_home, col_chat, col_mult, col_team, col_logo = st.columns(
        [0.55, 0.10, 0.12, 0.18, 0.15, 0.10], gap="small"
    )

    # Sentinel marks the row we style as the "navbar"
    with spacer:
        st.markdown('<span class="nav-sentinel"></span>', unsafe_allow_html=True)

    with col_home:
        st.page_link("app.py", label="Home")
    with col_chat:
        st.page_link("pages/1_Chatbot.py", label="Chatbot")
    with col_mult:
        st.page_link("pages/3_Industry_Peer_Multiples.py", label="Industry Multiples")
    with col_team:
        st.page_link("pages/2_Meet_the_Team.py", label="Meet the Team")

    # Rightmost: clickable logo (links to Home)
    with col_logo:
        st.markdown(
            f'<a href="./"><img src="{logo_path}" alt="Ferne" class="nav-logo" /></a>',
            unsafe_allow_html=True,
        )
