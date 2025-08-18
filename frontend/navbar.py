import streamlit as st

LINK_COLOR = "#000000"  # black text
NAV_BG = "#bad4a6"      # green background

def render_navbar():
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{ display: none; }}

        /* Full-width navbar container */
        .navbar {{
          width: 100% !important;
          background-color: {NAV_BG};
          padding: 10px 20px;
          display: flex;
          justify-content: flex-end;
          gap: 20px;
        }}

        .navbar a {{
          background: transparent;
          border: none;
          color: {LINK_COLOR};
          font-weight: 600;
          text-decoration: none;
          padding: 6px 12px;
          border-radius: 6px;
        }}

        .navbar a:hover {{
          background-color: rgba(0,0,0,0.05);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="navbar">
          <a href="/app">Home</a>
          <a href="/Chatbot">Chatbot</a>
          <a href="/Industry_Peer_Multiples">Industry Multiples</a>
          <a href="/Meet_the_Team">Meet the Team</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
