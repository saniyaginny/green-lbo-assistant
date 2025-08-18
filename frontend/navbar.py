import streamlit as st

def apply_page_chrome():
    """Sets global Streamlit page settings (title, layout, hides sidebar)."""
    st.set_page_config(layout="wide")
    hide_sidebar_style = """
        <style>
            [data-testid="stSidebar"] {display: none;}
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)


def render_navbar():
    """Renders a clean top navbar with active page highlighting."""
    st.markdown(
        """
        <style>
        .navbar {
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-top: 8px;
            margin-bottom: 28px;
        }
        .nav-button {
            padding: 8px 18px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            color: black !important;
            background-color: transparent;
            border: none;
            transition: background-color 0.2s ease;
        }
        .nav-button:hover {
            background-color: var(--secondaryBackgroundColor);
        }
        .nav-button.active {
            background-color: var(--secondaryBackgroundColor);
            font-weight: 600;
        }
        </style>
        
        <div class="navbar">
            <a class="nav-button {home}" href="/">Home</a>
            <a class="nav-button {chatbot}" href="/Chatbot">Chatbot</a>
            <a class="nav-button {multiples}" href="/Industry_Multiples">Industry Multiples</a>
            <a class="nav-button {team}" href="/Meet_the_Team">Meet the Team</a>
        </div>
        """.format(
            home="active" if st.session_state.get("page") == "home" else "",
            chatbot="active" if st.session_state.get("page") == "chatbot" else "",
            multiples="active" if st.session_state.get("page") == "multiples" else "",
            team="active" if st.session_state.get("page") == "team" else "",
        ),
        unsafe_allow_html=True
    )
