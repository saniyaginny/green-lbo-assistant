import streamlit as st
import os, base64

NAV_BG = "#bad4a6"    # navbar background
LINK_COLOR = "black"  # link text color
ACCENT = "#4d9019"    # subtle green for hover underline

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

        :root {{
            /* Streamlit header is about 3.5rem high */
            --app-header-height: 3.5rem;
            --navbar-height: 80px; /* keep in sync with padding/img size */
        }}

        .block-container {{
            padding-top: 0rem;
        }}

        /* Full-width fixed navbar that slides down on load */
        .navbar {{
            position: fixed;
            top: var(--app-header-height);
            left: 0;
            right: 0;
            width: 100vw;
            z-index: 999;
            background-color: {NAV_BG};
            padding: 10px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-sizing: border-box;

            /* Animation & transitions */
            transform: translateY(-100%);
            animation: navSlideDown 500ms ease-out 120ms forwards;
            transition: box-shadow 250ms ease, background-color 250ms ease;
        }}

        /* Soft shadow when page is scrolled */
        .navbar.scrolled {{
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        }}

        @keyframes navSlideDown {{
            to {{ transform: translateY(0); }}
        }}

        .navbar img {{
            height: 40px;
        }}

        .nav-links {{
            display: flex;
            gap: 20px;
        }}

        .nav-links a {{
            position: relative;
            color: {LINK_COLOR};
            text-decoration: none;
            font-weight: 500;
            padding: 6px 10px;
            border-radius: 4px;
        }}

        /* Underline grows from center on hover */
        .nav-links a::after {{
            content: "";
            position: absolute;
            left: 12%;
            right: 12%;
            bottom: 6px;
            height: 2px;
            background: {ACCENT};
            transform: scaleX(0);
            transform-origin: 50% 50%;
            transition: transform 220ms ease;
        }}

        .nav-links a:hover::after {{
            transform: scaleX(1);
        }}

        /* Spacer pushes content below fixed navbar + Streamlit header */
        .navbar-spacer {{
            height: calc(var(--navbar-height) + var(--app-header-height));
            width: 100%;
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
            </div>
        </div>

        <!-- Spacer so page content isn't hidden under the fixed navbar -->
        <div class="navbar-spacer"></div>

        <script>
        // Add/remove 'scrolled' class for shadow after slight scroll
        (function() {{
          const nav = document.querySelector('.navbar');
          const onScroll = () => {{
            if (!nav) return;
            if (window.scrollY > 4) {{
              nav.classList.add('scrolled');
            }} else {{
              nav.classList.remove('scrolled');
            }}
          }};
          window.addEventListener('scroll', onScroll, {{ passive: true }});
          onScroll(); // initialize on load
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
