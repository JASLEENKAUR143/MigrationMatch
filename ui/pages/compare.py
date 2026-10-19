"""Search & Compare Page — Head-to-Head & Multi-City Comparison."""
import textwrap
import pandas as pd
import streamlit as st

from model.recommendation_model import get_city_profile
from ui.charts import radar_compare
from ui.components import top_header_bar
from ui.helpers import cost_of_living_label, format_inr, get_city_image


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("Search and Compare")

    st.markdown(
        textwrap.dedent(
            """
<div style="margin-bottom: 1.25rem;">
<div style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.025em;">
⚖️ Search & Compare Cities Side-by-Side
</div>
<div style="font-size: 0.9rem; color: var(--text-secondary);">
Evaluate destination cities across multiple financial, employment, and socio-economic dimensions.
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    all_cities = sorted(df["City"].unique().tolist())
    cmp_cities = st.session_state.get("compare_cities", ["Pune", "Bengaluru"])

    city_a_default = cmp_cities[0] if len(cmp_cities) > 0 and cmp_cities[0] in all_cities else "Pune"
    city_b_default = cmp_cities[1] if len(cmp_cities) > 1 and cmp_cities[1] in all_cities else "Bengaluru"

    col_sel_a, col_swap, col_sel_b = st.columns([2, 0.5, 2])
    with col_sel_a:
        city_a = st.selectbox("🏙️ CITY A (BASELINE)", all_cities, index=all_cities.index(city_a_default))
    with col_swap:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("🔄", key="swap_cities_btn", help="Swap Baseline and Comparison"):
            st.session_state.compare_cities = [city_b_default, city_a_default]
            st.rerun()
    with col_sel_b:
        city_b = st.selectbox("🏙️ CITY B (COMPARISON)", all_cities, index=all_cities.index(city_b_default))

    prof_a = get_city_profile(df, city_a)
    prof_b = get_city_profile(df, city_b)

    if prof_a.empty or prof_b.empty:
        st.warning("City profile data could not be retrieved.")
        return

    # Head-to-Head Cards
    col_card_a, col_card_b = st.columns(2)

    with col_card_a:
        img_a = get_city_image(city_a)
        st.markdown(
            textwrap.dedent(
                f"""
<div class="city-explorer-card" style="margin-bottom: 1.25rem;">
<div class="city-card-header-img" style="background-image: url('{img_a}'); height: 160px;">
<span class="score-pill score-pill-emerald" style="background: var(--card-bg); border: 1px solid var(--border-color); font-size: 0.75rem; z-index: 2;">
✨ 88% Match
</span>
<div class="city-card-city-name" style="font-size: 1.35rem;">{city_a}</div>
<div class="city-card-location">📍 Baseline Destination</div>
</div>
<div class="city-card-body" style="gap: 12px;">
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">💵 AVG MONTHLY SALARY</span><br>
<strong style="font-size: 1.2rem;">{format_inr(prof_a['Average_Salary'])}</strong>
</div>
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">🏠 AVG MONTHLY RENT (1BHK)</span><br>
<strong style="font-size: 1.2rem;">{format_inr(prof_a['Average_1BHK_Rent'])}</strong>
</div>
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">📊 COST OF LIVING INDEX</span><br>
<strong style="color: #F59E0B;">● {cost_of_living_label(prof_a['Estimated_Monthly_Expenses'])}</strong>
</div>
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">🏥 HEALTHCARE ACCESS</span><br>
<strong style="color: #0D7A5F;">Rating: {prof_a['Healthcare_Score']:.0f}/100</strong>
</div>
<div>
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">🚌 TRANSPORTATION RELIABILITY</span><br>
<span style="font-size: 0.82rem; color: var(--text-secondary);">Developing transit corridors, reliable city bus network, moderate congestion.</span>
</div>
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    with col_card_b:
        img_b = get_city_image(city_b)
        sal_delta = prof_b["Average_Salary"] - prof_a["Average_Salary"]
        sal_arrow = f"<span style='color:#0D7A5F; font-size: 0.9rem;'>↑ +{format_inr(sal_delta)}</span>" if sal_delta >= 0 else f"<span style='color:#EF4444; font-size: 0.9rem;'>↓ {format_inr(sal_delta)}</span>"

        rent_delta = prof_b["Average_1BHK_Rent"] - prof_a["Average_1BHK_Rent"]
        rent_arrow = f"<span style='color:#EF4444; font-size: 0.9rem;'>↑ +{format_inr(rent_delta)}</span>" if rent_delta > 0 else f"<span style='color:#0D7A5F; font-size: 0.9rem;'>↓ {format_inr(rent_delta)}</span>"

        st.markdown(
            textwrap.dedent(
                f"""
<div class="city-explorer-card" style="margin-bottom: 1.25rem;">
<div class="city-card-header-img" style="background-image: url('{img_b}'); height: 160px;">
<span class="score-pill score-pill-emerald" style="background: var(--card-bg); border: 1px solid var(--border-color); font-size: 0.75rem; z-index: 2;">
✨ 82% Match
</span>
<div class="city-card-city-name" style="font-size: 1.35rem;">{city_b}</div>
<div class="city-card-location">📍 Comparison Destination</div>
</div>
<div class="city-card-body" style="gap: 12px;">
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">💵 AVG MONTHLY SALARY</span><br>
<strong style="font-size: 1.2rem;">{format_inr(prof_b['Average_Salary'])} {sal_arrow}</strong>
</div>
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">🏠 AVG MONTHLY RENT (1BHK)</span><br>
<strong style="font-size: 1.2rem;">{format_inr(prof_b['Average_1BHK_Rent'])} {rent_arrow}</strong>
</div>
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">📊 COST OF LIVING INDEX</span><br>
<strong style="color: #EF4444;">● {cost_of_living_label(prof_b['Estimated_Monthly_Expenses'])}</strong>
</div>
<div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">🏥 HEALTHCARE ACCESS</span><br>
<strong style="color: #0D7A5F;">Rating: {prof_b['Healthcare_Score']:.0f}/100</strong>
</div>
<div>
<span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">🚌 TRANSPORTATION RELIABILITY</span><br>
<span style="font-size: 0.82rem; color: var(--text-secondary);">Extensive transit network, metro connectivity, peak traffic delays.</span>
</div>
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    # Multi-City Radar & Comparison Matrix
    st.markdown("<br>", unsafe_allow_html=True)
    col_radar, col_matrix = st.columns([1, 1.4])

    with col_radar:
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.5rem;">
📡 Multi-Dimensional Radar Comparison
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )
        cmp_df = df[df["City"].isin([city_a, city_b])].groupby("City").mean(numeric_only=True).reset_index()
        st.plotly_chart(radar_compare(cmp_df, [city_a, city_b]), use_container_width=True)

    with col_matrix:
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem;">
📋 Comparative Metrics Matrix
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )
        matrix_data = {
            "Dimension": ["Average Salary", "Average 1BHK Rent", "Monthly Living Expenses", "Estimated Savings", "Job Demand Score", "Quality of Life Score", "Safety Score", "Affordability Score"],
            f"{city_a} (Baseline)": [
                format_inr(prof_a["Average_Salary"]),
                format_inr(prof_a["Average_1BHK_Rent"]),
                format_inr(prof_a["Estimated_Monthly_Expenses"]),
                format_inr(prof_a["Estimated_Monthly_Savings"]),
                f"{prof_a['Job_Demand_Score']:.0f}/100",
                f"{prof_a['Quality_of_Life_Score']:.0f}/100",
                f"{prof_a['Safety_Score']:.0f}/100",
                f"{prof_a['Affordability_Score']:.0f}/100",
            ],
            f"{city_b} (Comparison)": [
                format_inr(prof_b["Average_Salary"]),
                format_inr(prof_b["Average_1BHK_Rent"]),
                format_inr(prof_b["Estimated_Monthly_Expenses"]),
                format_inr(prof_b["Estimated_Monthly_Savings"]),
                f"{prof_b['Job_Demand_Score']:.0f}/100",
                f"{prof_b['Quality_of_Life_Score']:.0f}/100",
                f"{prof_b['Safety_Score']:.0f}/100",
                f"{prof_b['Affordability_Score']:.0f}/100",
            ],
        }
        st.dataframe(pd.DataFrame(matrix_data), use_container_width=True, hide_index=True)