"""City Explorer Page — Industrial Hubs across India matching Image 2 (City Explorer)."""
import textwrap
import pandas as pd
import streamlit as st

from ui.components import city_explorer_card, top_header_bar


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("City Explorer")

    st.markdown(
        textwrap.dedent(
            """
<div style="margin-bottom: 1.25rem;">
<div style="font-size: 1.65rem; font-weight: 800; letter-spacing: -0.025em;">
🏙️ City Explorer & Industrial Hubs
</div>
<div style="font-size: 0.9rem; color: var(--text-secondary);">
Discover emerging industrial hubs across India. Filter by region and sector to identify optimal migration destinations.
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    # Search and Filter Strip
    col_search, col_region, col_industry = st.columns([2, 2.2, 1.8])

    with col_search:
        search_query = st.text_input(
            "Filter cities by name or state:",
            value=st.session_state.get("city_search_query", ""),
            placeholder="🔍 Type city or state name...",
            label_visibility="collapsed",
            key="city_explorer_search",
        )

    with col_region:
        region_options = ["All", "North", "South", "West", "East", "Central"]
        selected_region = st.radio(
            "Region Filter",
            region_options,
            horizontal=True,
            label_visibility="collapsed",
        )

    with col_industry:
        skills = ["All Sectors"] + sorted(df["Skill"].unique().tolist())
        selected_sector = st.selectbox("Industry / Sector", skills, label_visibility="collapsed")

    # City Aggregation
    agg_df = df.groupby(["City", "State", "Region"]).agg({
        "Job_Demand_Score": "mean",
        "Average_Salary": "mean",
        "Average_1BHK_Rent": "mean",
        "Estimated_Monthly_Expenses": "mean",
        "Job_Availability": "sum",
        "Quality_of_Life_Score": "mean",
    }).reset_index()

    # Filtering Logic
    if search_query:
        agg_df = agg_df[
            agg_df["City"].str.contains(search_query, case=False)
            | agg_df["State"].str.contains(search_query, case=False)
        ]

    if selected_region != "All":
        agg_df = agg_df[agg_df["Region"].str.lower() == selected_region.lower()]

    if selected_sector != "All Sectors":
        sector_cities = df[df["Skill"] == selected_sector]["City"].unique()
        agg_df = agg_df[agg_df["City"].isin(sector_cities)]

    st.markdown(
        textwrap.dedent(
            f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0 0.75rem 0;">
<span style="font-weight: 700; color: var(--text-secondary); font-size: 0.85rem;">📍 SHOWING {len(agg_df)} INDUSTRIAL & ECONOMIC HUBS</span>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    # Render Grid (3 columns)
    cols = st.columns(3)
    for i, (_, row) in enumerate(agg_df.iterrows()):
        with cols[i % 3]:
            city_explorer_card(row)
            if st.button(f"🔍 View Hub Data: {row['City']} →", key=f"hub_{row['City']}_{i}", use_container_width=True):
                st.session_state.compare_cities = [row["City"], "Bengaluru"]
                st.session_state.nav_page = "Search and Compare"
                st.rerun()
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
