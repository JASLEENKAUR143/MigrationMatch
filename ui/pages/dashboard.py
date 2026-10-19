"""Main Overview Dashboard — Professional & Classy."""
import textwrap
import pandas as pd
import streamlit as st

from ui.charts import city_comparison_overview_chart
from ui.components import (
    featured_recommendation_card,
    page_header,
    recommendation_card_detailed,
    section_title,
    stat_kpi_cards,
    top_header_bar,
)
from ui.helpers import format_inr
from ui.session import get_inputs, run_recommendation


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("Dashboard")

    user = st.session_state.get("user", {"name": "Jasleen Kaur"})
    user_name = user.get("name", "Jasleen Kaur")

    st.markdown(
        """
        <div class="dashboard-hero">
            <div class="dashboard-hero-copy">
                <div class="dashboard-eyebrow">✦ 2026 RELOCATION INTELLIGENCE</div>
                <h1>Move with confidence.<br><span>Match your skills to opportunity.</span></h1>
                <p>Explore India's strongest cities for work, savings, safety, and quality of life — powered by explainable data science.</p>
                <div class="dashboard-hero-pills">
                    <span>🤖 ML-assisted matching</span>
                    <span>📊 45 cities analysed</span>
                    <span>🔒 Your data stays local</span>
                </div>
            </div>
            <div class="dashboard-hero-art" aria-hidden="true">
                <div class="hero-orbit hero-orbit-one"></div>
                <div class="hero-orbit hero-orbit-two"></div>
                <div class="hero-pin">📍</div>
                <div class="hero-city-label hero-city-one">Pune</div>
                <div class="hero-city-label hero-city-two">Bengaluru</div>
                <div class="hero-city-label hero-city-three">Surat</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Header Greeting
    st.markdown(
        textwrap.dedent(
            f"""
<div style="margin-bottom: 1.25rem;">
<div style="font-size: 1.75rem; font-weight: 800; letter-spacing: -0.03em;">
Welcome back, {user_name}
</div>
<div style="font-size: 0.92rem; color: var(--text-secondary);">
Discover optimal Indian cities for your trade skills, career progression, income, and lifestyle preferences.
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    # 4 Stat Counters
    stat_kpi_cards(df)
    st.markdown("<br>", unsafe_allow_html=True)

    # Ensure recommendations are computed
    if st.session_state.get("last_results") is None:
        run_recommendation(df_feat, top_n=10)
    results = st.session_state.get("last_results")

    # Layout: Left column (Top 5 Recommended) vs Right column (Profile & Comparison Chart)
    col_left, col_right = st.columns([1.1, 1.3])

    with col_left:
        st.markdown(
            textwrap.dedent(
                """
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
<span style="font-size: 1.15rem; font-weight: 800;">Top 5 Recommended Destinations</span>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        if results is not None and not results.empty:
            for idx, (_, row) in enumerate(results.head(5).iterrows()):
                recommendation_card_detailed(row, rank=idx + 1)
        else:
            st.info("No recommendations found. Please adjust your search criteria.")

        if st.button("Explore All Cities in City Explorer →", key="view_all_rec_btn", use_container_width=True):
            st.session_state.nav_page = "City Explorer"
            st.rerun()

    with col_right:
        # Profile Summary Card
        inputs = get_inputs()
        st.markdown(
            textwrap.dedent(
                f"""
<div class="mm-card" style="padding: 1.25rem; margin-bottom: 1rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
<span style="font-size: 1.05rem; font-weight: 800;">Your Profile Summary</span>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.82rem;">
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border: 1px solid var(--border-color);">
<span style="color: var(--text-secondary);">Skill / Occupation</span><br>
<strong style="font-size: 0.95rem;">{inputs.get('skill', 'Electrician')}</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border: 1px solid var(--border-color);">
<span style="color: var(--text-secondary);">Target Rent Budget</span><br>
<strong style="font-size: 0.95rem;">{format_inr(inputs.get('max_rent', 8000))}</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border: 1px solid var(--border-color);">
<span style="color: var(--text-secondary);">Experience Level</span><br>
<strong style="font-size: 0.95rem;">{inputs.get('experience_years', 3)} Years</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border: 1px solid var(--border-color);">
<span style="color: var(--text-secondary);">Family Size</span><br>
<strong style="font-size: 0.95rem;">{inputs.get('family_size', 3)} Members</strong>
</div>
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        # City Comparison Overview Chart
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.5rem;">
Top 5 Cities Overview Comparison
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )
        if results is not None and not results.empty:
            st.plotly_chart(city_comparison_overview_chart(results), use_container_width=True)

    # Featured Recommendation Banner
    st.markdown("<br>", unsafe_allow_html=True)
    if results is not None and not results.empty:
        featured_recommendation_card(results.iloc[0])

    # "Why These Cities?" Weight Breakdown Strip
    st.markdown(
        textwrap.dedent(
            """
<div class="mm-card" style="margin-top: 1rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.35rem;">Why These Cities?</div>
<div style="font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 1rem;">
Scores are calculated using multi-criteria weighted scoring across employment availability, salary matching, affordability, and living conditions.
</div>
<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; font-size: 0.8rem;">
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border-top: 3px solid #0D7A5F;">
<span style="color: var(--text-secondary);">Job Demand</span><br>
<strong>30% Weight</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border-top: 3px solid #3B82F6;">
<span style="color: var(--text-secondary);">Salary Match</span><br>
<strong>25% Weight</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border-top: 3px solid #F59E0B;">
<span style="color: var(--text-secondary);">Rent Affordability</span><br>
<strong>20% Weight</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border-top: 3px solid #8B5CF6;">
<span style="color: var(--text-secondary);">Cost of Living</span><br>
<strong>15% Weight</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.65rem 0.85rem; border-radius: 8px; border-top: 3px solid #10B981;">
<span style="color: var(--text-secondary);">Savings Potential</span><br>
<strong>10% Weight</strong>
</div>
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    # Bottom Actions
    btn_c1, btn_c2 = st.columns(2)
    with btn_c1:
        if st.button("Generate Custom Recommendations", type="primary", use_container_width=True):
            st.session_state.nav_page = "Get Recommendations"
            st.rerun()
    with btn_c2:
        if st.button("Compare Cities Side-by-Side", use_container_width=True):
            st.session_state.nav_page = "Search and Compare"
            st.rerun()