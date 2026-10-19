"""Market Analysis Page — Real-time insights and economic analytics."""
import textwrap
import pandas as pd
import streamlit as st

from ui.charts import (
    correlation_heatmap,
    cost_breakdown_donut,
    regional_salary_trends_chart,
    rental_fluctuation_line_chart,
    top_skills_demand_chart,
    vacancies_by_skill_chart,
)
from ui.components import top_header_bar
from ui.helpers import format_inr
from ui.session import get_inputs


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("Market Analysis")

    inputs = get_inputs()
    current_skill = inputs.get("skill", "AC Technician")
    current_results = st.session_state.get("last_results")
    if current_results is not None and not current_results.empty:
        top_destination = str(current_results.iloc[0]["City"])
    else:
        skill_rows = df[df["Skill"] == current_skill]
        top_destination = (
            str(
                skill_rows.groupby("City")["Job_Demand_Score"]
                .mean()
                .sort_values(ascending=False)
                .index[0]
            )
            if not skill_rows.empty
            else str(df.groupby("City")["Job_Demand_Score"].mean().idxmax())
        )

    st.markdown(
        textwrap.dedent(
            f"""
<div style="margin-bottom: 1.25rem;">
<div style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.025em;">
📊 Market Analytics & Economic Trends
</div>
<div style="font-size: 0.9rem; color: var(--text-secondary);">
Real-time market insights, salary distributions, and living cost analytics for <strong>{current_skill}</strong>.
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    # Top 3 KPI Cards
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

    with col_kpi1:
        st.markdown(
            textwrap.dedent(
                f"""
<div class="stat-kpi-card">
<div class="stat-kpi-header">
<span style="font-size: 1.2rem;">📈</span>
<span class="score-pill score-pill-emerald" style="font-size: 0.72rem;">+14% YoY</span>
</div>
<div>
<div class="stat-kpi-label">DEMAND TREND</div>
<div class="stat-kpi-value" style="font-size: 1.3rem;">{current_skill}s</div>
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    with col_kpi2:
        skill_sal = df[df["Skill"] == current_skill]["Average_Salary"].mean()
        if pd.isna(skill_sal):
            skill_sal = 18450
        st.markdown(
            textwrap.dedent(
                f"""
<div class="stat-kpi-card">
<div class="stat-kpi-header">
<span style="font-size: 1.2rem;">💵</span>
<span class="score-pill" style="background: var(--subcard-bg); font-size: 0.72rem;">National Avg</span>
</div>
<div>
<div class="stat-kpi-label">AVG SALARY (MONTHLY)</div>
<div class="stat-kpi-value" style="font-size: 1.3rem;">{format_inr(skill_sal)}</div>
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    with col_kpi3:
        st.markdown(
            textwrap.dedent(
                """
<div class="stat-kpi-card">
<div class="stat-kpi-header">
<span style="font-size: 1.2rem;">🏙️</span>
<span class="score-pill score-pill-emerald" style="font-size: 0.72rem;">✨ Top Match</span>
</div>
<div>
<div class="stat-kpi-label">TOP DESTINATION</div>
<div class="stat-kpi-value" style="font-size: 1.3rem;">{top_destination}</div>
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Middle Charts: Regional Salary Trends vs Cost Breakdown Donut
    col_reg, col_donut = st.columns([1.6, 1])

    with col_reg:
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.25rem;">
📈 Regional Salary Trends
</div>
<div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
Average monthly compensation vs living cost by tier & region
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )
        st.plotly_chart(regional_salary_trends_chart(df), use_container_width=True)

    with col_donut:
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.25rem;">
🍩 Cost of Living Breakdown
</div>
<div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
Estimated living expense distribution in top destinations
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )
        st.plotly_chart(cost_breakdown_donut(), use_container_width=True)

    # Rental Price Fluctuations Line Chart
    st.markdown(
        textwrap.dedent(
            """
<div class="mm-card" style="padding: 1.25rem; margin-top: 1rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.25rem;">
🏠 Rental Price Fluctuations
</div>
<div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
12-month historical data for Top 3 Destinations (Varanasi, Lucknow, Patna)
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )
    st.plotly_chart(rental_fluctuation_line_chart(), use_container_width=True)

    # Additional Analytics: Skill Demand, Vacancies, and Correlation
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='mm-card'><strong style='font-size:0.95rem;'>🔥 Top Skills by Demand</strong></div>", unsafe_allow_html=True)
        st.plotly_chart(top_skills_demand_chart(df), use_container_width=True)

    with c2:
        st.markdown("<div class='mm-card'><strong style='font-size:0.95rem;'>💼 Vacancies by Skill</strong></div>", unsafe_allow_html=True)
        st.plotly_chart(vacancies_by_skill_chart(df), use_container_width=True)

    with c3:
        st.markdown("<div class='mm-card'><strong style='font-size:0.95rem;'>🔬 Correlation Matrix</strong></div>", unsafe_allow_html=True)
        st.plotly_chart(correlation_heatmap(df), use_container_width=True)