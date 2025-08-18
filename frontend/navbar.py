import streamlit as st
import os, base64

NAV_BG = "#bad4a6"
LINK_COLOR = "#333333"

def _img_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{b64}"

def render_navbar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "FerneLogo.png")
    logo_uri = _img_to_data_uri(logo_path)

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{ display: none; }}

        .navbar {{
            width: 100%;
            background-color: {NAV_BG};
            padding: 10px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .navbar img {{
            height: 40px;
        }}

        .nav-links {{
            display: flex;
            gap: 20px;
        }}

        .nav-links a {{
            color: {LINK_COLOR};
            text-decoration: none;
            font-weight: 500;
            padding: 6px 10px;
            border-radius: 4px;
        }}

        .nav-links a:hover {{
            background-color: #d3e4c2;
        }}
        </style>

        <div class="navbar">
            <div class="navbar-logo">
                <img src="{logo_uri}" alt="Logo">
            </div>
            <div class="nav-links">
                <a href="./" target="_self">Home</a>
                <a href="/Chatbot" target="_self">Chatbot</a>
                <a href="/Industry_Peer_Multiples" target="_self">Industry Multiples</a>
                <a href="/Meet_the_Team" target="_self">Meet the Team</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
