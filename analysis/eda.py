"""
analysis/eda.py

Functions:
- load_data(path): loads CSV into a DataFrame
- clean_data(df): performs cleaning steps and returns cleaned DataFrame
- get_basic_stats(df): returns (num_cities, num_occupations, num_records, num_states)

This module centralizes data cleaning and basic exploratory helpers for Streamlit and tests.
"""
from pathlib import Path

import pandas as pd
import numpy as np

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "migrationmatch_dataset.csv"

REQUIRED_COLUMNS = [
    "City", "State", "Region", "Skill", "Job_Demand_Score", "Job_Availability",
    "Minimum_Salary", "Average_Salary", "Maximum_Salary",
    "Average_1BHK_Rent", "Shared_Rent",
    "Food_Cost", "Utilities_Cost", "Transport_Cost", "Other_Monthly_Cost",
    "Estimated_Monthly_Expenses", "Estimated_Monthly_Savings",
    "Healthcare_Score", "Transportation_Score", "Quality_of_Life_Score",
    "Safety_Score", "Affordability_Score"
]

def load_data(path=DEFAULT_DATA_PATH):
    """
    Loads CSV from path. Raises FileNotFoundError if missing.
    """
    df = pd.read_csv(path)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset with the following steps:
    - Lower-level checks for required columns
    - Strip whitespace and standardize text for City, State, Skill
    - Remove duplicates
    - Detect and handle missing values:
        * For numeric columns: fill with median
        * For categorical: fill with mode
    - Ensure numeric columns have valid (non-negative) values; clip negatives to 0
    - Recompute Estimated_Monthly_Expenses if missing or inconsistent
    - Recompute Estimated_Monthly_Savings = Average_Salary - Estimated_Monthly_Expenses
    """
    df = df.copy()

    # 1. Verify required columns exist — if not, raise error
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise KeyError(f"Required column missing: {col}")

    # 2. Strip and standardize text columns
    for col in ["City", "State", "Region", "Skill"]:
        df[col] = df[col].astype(str).str.strip().replace({"nan": ""})
        # Title case City and State for consistency
        if col in ["City", "State"]:
            df[col] = df[col].str.title()

    # 3. Remove exact duplicate rows
    df_before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    df_after = len(df)

    # 4. Handle missing values
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]

    # Fill numeric NaNs with median
    for c in num_cols:
        if df[c].isna().any():
            median = df[c].median()
            df[c] = df[c].fillna(median)

    # Fill categorical NaNs with mode or empty string
    for c in cat_cols:
        if df[c].isna().any():
            mode = df[c].mode()
            fill = mode.iloc[0] if not mode.empty else ""
            df[c] = df[c].fillna(fill)

    # 5. Clip invalid numeric values (no negatives)
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        df[c] = df[c].clip(lower=0)

    # 6. Recompute Estimated_Monthly_Expenses and Savings if needed
    expense_components = ["Average_1BHK_Rent", "Food_Cost", "Utilities_Cost", "Transport_Cost", "Other_Monthly_Cost"]
    # If any expense component missing or zero, compute reasonable defaults proportional to salary
    for idx, row in df.iterrows():
        avg_salary = row["Average_Salary"] if row["Average_Salary"] > 0 else np.nan
        # If components are zero, replace with sensible fractions of salary
        if any(row[c] == 0 for c in expense_components) and not np.isnan(avg_salary) and avg_salary > 0:
            df.at[idx, "Food_Cost"] = df.at[idx, "Food_Cost"] if df.at[idx, "Food_Cost"] > 0 else int(avg_salary * 0.12)
            df.at[idx, "Utilities_Cost"] = df.at[idx, "Utilities_Cost"] if df.at[idx, "Utilities_Cost"] > 0 else int(avg_salary * 0.04)
            df.at[idx, "Transport_Cost"] = df.at[idx, "Transport_Cost"] if df.at[idx, "Transport_Cost"] > 0 else int(avg_salary * 0.06)
            df.at[idx, "Other_Monthly_Cost"] = df.at[idx, "Other_Monthly_Cost"] if df.at[idx, "Other_Monthly_Cost"] > 0 else int(avg_salary * 0.05)
            # Rent: if zero set a portion of salary
            df.at[idx, "Average_1BHK_Rent"] = df.at[idx, "Average_1BHK_Rent"] if df.at[idx, "Average_1BHK_Rent"] > 0 else int(avg_salary * 0.30)
            df.at[idx, "Shared_Rent"] = int(df.at[idx, "Average_1BHK_Rent"] * 0.5)

    # Recompute the total expenses and savings
    df["Estimated_Monthly_Expenses"] = (
        df["Average_1BHK_Rent"] + df["Food_Cost"] + df["Utilities_Cost"] + df["Transport_Cost"] + df["Other_Monthly_Cost"]
    ).astype(int)

    df["Estimated_Monthly_Savings"] = (df["Average_Salary"] - df["Estimated_Monthly_Expenses"]).astype(int)
    # Make sure savings are not extremely negative — clip to -0.5 * salary as a pragmatic cap
    df["Estimated_Monthly_Savings"] = df["Estimated_Monthly_Savings"].clip(lower=(-0.5 * df["Average_Salary"])).astype(int)

    # 7. Ensure all score columns are 0–100 and integers
    score_cols = ["Job_Demand_Score", "Healthcare_Score", "Transportation_Score",
                  "Quality_of_Life_Score", "Safety_Score", "Affordability_Score"]
    for c in score_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).round().astype(int)
        df[c] = df[c].clip(0, 100)

    return df.reset_index(drop=True)

def get_basic_stats(df: pd.DataFrame):
    num_cities = df["City"].nunique()
    num_occupations = df["Skill"].nunique()
    num_records = len(df)
    num_states = df["State"].nunique()
    return num_cities, num_occupations, num_records, num_states