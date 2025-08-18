import streamlit as st
from navbar import apply_page_chrome, render_navbar
apply_page_chrome()


TEXT_ACCENT = "#4d9019"

render_navbar('Meet the Team')

st.markdown(
    f"""
    <div style="text-align:center; margin-top: 36px;">
      <h2 style="color:{TEXT_ACCENT}; margin-bottom: 8px;">Meet the Team</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("Add team bios, roles, and links here.")

