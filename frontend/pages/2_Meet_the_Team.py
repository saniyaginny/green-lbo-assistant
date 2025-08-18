import streamlit as st
from navbar import render_navbar

TEXT_ACCENT = "#4d9019"

st.set_page_config(page_title="Meet the Team", layout="wide")

render_navbar()

st.markdown(
    f"""
    <div style="text-align:center; margin-top: 36px;">
      <h2 style="color:{TEXT_ACCENT}; margin-bottom: 8px;">Meet the Team</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("Add team bios, roles, and links here.")

