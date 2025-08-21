# -*- coding: utf-8 -*-
import streamlit as st
from navbar import render_navbar
import os, base64

PRIMARY = "#a7c736"
TEXT_ACCENT = "#748b4e"

st.set_page_config(page_title="Home", layout="wide")
render_navbar()

# =========================
# Base64 helper for logo
# =========================
def _img_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    return "data:image/png;base64,{}".format(b64)

base_dir = os.path.dirname(os.path.abspath(__file__))
# Ensure this file (FerneLogo.png) sits next to app.py
logo_path = os.path.join(base_dir, "FerneLogo.png")
logo_uri = _img_to_data_uri(logo_path)

# =========================
# Global CSS
# =========================
st.markdown("""
<style>
  /* Page background */
  .stApp {
    background-color: #ffffff;
  }

  /* Pills (if used elsewhere) */
  .pill-container {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 16px;
  }
  .pill button {
    background: transparent !important;
    color: """ + PRIMARY + """ !important;
    border: 1px solid """ + PRIMARY + """ !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 6px 12px !important;
  }
  .pill button:hover {
    background: """ + PRIMARY + """ !important;
    color: white !important;
  }

  /* Hero subtitle light/dark */
  html[data-theme="light"] p.home-subtitle { color: #444; }
  html[data-theme="dark"]  p.home-subtitle { color: white; }

  /* -------- Logo: Fade + Slide Down on load -------- */
  @keyframes logoFadeDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .hero-logo {
    height: 80px;  /* tweak size here */
    animation: logoFadeDown 700ms ease-out 100ms both;
    transition: transform 300ms ease, filter 300ms ease;
  }
  .hero-logo:hover {
    transform: scale(1.08) rotate(-2deg);  /* bigger + slight tilt */
    filter: drop-shadow(0 8px 18px rgba(77, 144, 25, 0.45)); /* green glow */
  }

  /* -------- "What you can do" card (hover lift) -------- */
  .card {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    border: 2px solid #4d9019;
    border-radius: 12px;
    background: #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease, background-color 220ms ease;
  }

  /* When hovering over a team card, change the team name color */
  .team-card:hover .team-name {
    color: #2e6b0f; /* darker green */
    transition: color 200ms ease;
  }

  /* When hovering over the "What you can do" card, change the title color */
  .card:hover h4{
    color: #2e6b0f;
  }
  .card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    border-color: #4d9019;
  }

  /* -------- Team grid + card hovers -------- */
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
    background: #fff;
    transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease, background-color 220ms ease;
  }
  .team-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    border-color: #4d9019;
  }

  /* Centered name/role/link */
  .team-name { 
    margin: 0 0 4px 0; 
    color: #2b2b2b; 
    font-weight: 500;
    font-size: 100px;
    text-align: center;
  }
  .team-role { 
    margin: 0; 
    font-weight: 500; 
    color: #444; 
    text-align: center;
  }
  .team-link { 
    margin-top: 8px; 
    text-align: center;
  }
  .team-link a { 
    text-decoration: none; 
    color: #0077b5; 
    font-weight: 500; 
    transition: color 200ms ease, text-decoration 200ms ease, transform 150ms ease;
  }
  .team-link a:hover { 
    color: #005582; 
    text-decoration: underline; 
    transform: translateY(-1px);
  }

  /* Hide Streamlit's auto-inserted anchor icons on headings (safety net) */
  h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { display: none !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# Hero with animated logo
# =========================
st.markdown(
    """
    <div style="text-align:center; margin-top: 36px;">
      <img src="{0}" alt="Ferne Logo" class="hero-logo" />
      <p class="home-subtitle">Renewable-focused P2P LBO assistant. Screen targets faster and ask document-grounded questions.</p>
    </div>
    """.format(logo_uri),
    unsafe_allow_html=True
)

# =========================
# What you can do card
# =========================
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
# Meet the Team
# =========================
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
      <h5 class="team-name">Nandini Prasad</h5>
      <p class="team-role">AI Engineer</p>
      <p class="team-link"><a href="https://www.linkedin.com/in/nandini-prasad-395a6128a/" target="_blank" rel="noopener noreferrer">LinkedIn</a></p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
