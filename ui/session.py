"""Session management for MigrationMatch — Auth, preferences, history, saved shortlist."""
import os

import pandas as pd
import streamlit as st

from data.database import (
    init_db,
    load_saved_cities,
    load_users,
    save_recommendation,
    seed_demo_users,
    set_saved_city,
)
from model.recommendation_model import recommend_cities

DEFAULT_INPUTS = {
    "skill": "Electrician",
    "experience_years": 3,
    "expected_salary": 25000,
    "max_rent": 8000,
    "desired_savings": 10000,
    "family_size": 3,
    "region_pref": None,
    "preferred_city_type": "Tier 1 & Tier 2 Cities",
}

DEFAULT_USER = {
    "name": "Jasleen Kaur",
    "email": "jasleen@gmail.com",
    "role": "Verified User",
    "institution": "Punjab College of Technical Education, Ludhiana",
    "course": "BCA (2024-2027)",
    "is_logged_in": True,
}

DEFAULT_ADMIN_PARAMS = {
    "cost_of_living_weight": 0.20,
    "job_demand_weight": 0.30,
    "salary_suitability_weight": 0.25,
    "savings_weight": 0.15,
    "quality_of_life_weight": 0.10,
    "healthcare_weight": 0.05,
    "transportation_weight": 0.05,
    "safety_weight": 0.05,
    "refresh_rate": "Weekly",
    "selected_preset": "Balanced Approach",
}

INITIAL_HISTORY = [
    {
        "timeframe": "Today",
        "title": "AC Technician in Any Region",
        "params": "Demand > 70%, Cost of Living < 50k INR, Language: Hindi/English",
        "top_city": "Varanasi",
        "top_score": 100,
        "skill": "AC Technician",
        "salary": 22000,
        "rent": 7500,
    },
    {
        "timeframe": "Yesterday",
        "title": "Electrician in Maharashtra",
        "params": "Industrial sector, Safety score > 80, West Region",
        "top_city": "Pune",
        "top_score": 92,
        "skill": "Electrician",
        "salary": 28000,
        "rent": 8000,
    },
    {
        "timeframe": "12 Oct",
        "title": "Plumber in Gujarat",
        "params": "Residential demand, Affordable housing available",
        "top_city": "Surat",
        "top_score": 88,
        "skill": "Plumber",
        "salary": 20000,
        "rent": 6500,
    },
]


def init_session(df: pd.DataFrame) -> None:
    init_db()
    seed_demo_users()
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Dashboard"

    if "user" not in st.session_state:
        st.session_state.user = DEFAULT_USER.copy()

    if "theme" not in st.session_state:
        st.session_state.theme = "Light"

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if "admin_pin" not in st.session_state:
        try:
            configured_admin_pin = st.secrets.get("admin_pin")
        except FileNotFoundError:
            configured_admin_pin = None
        st.session_state.admin_pin = (
            configured_admin_pin or os.getenv("MIGRATIONMATCH_ADMIN_PIN") or "1234"
        )

    if "inputs" not in st.session_state:
        st.session_state.inputs = DEFAULT_INPUTS.copy()

    if "admin_params" not in st.session_state:
        st.session_state.admin_params = DEFAULT_ADMIN_PARAMS.copy()

    if "saved_cities" not in st.session_state:
        email = st.session_state.user["email"]
        st.session_state.saved_cities = load_saved_cities(
            email, ["Varanasi", "Bengaluru", "Pune", "Ahmedabad", "Coimbatore"]
        )

    if "search_history" not in st.session_state:
        st.session_state.search_history = INITIAL_HISTORY.copy()

    if "compare_cities" not in st.session_state:
        st.session_state.compare_cities = ["Pune", "Bengaluru"]

    if "last_results" not in st.session_state:
        st.session_state.last_results = None

    if "user_database" not in st.session_state:
        st.session_state.user_database = load_users()


def get_inputs() -> dict:
    return st.session_state.get("inputs", DEFAULT_INPUTS.copy())


def update_inputs(**kwargs) -> None:
    for k, v in kwargs.items():
        if k in st.session_state.inputs:
            st.session_state.inputs[k] = v


def toggle_saved_city(city: str) -> bool:
    saved = st.session_state.setdefault("saved_cities", [])
    email = st.session_state.get("user", {}).get("email", "jasleen@gmail.com")
    if city in saved:
        saved.remove(city)
        set_saved_city(email, city, False)
        return False
    else:
        saved.append(city)
        set_saved_city(email, city, True)
        return True


def is_city_saved(city: str) -> bool:
    return city in st.session_state.get("saved_cities", [])


def run_recommendation(df_feat: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    inp = get_inputs()
    weights = {
        "Job_Demand": st.session_state.admin_params.get("job_demand_weight", 0.30),
        "Salary_Suitability": st.session_state.admin_params.get("salary_suitability_weight", 0.25),
        "Rental_Affordability": st.session_state.admin_params.get("cost_of_living_weight", 0.20),
        "Savings_Suitability": st.session_state.admin_params.get("savings_weight", 0.15),
        "Quality_of_Life": st.session_state.admin_params.get("quality_of_life_weight", 0.10),
    }
    results = recommend_cities(
        df=df_feat,
        skill=inp["skill"],
        experience_years=inp["experience_years"],
        expected_salary=inp["expected_salary"],
        max_rent=inp["max_rent"],
        desired_savings=inp["desired_savings"],
        region_pref=inp.get("region_pref"),
        top_n=top_n,
        custom_weights=weights,
    )
    st.session_state.last_results = results
    if not results.empty:
        user_email = st.session_state.get("user", {}).get("email", "jasleen@gmail.com")
        save_recommendation(
            user_email,
            inp["skill"],
            inp.get("region_pref"),
            results.iloc[0]["City"],
            results.iloc[0]["Match_Score"],
        )
    return results


def clear_session() -> None:
    st.session_state.user["is_logged_in"] = False
    st.session_state.user["role"] = "Guest"
    st.session_state.user["name"] = ""
    st.session_state.user["email"] = ""
    st.session_state.admin_authenticated = False
    st.session_state.nav_page = "Login"
