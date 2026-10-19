"""My Profile Page — User profile settings and preferences for Jasleen Kaur."""
import textwrap
import pandas as pd
import streamlit as st

from ui.components import top_header_bar
from ui.helpers import format_inr
from ui.session import get_inputs, update_inputs


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("My Profile")

    user = st.session_state.get("user", {"name": "Jasleen Kaur", "email": "jasleen@gmail.com"})
    inputs = get_inputs()

    st.markdown(
        textwrap.dedent(
            """
<div style="margin-bottom: 1.25rem;">
<div style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.025em;">
👤 User Profile & Relocation Preferences
</div>
<div style="font-size: 0.9rem; color: var(--text-secondary);">
Manage your personal details, professional background, financial targets, and destination preferences.
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    col_prof_card, col_form = st.columns([1, 1.8])

    with col_prof_card:
        user_name = user.get("name", "Jasleen Kaur")
        user_email = user.get("email", "jasleen@gmail.com")
        user_role = user.get("role", "Verified User")
        user_college = user.get("institution", "Punjab College of Technical Education, Ludhiana")
        user_course = user.get("course", "BCA (2024-2027)")

        st.markdown(
            f"### {user_name}\n\n✨ **{user_role}**  \n📧 {user_email}"
        )
        st.caption("🎓 Academic Program")
        st.markdown(f"**{user_course}**")
        st.caption("🏛️ Institution")
        st.markdown(f"**{user_college}**")

        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem; margin-top: 1rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
<span style="font-size: 0.88rem; font-weight: 700;">🌟 Profile Completeness</span>
<span class="score-pill score-pill-emerald">Verified</span>
</div>
<div style="font-size: 1.35rem; font-weight: 800; color: #0D7A5F;">95%</div>
<div style="height: 6px; background: rgba(100, 116, 139, 0.2); border-radius: 6px; overflow: hidden; margin-top: 4px;">
<div style="height: 100%; width: 95%; background: linear-gradient(90deg, #0D7A5F, #10B981);"></div>
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    with col_form:
        st.markdown(
            textwrap.dedent(
                """
<div class="mm-card" style="padding: 1.25rem;">
<div style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem;">
🛠️ Edit Relocation & Profile Preferences
</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

        skills = sorted(df["Skill"].unique().tolist())
        with st.form("profile_edit_form"):
            new_name = st.text_input("Full Name", value=user.get("name", "Jasleen Kaur"))
            new_skill = st.selectbox(
                "Primary Trade Skill / Profession",
                skills,
                index=skills.index(inputs.get("skill", "Electrician")) if inputs.get("skill") in skills else 0,
            )
            new_exp = st.slider("Years of Practical Experience", 0, 15, int(inputs.get("experience_years", 3)))
            new_sal = st.number_input("Expected Monthly Salary (₹)", 5000, 100000, int(inputs.get("expected_salary", 25000)), step=1000)
            new_rent = st.number_input("Max Monthly Rent Budget (₹)", 1000, 50000, int(inputs.get("max_rent", 8000)), step=500)
            new_fam = st.number_input("Family Size (Members)", 1, 10, int(inputs.get("family_size", 3)))

            if st.form_submit_button("💾 Save Profile Updates", type="primary", use_container_width=True):
                st.session_state.user["name"] = new_name
                update_inputs(
                    skill=new_skill,
                    experience_years=new_exp,
                    expected_salary=new_sal,
                    max_rent=new_rent,
                    family_size=new_fam,
                )
                st.session_state.last_results = None
                st.success("✅ Profile preferences successfully updated!")
                st.rerun()
