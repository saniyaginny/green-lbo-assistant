# -*- coding: utf-8 -*-
import pandas as pd
import altair as alt
import streamlit as st
from navbar import render_navbar

# Brand colors
TITLE_COLOR = "#4d9019"   # headline green
ACCENT = "#88b45c"        # range bar color

st.set_page_config(page_title="Industry Multiples", layout="wide")
render_navbar()

# Detect theme (light/dark) and pick axis colors accordingly
theme_base = st.get_option("theme.base") or "light"
is_dark = str(theme_base).lower() == "dark"

AXIS_LABEL_COLOR = "#ffffff" if is_dark else "#000000"
AXIS_TITLE_COLOR = AXIS_LABEL_COLOR
TICK_COLOR = AXIS_LABEL_COLOR
GRID_COLOR = "#333333" if is_dark else "#e6e6e6"
MEDIAN_COLOR = "#e5e7eb" if is_dark else "#1f2937"   # light gray in dark mode / dark gray in light mode

# ---------- CSS: chart card fit + lift; centered titles; chip; description card ----------
st.markdown("""
<style>
  /* Mount fade-up */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* Altair container styled as a card */
  div[data-testid="stAltairChart"],
  div[data-testid="stVegaLiteChart"] {
    max-width: 1200px;
    width: 100% !important;
    margin: 16px auto;
    padding: 20px;
    border: 1px solid rgba(77,144,25,0.25);
    border-radius: 12px;
    background: rgba(255,255,255,0.92);
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: transform 220ms ease, box-shadow 220ms ease,
                border-color 220ms ease, background-color 220ms ease;
    animation: fadeUp 600ms ease both;
    box-sizing: border-box;
    overflow: hidden;
  }
  div[data-testid="stAltairChart"]:hover,
  div[data-testid="stVegaLiteChart"]:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    border-color: #4d9019;
    background-color: #ffffff;
  }

  /* Section title underline on hover */
  .section-title {
    text-align: center;
    font-weight: 600;
    position: relative;
    display: inline-block;
  }
  .section-title::after {
    content: "";
    position: absolute;
    left: 25%;
    right: 25%;
    bottom: -6px;
    height: 3px;
    background: #4d9019;
    transform: scaleX(0);
    transform-origin: 50% 50%;
    transition: transform 240ms ease;
  }
  .section-title:hover::after { transform: scaleX(1); }

  /* Selected chip (optional) */
  .selected-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(77,144,25,0.25);
    background: rgba(186,212,166,0.35);
    font-weight: 600;
    color: #2c5f10;
    margin: 6px 0 2px 0;
    animation: chipPulse 2200ms ease-in-out infinite;
  }
  @keyframes chipPulse {
    0%   { box-shadow: 0 0 0 0 rgba(77,144,25,0.20); }
    50%  { box-shadow: 0 0 0 8px rgba(77,144,25,0.00); }
    100% { box-shadow: 0 0 0 0 rgba(77,144,25,0.00); }
  }
  .chip-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }

  /* Description card beneath charts */
  .desc-card {
    max-width: 1200px;
    width: 100%;
    margin: 16px auto 24px auto;
    padding: 18px 20px;
    border: 1px solid rgba(77,144,25,0.25);
    border-radius: 12px;
    background: rgba(255,255,255,0.92);
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
    animation: fadeUp 600ms ease both;
    box-sizing: border-box;
  }
  .desc-card:hover {
    transform: translateY(-3px) scale(1.005);
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    border-color: #4d9019;
  }
  .desc-heading {
    margin: 0 0 6px 0;
    color: #4d9019;
    transition: color 200ms ease;
  }
  .desc-card:hover .desc-heading {
    color: #2e6b0f; /* darker green on hover */
  }
  .desc-list {
    margin-top: 6px;
  }
</style>
""", unsafe_allow_html=True)

# Page title
st.markdown(
    f"""
    <div style="text-align:center; margin-top: 36px;">
      <h2 style="color:{TITLE_COLOR}; margin-bottom: 8px;">Industry Multiples</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# Data for charts
def df_anchors():
    data = [
        ["EV / EBITDA",                5.61, 3.77, 9.38],
        ["EV / Revenue",               2.57, 0.96, 3.53],
        ["Net Debt / EBITDA",          3.23, 3.00, 6.23],
        ["EBITDA / Interest Expense",  4.11, 8.98, 13.09],
        ["Interest Coverage Ratio",    2.19, 0.83, 3.02],
    ]
    return pd.DataFrame(data, columns=["Metric", "Low", "Difference", "High"])

def df_direct_comps():
    data = [
        ["EV / EBITDA",                2.04, 13.77, 15.81],
        ["EV / Revenue",               0.64, 5.97, 6.61],
        ["Net Debt / EBITDA",          0.27, 16.47, 16.74],
        ["Total Debt / Total Capital", 0.09, 0.75, 0.84],
        ["EBITDA / Interest Expense",  1.71, 5.68, 7.39],
        ["Price to Book Value",        0.12, 3.28, 3.40],
    ]
    return pd.DataFrame(data, columns=["Metric", "Low", "Difference", "High"])

# Marker data (company -> metric values)
ANCHOR_COMPANY_VALUES = {
    "NextEra Energy": {
        "EV / EBITDA": 7.70,
        "EV / Revenue": 3.94,
        "Net Debt / EBITDA": 4.08,
        "EBITDA / Interest Expense": 8.87,
        "Interest Coverage Ratio": 2.50,
    },
    "Duke Energy": {
        "EV / EBITDA": 6.26,
        "EV / Revenue": 1.42,
        "Net Debt / EBITDA": 5.89,
        "EBITDA / Interest Expense": 4.36,
        "Interest Coverage Ratio": 2.38,
    },
    "Southern Company": {
        "EV / EBITDA": 6.88,
        "EV / Revenue": 3.02,
        "Net Debt / EBITDA": 4.90,
        "EBITDA / Interest Expense": 4.96,
        "Interest Coverage Ratio": 2.54,
    },
    "NRG Energy": {
        "EV / EBITDA": 5.02,
        "EV / Revenue": 0.41,
        "Net Debt / EBITDA": 4.10,
        "EBITDA / Interest Expense": 4.55,
        "Interest Coverage Ratio": 3.05,
    },
    "Dominion Energy": {
        "EV / EBITDA": 6.60,
        "EV / Revenue": 3.17,
        "Net Debt / EBITDA": 5.54,
        "EBITDA / Interest Expense": 4.49,
        "Interest Coverage Ratio": 1.73,
    },
}

DIRECT_COMPANY_VALUES = {
    "Ormat Technologies": {
        "EV / EBITDA": 10.48,
        "EV / Revenue": 5.60,
        "Net Debt / EBITDA": 2.99,
        "Total Debt / Total Capital": 0.38,
        "EBITDA / Interest Expense": 4.17,
        "Price to Book Value": 1.96,
    },
    "AES Corporation": {
        "EV / EBITDA": 2.04,
        "EV / Revenue": 0.75,
        "Net Debt / EBITDA": 8.75,
        "Total Debt / Total Capital": 0.81,
        "EBITDA / Interest Expense": 2.33,
        "Price to Book Value": 0.26,
    },
    "Ameresco Inc": {
        "EV / EBITDA": 10.93,
        "EV / Revenue": 1.18,
        "Net Debt / EBITDA": 6.99,
        "Total Debt / Total Capital": 0.58,
        "EBITDA / Interest Expense": 4.36,
        "Price to Book Value": 2.12,
    },
    "Vistra Corporation": {
        "EV / EBITDA": 7.61,
        "EV / Revenue": 1.42,
        "Net Debt / EBITDA": 7.14,
        "Total Debt / Total Capital": 0.73,
        "EBITDA / Interest Expense": 5.14,
        "Price to Book Value": 0.42,
    },
    "Public Service Enterprise Group": {
        "EV / EBITDA": 9.50,
        "EV / Revenue": 3.31,
        "Net Debt / EBITDA": 0.41,
        "Total Debt / Total Capital": 0.10,
        "EBITDA / Interest Expense": 5.21,
        "Price to Book Value": 0.23,
    },
}

# Marker colors per company
ANCHOR_MARKER_COLORS = {
    "NextEra Energy": "#ed582b",
    "Duke Energy": "#edb02b",
    "Southern Company": "#a49df5",
    "NRG Energy": "#2be3ed",
    "Dominion Energy": "#ed2bda",
}
DIRECT_MARKER_COLORS = {
    "Ormat Technologies": "#ed582b",
    "AES Corporation": "#edb02b",
    "Ameresco Inc": "#a49df5",
    "Vistra Corporation": "#2be3ed",
    "Public Service Enterprise Group": "#ed2bda",
}

# Helpers
def company_points_for_view(company_name: str, metrics: pd.Series, values_map: dict) -> pd.DataFrame:
    if not company_name or company_name == "None":
        return pd.DataFrame(columns=["Metric", "Value", "Company"])
    m = values_map.get(company_name, {})
    rows = []
    for metric in metrics:
        if metric in m and m[metric] is not None:
            rows.append((metric, float(m[metric]), company_name))
    return pd.DataFrame(rows, columns=["Metric", "Value", "Company"])

def render_range_chart(
    df: pd.DataFrame,
    x_title: str,
    company_points: pd.DataFrame | None = None,
    company_color: str | None = None,
):
    df = df.copy()
    df["Median"] = (df["Low"] + df["High"]) / 2

    base = alt.Chart(df).encode(
        y=alt.Y(
            "Metric:N",
            sort="-x",
            title="",
            axis=alt.Axis(
                labelFontSize=14,
                labelFontWeight="bold",
                labelColor=AXIS_LABEL_COLOR,
                ticks=True,
                tickColor=TICK_COLOR,
            ),
        ),
        tooltip=[
            alt.Tooltip("Metric:N"),
            alt.Tooltip("Low:Q", format=".2f"),
            alt.Tooltip("High:Q", format=".2f"),
            alt.Tooltip("Median:Q", format=".2f"),
        ],
    )

    range_rule = base.mark_rule(stroke=ACCENT, strokeWidth=8, opacity=0.95).encode(
        x=alt.X(
            "Low:Q",
            title=x_title,
            axis=alt.Axis(
                labelFontSize=14,
                labelFontWeight="bold",
                labelColor=AXIS_LABEL_COLOR,
                titleColor=AXIS_TITLE_COLOR,
                grid=True,
                gridColor=GRID_COLOR,
                tickColor=TICK_COLOR,
            ),
        ),
        x2="High:Q",
    )

    low_tick = base.mark_tick(color=TICK_COLOR, thickness=2, size=14).encode(x="Low:Q")
    high_tick = base.mark_tick(color=TICK_COLOR, thickness=2, size=14).encode(x="High:Q")
    median_tick = base.mark_point(color=MEDIAN_COLOR, filled=True, size=90).encode(x="Median:Q")

    layers = range_rule + low_tick + high_tick + median_tick

    # Optional company overlay with a subtle "glow ring"
    if company_points is not None and not company_points.empty:
        marker_color = company_color or "#d97706"
        glow = alt.Chart(company_points).mark_point(
            filled=True, size=400, opacity=0.18, color=marker_color
        ).encode(
            y=alt.Y("Metric:N", sort=df["Metric"].tolist(), title=""),
            x=alt.X("Value:Q"),
        )
        dot = alt.Chart(company_points).mark_point(
            filled=True, size=140, color=marker_color
        ).encode(
            y=alt.Y("Metric:N", sort=df["Metric"].tolist(), title=""),
            x=alt.X("Value:Q"),
            tooltip=[
                alt.Tooltip("Company:N"),
                alt.Tooltip("Metric:N"),
                alt.Tooltip("Value:Q", format=".2f"),
            ],
        )
        layers = layers + glow + dot

    chart = layers.properties(width=1200, height=420)
    st.altair_chart(chart, use_container_width=True)

def render_description_card(include_price_to_book: bool):
    parts = []
    parts.append("<div class='desc-card'>")
    parts.append("<h4 class='desc-heading'>Profitability</h4>")
    parts.append(
        "<ul class='desc-list'>"
        "<li><b>EV / EBITDA</b> - measures a company's total value relative to its operating cash flow</li>"
        "<li><b>EV / Revenue</b> - measures a company's total value relative to its total sales</li>"
        "</ul>"
    )
    parts.append("<h4 class='desc-heading'>Leverage</h4>")
    parts.append(
        "<ul class='desc-list'>"
        "<li><b>Net Debt / EBITDA</b> - measures a company's debt burden relative to its operating cash flow; shows how many years of operating cash flow would be needed to pay off all of a company's net debt</li>"
        "<li><b>Total Debt / Total Capital</b> - shows how much of a company's total funding (debt and equity) is comprised of debt</li>"
        "</ul>"
    )
    parts.append("<h4 class='desc-heading'>Coverage</h4>")
    parts.append(
        "<ul class='desc-list'>"
        "<li><b>EBITDA / Interest Expense</b> - shows how many times a company's operating earnings can cover its annual interest payments</li>"
        "<li><b>Interest Coverage Ratio</b> - measures a company's ability to cover its interest payments with its operating earnings</li>"
        "</ul>"
    )
    if include_price_to_book:
        parts.append(
            "<ul class='desc-list'>"
            "<li><b>Price to Book Value</b> - shows how the market values a company relative to its net assets</li>"
            "</ul>"
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)

# Top control: choose view
left, mid, right = st.columns([0.22, 0.56, 0.22])
with left:
    view = st.selectbox("Select section", ["Industry Anchors", "Direct Comparables"], index=0)

# Render per view
if view == "Industry Anchors":
    st.write(
        "This chart displays the valuation multiples for our 'industry anchor' peer group. "
        "These companies are the largest and most diversified players in the renewable energy sector. "
        "By analysing their multiples, you establish a market ceiling for valuation and gain critical context on how "
        "the most successful and scaled companies in the industry are valued."
    )

    # Company selector (anchors)
    pick1, pick2, pick3 = st.columns([0.3, 0.4, 0.3])
    with pick2:
        selected_anchor = st.selectbox(
            "Highlight company (optional)",
            ["None"] + list(ANCHOR_COMPANY_VALUES.keys()),
            index=0
        )
        if selected_anchor != "None":
            color = ANCHOR_MARKER_COLORS.get(selected_anchor, "#4d9019")
            st.markdown(
                f"<div class='selected-chip'><span class='chip-dot' style='background:{color}'></span> {selected_anchor}</div>",
                unsafe_allow_html=True
            )

    c1, c2, c3 = st.columns([0.5, 4, 0.5])
    with c2:
        st.markdown(
            "<div style='text-align:center;'><h3 class='section-title'>Industry Anchors Valuation Ranges</h3></div>",
            unsafe_allow_html=True
        )
        anchors_df = df_anchors()
        overlay_df = company_points_for_view(selected_anchor, anchors_df["Metric"], ANCHOR_COMPANY_VALUES)
        anchor_color = ANCHOR_MARKER_COLORS.get(selected_anchor) if selected_anchor != "None" else None
        render_range_chart(anchors_df, "Range (Low to High)", company_points=overlay_df, company_color=anchor_color)
        render_description_card(include_price_to_book=False)

else:
    st.write(
        "To get a precise sense of a company's market value, you need to compare it to its true peers. "
        "This chart helps you do just that. It displays the key multiples for companies that are similar in size and "
        "business model, giving you a focused and reliable valuation range. Use this data to quickly see how a company "
        "stacks up against its closest competitors and to identify potential valuation gaps."
    )

    # Company selector (direct comps)
    pick1, pick2, pick3 = st.columns([0.3, 0.4, 0.3])
    with pick2:
        selected_direct = st.selectbox(
            "Highlight company (optional)",
            ["None"] + list(DIRECT_COMPANY_VALUES.keys()),
            index=0
        )
        if selected_direct != "None":
            color = DIRECT_MARKER_COLORS.get(selected_direct, "#4d9019")
            st.markdown(
                f"<div class='selected-chip'><span class='chip-dot' style='background:{color}'></span> {selected_direct}</div>",
                unsafe_allow_html=True
            )

    c1, c2, c3 = st.columns([0.5, 4, 0.5])
    with c2:
        st.markdown(
            "<div style='text-align:center;'><h3 class='section-title'>Direct Comparables Valuation Ranges</h3></div>",
            unsafe_allow_html=True
        )
        comps_df = df_direct_comps()
        overlay_df = company_points_for_view(selected_direct, comps_df["Metric"], DIRECT_COMPANY_VALUES)
        direct_color = DIRECT_MARKER_COLORS.get(selected_direct) if selected_direct != "None" else None
        render_range_chart(comps_df, "Range (Low to High)", company_points=overlay_df, company_color=direct_color)
        render_description_card(include_price_to_book=True)
