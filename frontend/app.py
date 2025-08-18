mimport streamlit as st
from navbar import render_navbar

PRIMARY = "#a7c736"
TEXT_ACCENT = "#748b4e"

# Set page title to fix sidebar label
st.set_page_config(page_title="Home", layout="wide")

render_navbar()

# CSS for pill-style page links
st.markdown(f"""
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
""", unsafe_allow_html=True)

# Hero section without italic heading
st.markdown(
    """
    <style>
    /* Light mode: keep your normal color */
    html[data-theme="light"] p.home-subtitle {
        color: #444;
    }
    /* Dark mode: make it white */
    html[data-theme="dark"] p.home-subtitle {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align:center; margin-top: 36px;">
      <h2 style="color:#4d9019; margin-bottom: 8px;">Welcome to Ferne</h2>
      <p class="home-subtitle">Renewable-focused P2P LBO assistant. Screen targets faster and ask document-grounded questions.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# What you can do card
st.markdown(f"""
<style>
  .card {{
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    border: 2px solid #4d9019; /* slightly darker border */
    border-radius: 12px;
    background: #bad4a6
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }}
</style>
""", unsafe_allow_html=True)

# Card content
st.markdown("""
<div class="card">
  <h4>What you can do</h4>
  <ul>
    <li>Upload a 10-K/10-Q and ask focused questions.</li>
    <li>Use filters and prompts to spot LBO-ready profiles.</li>
    <li>See cited snippets so you can trust the output.</li>
  </ul>
</div>
""", unsafe_allow_html=True)
