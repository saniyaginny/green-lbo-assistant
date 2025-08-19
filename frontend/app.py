# app.py (your Home page)
import streamlit as st
from navbar import render_navbar

PRIMARY = "#a7c736"
TEXT_ACCENT = "#748b4e"

st.set_page_config(page_title="Home", layout="wide")
render_navbar()

# ---- existing CSS for pills ----
st.markdown("""
<style>
  .pill-container {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 16px;
  }
  .pill button {
    background: transparent !important;
    color: %s !important;
    border: 1px solid %s !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 6px 12px !important;
  }
  .pill button:hover {
    background: %s !important;
    color: white !important;
  }
</style>
""" % (PRIMARY, PRIMARY, PRIMARY), unsafe_allow_html=True)

# ---- existing hero ----
st.markdown(
    """
    <style>
    html[data-theme="light"] p.home-subtitle { color: #444; }
    html[data-theme="dark"] p.home-subtitle { color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align:center; margin-top: 36px;">
      <h2 style="color:#4d9019; margin-bottom: 8px;">Welcome to Green Buyout Intelligence</h2>
      <p class="home-subtitle">Renewable-focused P2P LBO assistant. Screen targets faster and ask document-grounded questions.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- existing card CSS ----
st.markdown("""
<style>
  .card {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    border: 2px solid #4d9019;
    border-radius: 12px;
    background: #bad4a6;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
</style>
""", unsafe_allow_html=True)

# ---- existing card content ----
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

# =========================
# ADD: Meet the Team section
# =========================

# CSS for the team grid/cards
st.markdown("""
<style>
  .team-wrap {
    max-width: 1100px;
    margin: 28px auto 0 auto;
  }
  .team-title {
    text-align: center;
    color: #4d9019;
    margin: 12px 0 18px 0;
  }
  .team-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
  }
  @media (max-width: 900px) {
    .team-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (max-width: 600px) {
    .team-grid { grid-template-columns: 1fr; }
  }
  .team-card {
    text-align: center;
    padding: 18px;
    border: 1px solid #eee;
    border-radius: 12px;
    background: #fafafa;
  }
  .team-name {
    margin: 0 0 4px 0;
    color: #4d9019;
  }
  .team-role {
    margin: 0;
    font-weight: 500;
    color: #444;
  }
  .team-link {
    margin-top: 8px;
  }
  .team-link a {
    text-decoration: none;
    color: #0077b5; /* LinkedIn blue */
    font-weight: 500;
  }
</style>
""", unsafe_allow_html=True)

# Content block
st.markdown("""
<div class="team-wrap">
  <h3 class="team-title">Meet the Team</h3>
  <div class="team-grid">
    <div class="team-card">
      <h4 class="team-name">Rahul Jageer</h4>
      <p class="team-role">Domain Lead</p>
      <p class="team-link"><a href="https://www.linkedin.com/in/rahul-jageer/" target="_blank" rel="noopener noreferrer">LinkedIn</a></p>
    </div>
    <div class="team-card">
      <h4 class="team-name">Saniya Ginny</h4>
      <p class="team-role">Frontend Engineer</p>
      <p class="team-link"><a href="https://www.linkedin.com/in/saniya-ginny/" target="_blank" rel="noopener noreferrer">LinkedIn</a></p>
    </div>
    <div class="team-card">
      <h4 class="team-name">Nandini Prasad</h4>
      <p class="team-role">Backend Engineer</p>
      <p class="team-link"><a href="https://www.linkedin.com/in/nandini-prasad-395a6128a/" target="_blank" rel="noopener noreferrer">LinkedIn</a></p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
