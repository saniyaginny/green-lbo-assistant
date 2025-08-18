import streamlit as st

LINK_COLOR = "#bad4a6"  # link text
NAV_BG = "#bad4a6"      
def render_navbar():
    st.markdown(
        f"""
        <style>
        /* hide Streamlit's sidebar */
        [data-testid="stSidebar"] {{ display: none; }}

        /* --- Light/Dark detection (all fallbacks) --- */
        /* Streamlit sometimes sets data-theme on html or body */
        html[data-theme="light"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel),
        body[data-theme="light"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          background-color: {NAV_BG} !important;
        }}
        html[data-theme="dark"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel),
        body[data-theme="dark"] div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          background-color: transparent !important;
        }}
        /* Browser/OS light/dark as a fallback */
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

        /* row padding so the bar looks like a navbar */
        div[data-testid="stHorizontalBlock"]:has(.nav-sentinel) {{
          padding: 8px 16px;
          margin: 0 0 8px 0;
        }}

        /* compact, right-aligned page links */
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
        </style>
        """,
        unsafe_allow_html=True,
    )

    # right-aligned, tight links (same layout you liked)
    spacer, col_home, col_chat, col_mult, col_team = st.columns(
        [0.60, 0.10, 0.12, 0.18, 0.18], gap="small"
    )
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
