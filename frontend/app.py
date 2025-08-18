# frontend/app.py
import streamlit as st
from navbar import apply_page_chrome, render_navbar

# Apply global chrome (wide layout, hide sidebar/hamburger/toolbar, inject top green bar shell)
apply_page_chrome()

# Brand colors
PRIMARY = "#a7c736"       # yellow-green accent you use
TEXT_ACCENT = "#748b4e"   # grey-green
TITLE_COLOR = "#4d9019"   # headline green
CARD_BG = "#bad4a6"       # light green card background

# Render the full-width green navbar with page links
render_navbar()

# Optional: pill-link styling (kept for future use)
st.markdown(
    f"""
    <style>
      .pill-container {{
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 16px;
      }}
      .pill button {{
        background: transparent !important;
        color: {PRIMARY} !important;
        border: 1px solid {PRIMARY} !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 6px 12px !important;
      }}
      .pill button:hover {{
        background: {PRIMARY} !important;
        color: white !important;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Make the subtitle switch to white in dark mode for readability
st.markdown(
    """
    <style>
      html[data-theme="light"] p.home-subtitle { color: #444; }
      html[data-theme="dark"]  p.home-subtitle { color: #ffffff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero
st.markdown(
    f"""
    <div style="text-align:center; margin-top: 36px;">
      <h2 style="color:{TITLE_COLOR}; margin-bottom: 8px;">Welcome to Green Buyout Intelligence</h2>
      <p class="home-subtitle">Renewable-focused P2P LBO assistant. Screen targets faster and ask document-grounded questions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Card styles
st.markdown(
    f"""
    <style>
      .card {{
        max-width: 900px;
        margin: 0 auto;
        padding: 20px 24px;
        border: 2px solid {TITLE_COLOR};
        border-radius: 12px;
        background: {CARD_BG};
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
      }}
      .card h4 {{
        margin-top: 0;
        margin-bottom: 12px;
      }}
      .card ul {{
        margin-top: 8px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Card content
st.markdown(
    """
    <div class="card">
      <h4>What you can do</h4>
      <ul>
        <li>Upload a 10-K/10-Q and ask focused questions.</li>
        <li>Use filters and prompts to spot LBO-ready profiles.</li>
        <li>See cited snippets so you can trust the output.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
