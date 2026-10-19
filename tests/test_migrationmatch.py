from pathlib import Path

import pandas as pd
import pytest
from analysis.eda import load_data, clean_data, get_basic_stats
from data.database import hash_password, verify_password
from model.recommendation_model import engineer_features, recommend_cities

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "migrationmatch_dataset.csv"

def test_password_hash_verification():
    password = "test-password"
    password_hash = hash_password(password)
    assert verify_password(password, password_hash)
    assert not verify_password("wrong-password", password_hash)

def test_dataset_exists():
    assert DATA_PATH.exists(), "Dataset file is missing."

def test_dataset_loads():
    df = load_data(DATA_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_required_columns_exist():
    df = load_data(DATA_PATH)
    required = [
        "City", "State", "Region", "Skill", "Job_Demand_Score", "Job_Availability",
        "Minimum_Salary", "Average_Salary", "Maximum_Salary",
        "Average_1BHK_Rent", "Shared_Rent",
        "Food_Cost", "Utilities_Cost", "Transport_Cost", "Other_Monthly_Cost",
        "Estimated_Monthly_Expenses", "Estimated_Monthly_Savings",
        "Healthcare_Score", "Transportation_Score", "Quality_of_Life_Score",
        "Safety_Score", "Affordability_Score"
    ]
    for col in required:
        assert col in df.columns, f"Missing column: {col}"

def test_dataset_not_empty_after_cleaning():
    df = load_data(DATA_PATH)
    dfc = clean_data(df)
    assert len(dfc) > 0

def test_number_of_cities_and_occupations():
    df = clean_data(load_data(DATA_PATH))
    assert df["City"].nunique() >= 40, "Number of cities is less than required (40)."
    assert df["Skill"].nunique() >= 20, "Number of occupations is less than required (20)."

def test_missing_values_handled():
    df = clean_data(load_data(DATA_PATH))
    assert df.isnull().sum().sum() == 0, "There are still missing values after cleaning."

def test_salary_values_valid():
    df = clean_data(load_data(DATA_PATH))
    assert (df["Average_Salary"] >= 0).all()
    assert (df["Minimum_Salary"] >= 0).all()
    assert (df["Maximum_Salary"] >= 0).all()

def test_rent_values_valid():
    df = clean_data(load_data(DATA_PATH))
    assert (df["Average_1BHK_Rent"] >= 0).all()
    assert (df["Shared_Rent"] >= 0).all()

def test_savings_values_valid():
    df = clean_data(load_data(DATA_PATH))
    assert "Estimated_Monthly_Savings" in df.columns
    # Basic sanity: savings shouldn't be absurd (not less than -50% of salary)
    assert (df["Estimated_Monthly_Savings"] >= -0.5 * df["Average_Salary"]).all()

def test_feature_engineering_adds_columns():
    df = clean_data(load_data(DATA_PATH))
    df_feat = engineer_features(df)
    expected_cols = [
        "Expense_Salary_Ratio", "Savings_Ratio", "Socio_Economic_Index",
        "Job_Demand_Index", "Rental_Ratio",
        "Average_Salary_Norm", "Rental_Ratio_Norm"
    ]
    for col in expected_cols:
        assert col in df_feat.columns, f"Feature not found: {col}"

def test_recommendation_function_basic():
    df = clean_data(load_data(DATA_PATH))
    df_feat = engineer_features(df)
    # pick a valid skill
    skill = df_feat["Skill"].unique()[0]
    recs = recommend_cities(
        df_feat,
        skill=skill,
        experience_years=2,
        expected_salary=15000,
        max_rent=8000,
        desired_savings=3000,
        region_pref=None,
        top_n=5
    )
    # Should return a DataFrame and top scores between 0 and 100
    assert isinstance(recs, pd.DataFrame)
    if not recs.empty:
        assert "Match_Score" in recs.columns
        assert recs["Match_Score"].between(0, 100).all()
        # Sorted descending
        scores = recs["Match_Score"].tolist()
        assert scores == sorted(scores, reverse=True)

def test_invalid_inputs_handled_in_recommend():
    df = clean_data(load_data(DATA_PATH))
    df_feat = engineer_features(df)
    with pytest.raises(ValueError):
        recommend_cities(df_feat, skill=df_feat["Skill"].iloc[0], experience_years=-1, expected_salary=10000, max_rent=5000, desired_savings=2000)