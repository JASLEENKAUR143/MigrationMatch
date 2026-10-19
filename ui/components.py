"""Reusable UI components for MigrationMatch — Classy Emerald & Slate Theme."""
import textwrap
import pandas as pd
import streamlit as st

from ui.helpers import (
    cost_of_living_label,
    format_inr,
    get_city_image,
    get_city_image_data_uri,
    get_city_sectors,
    job_demand_label,
    why_recommended,
)
from ui.styles import BRAND_EMERALD, BRAND_EMERALD_DARK, BRAND_EMERALD_LIGHT


def _open_city_search() -> None:
    query = st.session_state.get("global_search_input", "").strip()
    if query:
        st.session_state.city_search_query = query
        st.session_state.nav_page = "City Explorer"


def page_header(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def section_title(text: str) -> None:
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def top_header_bar(current_page: str = "Dashboard") -> None:
    """Header bar with search bar, notifications, light/dark mode toggle, and profile chip."""
    user = st.session_state.get("user", {"name": "Jasleen Kaur", "role": "Verified User", "is_logged_in": True})
    user_name = user.get("name", "Jasleen Kaur")
    theme = st.session_state.get("theme", "Light")

    # Header container with slight top margin for aesthetic alignment
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    col_bread, col_search, col_actions = st.columns([1.2, 2.2, 2.0])

    with col_bread:
        st.markdown(
            textwrap.dedent(
                f"""
<div style="font-size: 0.82rem; color: var(--text-secondary); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding-top: 10px;">
🧭 Overview / <span style="color: #0D7A5F; font-weight: 800;">{current_page}</span>
</div>
"""
            ),
            unsafe_allow_html=True,
        )

    with col_search:
        st.text_input(
            "Search cities, states, or skills...",
            key="global_search_input",
            label_visibility="collapsed",
            placeholder="🔍 Search cities, states, or skills...",
            on_change=_open_city_search,
        )

    with col_actions:
        c_theme, c_notif, c_user = st.columns([0.8, 0.45, 1.35])
        with c_theme:
            theme_icon = "🌙 Dark" if theme == "Light" else "☀️ Light"
            if st.button(theme_icon, key="theme_toggle_btn", use_container_width=True, help="Toggle Light / Dark Mode"):
                st.session_state.theme = "Dark" if theme == "Light" else "Light"
                st.rerun()

        with c_notif:
            with st.popover("🔔", use_container_width=True):
                st.markdown("### 🔔 Updates")
                st.success("3 new city matches are ready to review.")
                st.info("Pune demand increased 8% this month.")
                st.caption("Updated just now • Data health stable")

        with c_user:
            if user.get("is_logged_in", True):
                if st.button(f"👤 {user_name}", key="profile_hdr_btn", use_container_width=True, help="View Profile"):
                    st.session_state.nav_page = "My Profile"
                    st.rerun()
            else:
                if st.button("✨ Sign In", key="signin_hdr_btn", type="primary", use_container_width=True):
                    st.session_state.nav_page = "Login"
                    st.rerun()


def stat_kpi_cards(df: pd.DataFrame | None = None) -> None:
    """Top KPI Stat counter cards."""
    city_count = int(df["City"].nunique()) if df is not None else 45
    skill_count = int(df["Skill"].nunique()) if df is not None else 20
    openings = int(df["Job_Availability"].sum()) if df is not None else 50000
    health = 100 - (df.isna().sum().sum() / max(df.size, 1) * 100) if df is not None else 98.2
    kpi_data = [
        {"icon": "🏙️", "val": f"{city_count} Cities", "sub": "Analyzed across India", "tag": "Live data", "color": "rgba(13, 122, 95, 0.15)"},
        {"icon": "💼", "val": f"{skill_count} Job Roles", "sub": "Skilled & blue-collar", "tag": "Verified", "color": "rgba(59, 130, 246, 0.15)"},
        {"icon": "📈", "val": f"{openings:,}", "sub": "Aggregated openings", "tag": "Active", "color": "rgba(245, 158, 11, 0.15)"},
        {"icon": "🛡️", "val": f"{health:.1f}%", "sub": "Data health index", "tag": "Stable", "color": "rgba(139, 92, 246, 0.15)"},
    ]

    cols = st.columns(4)
    for col, item in zip(cols, kpi_data):
        with col:
            st.markdown(
                textwrap.dedent(
                    f"""
<div class="stat-kpi-card">
<div class="stat-kpi-header">
<div class="stat-kpi-icon" style="background: {item['color']};">{item['icon']}</div>
<span class="stat-kpi-tag" style="background: {item['color']};">{item['tag']}</span>
</div>
<div>
<div class="stat-kpi-value">{item['val']}</div>
<div class="stat-kpi-label">{item['sub']}</div>
</div>
</div>
"""
                ),
                unsafe_allow_html=True,
            )


def featured_recommendation_card(city_row: pd.Series) -> None:
    """Hero featured city card with photo and explainability narrative."""
    city_name = city_row["City"]
    state_name = city_row["State"]
    score = city_row.get("Match_Score", 98.0)
    img_url = get_city_image(city_name)
    skill = city_row.get("Skill", "Electrician")

    st.markdown(
        textwrap.dedent(
            f"""
<div class="featured-hero-card">
<div class="featured-hero-img" style="background-image: url('{img_url}');">
<div class="featured-hero-city-title">{city_name}</div>
<div class="featured-hero-city-sub">{state_name}, India</div>
</div>
<div class="featured-hero-content">
<div>
<div style="display: flex; gap: 8px; margin-bottom: 0.5rem;">
<span class="score-pill score-pill-emerald">{score:.0f}% Match Score</span>
<span class="score-pill" style="background: var(--subcard-bg);">{skill}</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.4rem;">Why {city_name}?</div>
<div style="font-size: 0.84rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 1rem;">
{city_name} is rapidly expanding as an economic and industrial hub. Recent infrastructure modernization and strong demand for <strong>{skill}</strong> roles make it an exceptional match for your profile. Living costs are well-balanced against salary potential, ensuring superior monthly savings.
</div>
</div>
<div style="display: flex; gap: 1.5rem; font-size: 0.8rem; border-top: 1px solid var(--border-color); padding-top: 0.75rem;">
<div>
<span style="color: var(--text-secondary);">DEMAND GROWTH</span><br>
<strong style="color: #0D7A5F; font-size: 0.95rem;">+24% YoY</strong>
</div>
<div>
<span style="color: var(--text-secondary);">INFRASTRUCTURE</span><br>
<strong style="font-size: 0.95rem;">Tier A Rated</strong>
</div>
<div>
<span style="color: var(--text-secondary);">AVG SALARY</span><br>
<strong style="font-size: 0.95rem;">{format_inr(city_row['Average_Salary'])}</strong>
</div>
</div>
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )


def recommendation_card_detailed(row: pd.Series, rank: int) -> None:
    """Card for top 5 list with circular radial gauge score."""
    city = row["City"]
    state = row["State"]
    score = row["Match_Score"]
    img_url = get_city_image_data_uri(city)

    tag = "Best Match" if rank == 1 else ("Very Good Match" if rank == 2 else "Good Match")

    st.markdown(
        textwrap.dedent(
            f"""
<div class="mm-card" style="display: flex; gap: 16px; align-items: center; padding: 1rem 1.25rem;">
<div style="font-weight: 800; font-size: 1.2rem; color: #0D7A5F; width: 20px;">{rank}</div>
<div style="width: 85px; height: 65px; border-radius: 10px; background-image: url('{img_url}'); background-size: cover; background-position: center; flex-shrink: 0;"></div>
<div style="flex: 1;">
<div style="display: flex; align-items: center; gap: 8px;">
<strong style="font-size: 1.05rem;">{city}</strong>
<span class="score-pill score-pill-emerald" style="font-size: 0.68rem; padding: 0.15rem 0.45rem;">{tag}</span>
</div>
<div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 0.35rem;">{state} • High job demand with great savings potential</div>
<div style="display: flex; gap: 14px; font-size: 0.78rem; color: var(--text-secondary);">
<span>Avg. Salary: <strong style="color:var(--text-primary);">{format_inr(row['Average_Salary'])}</strong></span>
<span>Avg. Rent: <strong style="color:var(--text-primary);">{format_inr(row['Average_1BHK_Rent'])}</strong></span>
<span>Est. Savings: <strong style="color:#0D7A5F;">{format_inr(row['Estimated_Monthly_Savings'])}</strong></span>
</div>
</div>
<div class="score-radial">
{score:.0f}
<span>/100</span>
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )


def city_explorer_card(row: pd.Series) -> None:
    """Card for City Explorer hub grid."""
    city = row["City"]
    state = row["State"]
    region = row["Region"]
    img_url = get_city_image_data_uri(city)
    score = row.get("Job_Demand_Score", 85)
    sectors = get_city_sectors(city)
    col_tag = cost_of_living_label(row.get("Estimated_Monthly_Expenses", 6000))
    vacancies = int(row.get("Job_Availability", 750))

    sectors_html = "".join([f'<span class="sector-tag">{s}</span>' for s in sectors[:3]])

    st.markdown(
        textwrap.dedent(
            f"""
<div class="city-explorer-card">
<div class="city-card-header-img" style="background-image: url('{img_url}');">
<div></div>
<span class="score-pill score-pill-emerald" style="background: var(--card-bg); border: 1px solid var(--border-color); font-size: 0.72rem; z-index: 2;">
Match Score: {score:.0f}
</span>
<div class="city-card-city-name">{city}</div>
<div class="city-card-location">{state}, {region}</div>
</div>
<div class="city-card-body">
<div style="margin-bottom: 0.6rem;">{sectors_html}</div>
<div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: var(--text-secondary); border-top: 1px solid var(--border-color); padding-top: 0.5rem; margin-bottom: 0.6rem;">
<div>COST OF LIVING<br><strong style="color: var(--text-primary);">{col_tag}</strong></div>
<div>JOB GROWTH<br><strong style="color: #0D7A5F;">+14% YoY</strong></div>
<div>ACTIVE JOBS<br><strong style="color: var(--text-primary);">{vacancies}+</strong></div>
</div>
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )


def author_attribution_box() -> None:
    """Attribution box on About page."""
    st.markdown(
        textwrap.dedent(
            """
<div class="author-attribution-card">
<div>
<div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #0D7A5F;">
Minor Project • BCA (2024–2027)
</div>
<div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.2rem;">
Punjab College of Technical Education, Ludhiana
</div>
</div>
<div style="text-align: right;">
<div style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em;">Developed & Submitted by</div>
<div class="author-name-tag">Jasleen Kaur</div>
</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )
