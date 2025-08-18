# navbar.py
import streamlit as st

LINK_COLOR = "#bad4a6"   # link text (same as before)
NAV_BG     = "#bad4a6"   # light-mode navbar background

def render_navbar(logo_path: str = "FerneLogo.png"):
    st.markdown(
        f"""
        <style>
        /* Hide Streamlit's sidebar */
        [data-testid="stSidebar"] {{ display: none; }}

        /* Make the row that contains .nav-sentinel a full-width bar */
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

        /* Navbar padding */
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          padding: 8px 16px;
          margin: 0 0 8px 0;
        }}

        /* Keep your compact, right-aligned link style */
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

        /* Logo sizing */
        .nav-logo {{
          display: block;
          max-height: 36px;
          width: auto;
          object-fit: contain;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Layout: logo (left) + spacer + your original right-aligned links
    # (Previously you had: spacer, Home, Chatbot, Industry, Team with widths [0.60,0.10,0.12,0.18,0.18])
    # We insert a small logo column at the left, shrink spacer accordingly to keep link positions.
    col_logo, spacer, col_home, col_chat, col_mult, col_team = st.columns(
        [0.08, 0.52, 0.10, 0.12, 0.18, 0.18], gap="small"
    )

    # Sentinel marks the row we style as the navbar
    with spacer:
        st.markdown('<span class="nav-sentinel"></span>', unsafe_allow_html=True)

    # Left-aligned logo (clickable -> Home)
    with col_logo:
        st.markdown(
            f'<a href="./"><img src="{logo_path}" alt="Ferne" class="nav-logo" /></a>',
            unsafe_allow_html=True,
        )

    # Right-aligned links (same order/spacing you had)
    with col_home:
        st.page_link("app.py", label="Home")
    with col_chat:
        st.page_link("pages/1_Chatbot.py", label="Chatbot")
    with col_mult:
        st.page_link("pages/3_Industry_Peer_Multiples.py", label="Industry Multiples")
    with col_team:
        st.page_link("pages/2_Meet_the_Team.py", label="Meet the Team")
