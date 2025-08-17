import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Green Buyout Intelligence", layout="wide")

# Top bar
st.markdown("""
<style>
.topbar { background: #e0ecb4; padding: 12px 24px; }
.nav   { display:flex; justify-content:flex-end; gap:28px; font-weight:600; }
.nav a { color:#355E3B; text-decoration: underline; }
.center { text-align:center; margin-top: 40px; }
.round-btn {
  background:#8CC63E; color:white; border:none; padding:14px 28px;
  border-radius:999px; font-weight:600; cursor:pointer;
}
.round-btn:hover { filter:brightness(0.95); }
</style>
<div class="topbar">
  <div class="nav">
    <a href="/" target="_self">Home</a>
    <a href="/Chatbot" target="_self">Chatbot</a>
    <a href="/Meet_the_Team" target="_self">Meet the Team</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="center"><em><h3>Home</h3></em></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.markdown("""
    <div class="center">
      <a href="/Chatbot" target="_self"><button class="round-btn">Chatbot</button></a>
    </div>
    """, unsafe_allow_html=True)

backend = os.getenv("BACKEND_URL", "http://localhost:8000")
st.caption(f"Backend: {backend}")

