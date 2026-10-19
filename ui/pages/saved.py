"""Saved Results & Shortlist Page."""
import pandas as pd
import streamlit as st

from ui.components import top_header_bar
from ui.helpers import format_inr, get_city_image


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("Saved Results")

    st.markdown(
        """
<div style="margin-bottom: 1.25rem;">
    <div style="font-size: 1.65rem; font-weight: 800; color: #0F172A; letter-spacing: -0.025em;">
        Saved Relocation Shortlist 🔖
    </div>
    <div style="font-size: 0.9rem; color: #64748B;">
        Your bookmarked cities, preferred destinations, and saved relocation plans.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    saved_cities = st.session_state.get("saved_cities", ["Varanasi", "Bengaluru", "Pune", "Ahmedabad", "Coimbatore"])

    if not saved_cities:
        st.info("No saved cities in your shortlist yet. Explore cities to bookmark them!")
        return

    saved_df = df[df["City"].isin(saved_cities)].groupby(["City", "State", "Region"]).mean(numeric_only=True).reset_index()

    cols = st.columns(3)
    for i, (_, row) in enumerate(saved_df.iterrows()):
        city = row["City"]
        state = row["State"]
        img_url = get_city_image(city)

        with cols[i % 3]:
            st.markdown(
                f"""
<div class="city-explorer-card" style="margin-bottom: 1rem;">
    <div class="city-card-header-img" style="background-image: url('{img_url}');">
        <span class="score-pill score-pill-emerald" style="background: white; border: none; font-size: 0.72rem; z-index: 2;">
            🔖 Shortlisted
        </span>
        <div class="city-card-city-name">{city}</div>
        <div class="city-card-location">{state}</div>
    </div>
    <div class="city-card-body">
        <div style="font-size: 0.8rem; color: #475569; margin-bottom: 0.6rem;">
            Avg Salary: <strong>{format_inr(row['Average_Salary'])}</strong><br>
            Avg Rent: <strong>{format_inr(row['Average_1BHK_Rent'])}</strong><br>
            Est. Monthly Savings: <strong style="color:#0D7A5F;">{format_inr(row['Estimated_Monthly_Savings'])}</strong>
        </div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"Compare {city}", key=f"saved_cmp_{city}", use_container_width=True):
                    st.session_state.compare_cities = [city, "Bengaluru"]
                    st.session_state.nav_page = "Search & Compare"
                    st.rerun()
            with c2:
                if st.button(f"Remove", key=f"saved_rm_{city}", use_container_width=True):
                    st.session_state.saved_cities.remove(city)
                    st.toast(f"Removed {city} from saved shortlist.")
                    st.rerun()
