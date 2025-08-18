import streamlit as st

LINK_COLOR = "#bad4a6"  # link text
NAV_BG = "#bad4a6"      # light-mode navbar background

import streamlit as st

def render_navbar():
    st.markdown(
        """
        <style>
        /* Full-width navbar */
        .full-navbar {
            background-color: #bad4a6;   /* your green hex */
            width: 100vw;               /* full viewport width */
            position: fixed;            /* sticks at top */
            top: 0;
            left: 0;
            z-index: 999;
            padding: 12px 24px;
            display: flex;
            justify-content: flex-end;  /* links aligned to right */
            gap: 24px;                  /* spacing between links */
        }
        .full-navbar a {
            color: black;
            text-decoration: none;
            font-weight: 500;
        }
        .full-navbar a:hover {
            text-decoration: underline;
        }
        /* Push page content down so it’s not hidden behind navbar */
        .stApp {
            margin-top: 60px;
        }
        </style>

        <div class="full-navbar">
            <a href="/Home">Home</a>
            <a href="/Industry_Multiples">Industry Multiples</a>
            <a href="/Meet_the_Team">Meet the Team</a>
            <a href="/Chatbot">Chatbot</a>
        </div>
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
