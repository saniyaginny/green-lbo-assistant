# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64

NAV_BG = "#bad4a6"    # navbar background
LINK_COLOR = "black"  # link text color
ACCENT = "#4d9019"    # subtle green for hover underline

def _img_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return "data:image/png;base64,{}".format(b64)

def render_navbar() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "FerneLogo.png")
    logo_uri = _img_to_data_uri(logo_path)

    st.markdown(
        f"""
<style>
  [data-testid="stSidebar"] {{
    display: none;
  }}

  :root {{
    --app-header-height: 3.5rem;
    --navbar-height: 80px;
  }}

  .block-container {{
    padding-top: 0rem;
  }}

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
    transform: translateY(-100%);
    animation: navSlideDown 500ms ease-out 120ms forwards;
    transition: box-shadow 250ms ease, background-color 250ms ease;
  }}

  .navbar.scrolled {{
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
  }}

  @keyframes navSlideDown {{
    to {{ transform: translateY(0); }}
  }}

  /* --- Logo link + animations --- */
  .navbar-logo a {{
    display: inline-block;
    line-height: 0;
    border-radius: 10px; /* for subtle focus outline shape */
    outline: none;
    transition: transform 220ms ease, filter 220ms ease;
  }}
  .navbar-logo a:hover {{
    transform: translateY(-2px) scale(1.03);
    filter: drop-shadow(0 6px 12px rgba(0,0,0,0.08));
  }}
  .navbar-logo a:active {{
    transform: translateY(0) scale(0.98);
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.08));
  }}
  .navbar-logo img {{
    height: 40px;
    display: block;
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

  .navbar-spacer {{
    height: calc(var(--navbar-height) + var(--app-header-height));
    width: 100%;
  }}
</style>

<div class="navbar">
  <div class="navbar-logo">
    <!-- Make logo clickable; data-path enables SID rewrite -->
    <a href="./" data-path="./" target="_self" aria-label="Go to Home">
      <img src="{logo_uri}" alt="Logo">
    </a>
  </div>

  <!-- data-path is used by the script to rewrite hrefs with sid -->
  <div class="nav-links" id="ferne-nav">
    <a href="./" data-path="./" target="_self">Home</a>
    <a href="/Chatbot" data-path="/Chatbot" target="_self">Chatbot</a>
    <a href="/Industry_Peer_Multiples" data-path="/Industry_Peer_Multiples" target="_blank" rel="noopener noreferrer">Industry Multiples</a>
  </div>
</div>

<div class="navbar-spacer"></div>

<script>
(function() {{
  var KEY = "ferne_sid";
  var url = new URL(window.location.href);

  function ensureSid() {{
    var sid = url.searchParams.get("sid");
    if (!sid) {{
      var saved = window.localStorage.getItem(KEY);
      if (saved) {{
        sid = saved;
      }} else {{
        // basic UUID fallback
        if (window.crypto && window.crypto.randomUUID) {{
          sid = window.crypto.randomUUID();
        }} else {{
          sid = Math.random().toString(36).slice(2) + Date.now().toString(36);
        }}
        window.localStorage.setItem(KEY, sid);
      }}
      // put sid into URL without reloading
      url.searchParams.set("sid", sid);
      window.history.replaceState(null, "", url.toString());
    }} else {{
      // keep localStorage in sync
      window.localStorage.setItem(KEY, sid);
    }}
    return sid;
  }}

  function withSid(href, sid) {{
    try {{
      var u = href.startsWith("http") ? new URL(href) : new URL(href, window.location.origin);
      if (u.searchParams.has("sid")) {{
        u.searchParams.set("sid", sid);
      }} else {{
        u.searchParams.append("sid", sid);
      }}
      return href.startsWith("http") ? u.toString() : (u.pathname + u.search + u.hash);
    }} catch (e) {{
      // fallback: naive append
      return href + (href.indexOf("?") >= 0 ? "&" : "?") + "sid=" + encodeURIComponent(sid);
    }}
  }}

  var sid = ensureSid();

  // Rewrite navbar links to include sid
  var nav = document.getElementById("ferne-nav");
  if (nav) {{
    var anchors = nav.querySelectorAll("a[data-path]");
    anchors.forEach(function(a) {{
      var base = a.getAttribute("data-path") || a.getAttribute("href");
      a.setAttribute("href", withSid(base, sid));
    }});
  }}

  // Also rewrite the logo link to include sid
  var logoLink = document.querySelector(".navbar-logo a[data-path]");
  if (logoLink) {{
    var baseLogo = logoLink.getAttribute("data-path") || logoLink.getAttribute("href");
    logoLink.setAttribute("href", withSid(baseLogo, sid));
  }}

  // Add/remove shadow when scrolling
  var navEl = document.querySelector(".navbar");
  function onScroll() {{
    if (!navEl) return;
    if (window.scrollY > 4) {{
      navEl.classList.add("scrolled");
    }} else {{
      navEl.classList.remove("scrolled");
    }}
  }}
  window.addEventListener("scroll", onScroll, {{ passive: true }});
  onScroll();
}})();
</script>
        """,
        unsafe_allow_html=True,
    )

