"""Worker Recommendation Page — Professional & Classy."""
import textwrap
import pandas as pd
import streamlit as st

from ui.components import top_header_bar
from ui.helpers import format_inr, get_city_image, why_recommended
from ui.session import get_inputs, run_recommendation, update_inputs


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("Get Recommendations")

    st.markdown(
        textwrap.dedent(
            """
<div style="margin-bottom: 1.25rem;">
<div style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.025em;">
🎯 Find Your Next Optimal Destination
</div>
<div style="font-size: 0.9rem; color: var(--text-secondary);">
Input your professional profile, trade expertise, and budget to generate calibrated, explainable city recommendations.
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    inputs = get_inputs()
    skills_list = sorted(df["Skill"].unique().tolist())
    regions_list = ["All Regions", "North", "South", "East", "West", "Central"]

    col_form, col_results = st.columns([1, 1.6])

    with col_form:
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 1rem;">
⚙️ Recommendation Parameters
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        with st.form("recommendation_param_form"):
            selected_skill = st.selectbox(
                "💼 PRIMARY SKILL / TRADE",
                skills_list,
                index=skills_list.index(inputs.get("skill", "Electrician")) if inputs.get("skill") in skills_list else 0,
            )

            exp_years = st.slider("⏳ YEARS OF EXPERIENCE", min_value=0, max_value=15, value=int(inputs.get("experience_years", 3)))

            exp_salary = st.number_input(
                "💵 EXPECTED MONTHLY SALARY (₹)",
                min_value=5000,
                max_value=100000,
                value=int(inputs.get("expected_salary", 25000)),
                step=1000,
            )

            target_rent = st.number_input(
                "🏠 TARGET MONTHLY RENT BUDGET (₹)",
                min_value=1000,
                max_value=50000,
                value=int(inputs.get("max_rent", 8000)),
                step=500,
            )

            family_size = st.number_input("👨‍👩‍👧 FAMILY MEMBERS", min_value=1, max_value=10, value=int(inputs.get("family_size", 3)))

            selected_region = st.selectbox("📍 PREFERRED REGION", regions_list, index=0)

            submitted = st.form_submit_button("🚀 Generate Recommendations", type="primary", use_container_width=True)

            if submitted:
                reg_val = None if selected_region == "All Regions" else selected_region
                update_inputs(
                    skill=selected_skill,
                    experience_years=exp_years,
                    expected_salary=exp_salary,
                    max_rent=target_rent,
                    family_size=family_size,
                    region_pref=reg_val,
                )
                run_recommendation(df_feat, top_n=10)
                st.success("✨ Recommendations successfully calibrated and updated!")
                st.rerun()

        # Engine Status Card
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="background: var(--subcard-bg); border: 1px solid var(--border-color); padding: 1rem; font-size: 0.8rem; color: var(--text-secondary); margin-top: 1rem;">
<div style="font-weight: 700; color: #0D7A5F; margin-bottom: 0.25rem;">⚡ ENGINE STATUS: ACTIVE & OPTIMIZED</div>
The multi-criteria decision algorithm evaluates employment availability, living expense index, and infrastructure metrics across 45+ cities.
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    with col_results:
        results = st.session_state.get("last_results")
        if results is None or results.empty:
            results = run_recommendation(df_feat, top_n=10)

        st.markdown(
            textwrap.dedent(
                f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
<span style="font-size: 1.15rem; font-weight: 800;">🌟 Top Destination Matches</span>
<span style="font-size: 0.8rem; color: var(--text-secondary);">Showing top {min(len(results), 4)} optimal results</span>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        top4 = results.head(4)
        c1, c2 = st.columns(2)

        for i, (_, row) in enumerate(top4.iterrows()):
            target_col = c1 if i % 2 == 0 else c2
            city_name = row["City"]
            state_name = row["State"]
            score = row["Match_Score"]
            img_url = get_city_image(city_name)

            with target_col:
                st.markdown(
                    textwrap.dedent(
                        f"""
<div class="city-explorer-card" style="margin-bottom: 1rem;">
<div class="city-card-header-img" style="background-image: url('{img_url}');">
<div></div>
<span class="score-pill score-pill-emerald" style="background: var(--card-bg); border: 1px solid var(--border-color); font-size: 0.75rem; z-index: 2;">
✨ {score:.0f}% Match
</span>
<div class="city-card-city-name">{city_name}</div>
<div class="city-card-location">{state_name}</div>
</div>
<div class="city-card-body">
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.78rem; margin-bottom: 0.6rem;">
<div style="background: var(--subcard-bg); padding: 0.4rem 0.6rem; border-radius: 6px; border: 1px solid var(--border-color);">
<span style="color: var(--text-secondary);">💵 EST. SALARY</span><br>
<strong style="font-size: 0.9rem;">{format_inr(row['Average_Salary'])}</strong>
</div>
<div style="background: var(--subcard-bg); padding: 0.4rem 0.6rem; border-radius: 6px; border: 1px solid var(--border-color);">
<span style="color: var(--text-secondary);">🏠 AVG. RENT</span><br>
<strong style="font-size: 0.9rem;">{format_inr(row['Average_1BHK_Rent'])}</strong>
</div>
</div>
<div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.6rem;">
💡 {why_recommended(row)}
</div>
</div>
</div>
"""
                    ),
                    unsafe_allow_html=True,
                )

                if st.button(f"🔍 Compare {city_name} →", key=f"rec_cmp_{city_name}", use_container_width=True):
                    st.session_state.compare_cities = [city_name, "Bengaluru"]
                    st.session_state.nav_page = "Search and Compare"
                    st.rerun()
