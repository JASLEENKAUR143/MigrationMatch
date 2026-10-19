"""MigrationMatch — Skill-to-City Relocation Platform
Main Entry Point: Loads data, configures layout, and routes pages.
Author: Jasleen Kaur, BCA (2024-2027), Punjab College of Technical Education, Ludhiana
"""
from pathlib import Path
import streamlit as st

from analysis.eda import clean_data, load_data
from model.recommendation_model import engineer_features
from ui.pages import (
    about,
    admin,
    analytics,
    city_explorer,
    compare,
    dashboard,
    history,
    login,
    profile,
    recommendation,
    report_generator,
    saved,
)
from ui.session import init_session
from ui.sidebar import render_sidebar
from ui.styles import inject_styles

st.set_page_config(
    page_title="MigrationMatch — Skill-to-City Relocation Platform",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "migrationmatch_dataset.csv"

@st.cache_data
def load_and_prepare():
    df = load_data(DATA_PATH)
    df_clean = clean_data(df)
    df_feat = engineer_features(df_clean.copy())
    return df_clean, df_feat


try:
    df, df_feat = load_and_prepare()
except FileNotFoundError:
    st.error(
        "Dataset not found at `data/migrationmatch_dataset.csv`. "
        "Please ensure the CSV file exists."
    )
    st.stop()
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    st.stop()

init_session(df)
inject_styles()

page = render_sidebar()

# Exact requested navigation map
PAGES = {
    "Dashboard": dashboard.render,
    "My Profile": profile.render,
    "Get Recommendations": recommendation.render,
    "Search and Compare": compare.render,
    "City Explorer": city_explorer.render,
    "Market Analysis": analytics.render,
    "Saved Results": saved.render,
    "Search History": history.render,
    "Report Generator": report_generator.render,
    "Admin": admin.render,
    "About Project": about.render,
    "Login": login.render,
    # Aliases
    "Get Recommendation": recommendation.render,
    "Search & Compare": compare.render,
    "Analytics": analytics.render,
    "History": history.render,
    "About Us": about.render,
}

render_func = PAGES.get(page, dashboard.render)
render_func(df, df_feat)