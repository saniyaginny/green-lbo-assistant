# frontend/navbar.py
import streamlit as st

def render_navbar():
    st.markdown(
        """
        <style>
          .nav-wrap {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            background: #bad4a6; /* your green */
            z-index: 999;
            padding: 12px 16px;
          }
          .nav-row { display: flex; justify-content: flex-end; gap: 18px; }
          .stApp { margin-top: 56px; } /* push content below bar */
        </style>
        <div class="nav-wrap"><div class="nav-row"></div></div>
        """,
        unsafe_allow_html=True,
    )

    # Put the actual links right under the styled div; they’ll appear at the top
    cols = st.columns([0.55, 0.15, 0.15, 0.15])
    with cols[1]:
        st.page_link("app.py", label="Home")
    with cols[2]:
        st.page_link("pages/3_Industry_Peer_Multiples.py", label="Industry Multiples")
    with cols[3]:
        st.page_link("pages/2_Meet_the_Team.py", label="Meet the Team")

    # if you want Chatbot too:
    # add another column or adjust ratios
    # with cols[?]:
    #     st.page_link("pages/1_Chatbot.py", label="Chatbot")

