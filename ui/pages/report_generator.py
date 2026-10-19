"""Report Generator Page — Live formatted preview & download matching Image 1 (Screen 7)."""
import textwrap
import pandas as pd
import streamlit as st

from ui.components import top_header_bar
from ui.helpers import format_inr
from ui.session import get_inputs, run_recommendation


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("Report Generator")

    st.markdown(
        textwrap.dedent(
            """
<div style="margin-bottom: 1.25rem;">
<div style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.025em;">
Relocation Intelligence Report Generator
</div>
<div style="font-size: 0.9rem; color: #64748B;">
Generate and export structured relocation intelligence reports with explainable scoring and financial breakdowns.
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    inputs = get_inputs()
    results = st.session_state.get("last_results")
    if results is None or results.empty:
        results = run_recommendation(df_feat, top_n=5)

    skill_val = inputs.get("skill", "Electrician")
    exp_val = inputs.get("experience_years", 3)
    sal_val = format_inr(inputs.get("expected_salary", 25000))
    rent_val = format_inr(inputs.get("max_rent", 8000))
    fam_val = inputs.get("family_size", 3)

    col_config, col_preview = st.columns([1, 1.6])

    with col_config:
        st.markdown(
            textwrap.dedent(
                f"""
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem;">
Worker Profile Summary
</div>
<div style="font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-bottom: 0.5rem;">
<strong style="color:var(--text-color, #0F172A);">Skill:</strong> {skill_val}<br>
<strong style="color:var(--text-color, #0F172A);">Experience:</strong> {exp_val} Years<br>
<strong style="color:var(--text-color, #0F172A);">Expected Salary:</strong> {sal_val}<br>
<strong style="color:var(--text-color, #0F172A);">Target Rent:</strong> {rent_val}<br>
<strong style="color:var(--text-color, #0F172A);">Family Size:</strong> {fam_val} Members
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.5rem;">
Include in Report
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        st.checkbox("Top 5 Recommended Cities & Scores", value=True)
        st.checkbox("Monthly Savings Potential Analysis", value=True)
        st.checkbox("Explainability Rationale & Key Reasons", value=True)
        st.checkbox("City Comparison Matrix Table", value=True)
        st.checkbox("Socio-Economic Charts & Insights", value=True)

        st.markdown("<br>", unsafe_allow_html=True)
        report_csv = results.head(5).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Data Report (CSV)",
            data=report_csv,
            file_name=f"MigrationMatch_Report_{skill_val}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )

    with col_preview:
        st.markdown(
            textwrap.dedent(
                """
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.5rem;">
Report Document Preview
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        top_city = results.iloc[0]["City"] if not results.empty else "Varanasi"
        top_score = results.iloc[0]["Match_Score"] if not results.empty else 98.0

        st.markdown("## 📄 MigrationMatch Intelligence Report")
        report_head, report_meta = st.columns([2.2, 1])
        with report_head:
            st.caption("DECISION SUPPORT SYSTEM")
        with report_meta:
            st.caption(f"Target Skill: **{skill_val}**")
            st.caption(f"Profile ID: **MM-{exp_val}Y-2025**")
        st.info(
            f"**Executive Summary:** Based on the multi-criteria evaluation of 45+ cities, "
            f"**{top_city}** is ranked as the #1 optimal destination with a "
            f"Migration Match Score of **{top_score:.1f}/100**."
        )
        st.markdown("**Top 5 Ranked Destinations:**")

        # Show Table
        st.dataframe(
            results.head(5)[["Rank", "City", "State", "Match_Score", "Average_Salary", "Average_1BHK_Rent", "Estimated_Monthly_Savings"]].rename(
                columns={
                    "Match_Score": "Migration Score",
                    "Average_Salary": "Salary (₹)",
                    "Average_1BHK_Rent": "Rent (₹)",
                    "Estimated_Monthly_Savings": "Est. Savings (₹)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
