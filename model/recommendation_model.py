"""Feature engineering, recommendation engine, explainability, and real Scikit-Learn ML pipeline."""
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.tree import DecisionTreeClassifier


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Derived financial ratios
    df["Expense_Salary_Ratio"] = df["Estimated_Monthly_Expenses"] / (df["Average_Salary"].replace(0, np.nan))
    df["Expense_Salary_Ratio"] = df["Expense_Salary_Ratio"].fillna(1.0).clip(0, 2.0)

    df["Savings_Ratio"] = df["Estimated_Monthly_Savings"] / (df["Average_Salary"].replace(0, np.nan))
    df["Savings_Ratio"] = df["Savings_Ratio"].fillna(0).clip(-1.0, 1.0)

    # Socio-Economic composite index
    df["Socio_Economic_Index"] = df[[
        "Healthcare_Score", "Transportation_Score", "Quality_of_Life_Score", "Safety_Score", "Affordability_Score"
    ]].mean(axis=1)

    df["Job_Demand_Index"] = df["Job_Demand_Score"] / 100.0

    df["Rental_Ratio"] = df["Average_1BHK_Rent"] / (df["Average_Salary"].replace(0, np.nan))
    df["Rental_Ratio"] = df["Rental_Ratio"].fillna(1.0).clip(0, 2.0)

    scaler = MinMaxScaler()
    df[[
        "Average_Salary_Norm",
        "Rental_Ratio_Norm",
        "Expense_Salary_Ratio_Norm",
        "Savings_Ratio_Norm",
        "Socio_Economic_Index_Norm",
        "Job_Demand_Index_Norm",
    ]] = scaler.fit_transform(df[[
        "Average_Salary",
        "Rental_Ratio",
        "Expense_Salary_Ratio",
        "Savings_Ratio",
        "Socio_Economic_Index",
        "Job_Demand_Index",
    ]].fillna(0))

    return df


def _experience_salary_factor(experience_years: int) -> float:
    if experience_years <= 1:
        return 0.85
    elif 2 <= experience_years <= 5:
        return 1.0
    else:
        return 1.18


def recommend_cities(
    df: pd.DataFrame,
    skill: str,
    experience_years: int = 3,
    expected_salary: float = 25000,
    max_rent: float = 8000,
    desired_savings: float = 10000,
    region_pref: str = None,
    top_n: int = 10,
    custom_weights: dict = None,
) -> pd.DataFrame:
    if experience_years < 0 or expected_salary < 0 or max_rent < 0 or desired_savings < 0:
        raise ValueError("Experience, expected salary, rent and desired savings must be non-negative.")

    df = df.copy()

    subset = df[df["Skill"].str.lower() == skill.strip().lower()].copy()
    if subset.empty:
        subset = df.copy()

    if region_pref and region_pref.lower() not in ["all", "all regions", "any region", "none"]:
        subset = subset[subset["Region"].str.lower() == region_pref.strip().lower()]
        if subset.empty:
            subset = df[df["Skill"].str.lower() == skill.strip().lower()].copy()

    exp_factor = _experience_salary_factor(experience_years)
    subset["Adj_Average_Salary"] = subset["Average_Salary"] * exp_factor

    subset["Salary_Suitability"] = 1 - (
        np.abs(expected_salary - subset["Adj_Average_Salary"])
        / (np.maximum(expected_salary, subset["Adj_Average_Salary"]) + 1)
    )
    subset["Salary_Suitability"] = subset["Salary_Suitability"].clip(0, 1)

    subset["Rental_Affordability"] = 1 - subset["Rental_Ratio_Norm"]
    subset.loc[subset["Average_1BHK_Rent"] > max_rent, "Rental_Affordability"] *= 0.55
    subset["Rental_Affordability"] = subset["Rental_Affordability"].clip(0, 1)

    subset["Savings_Suitability"] = 1 - (
        np.abs(desired_savings - subset["Estimated_Monthly_Savings"])
        / (np.maximum(desired_savings, subset["Estimated_Monthly_Savings"]) + 1)
    )
    subset["Savings_Suitability"] = subset["Savings_Suitability"].clip(0, 1)

    subset["Healthcare_Norm"] = subset["Healthcare_Score"] / 100.0
    subset["Transportation_Norm"] = subset["Transportation_Score"] / 100.0
    subset["Quality_of_Life_Norm"] = subset["Quality_of_Life_Score"] / 100.0
    subset["Affordability_Norm"] = subset["Affordability_Score"] / 100.0
    subset["Job_Demand_Norm"] = subset["Job_Demand_Score"] / 100.0

    w = {
        "Job_Demand": 0.30,
        "Salary_Suitability": 0.25,
        "Rental_Affordability": 0.20,
        "Savings_Suitability": 0.15,
        "Quality_of_Life": 0.10,
    }
    if custom_weights:
        w.update(custom_weights)

    total_w = sum(w.values())
    w = {k: v / total_w for k, v in w.items()}

    subset["Score_Aggregate"] = (
        w["Job_Demand"] * subset["Job_Demand_Norm"]
        + w["Salary_Suitability"] * subset["Salary_Suitability"]
        + w["Rental_Affordability"] * subset["Rental_Affordability"]
        + w["Savings_Suitability"] * subset["Savings_Suitability"]
        + w["Quality_of_Life"] * subset["Quality_of_Life_Norm"]
    )

    min_s = subset["Score_Aggregate"].min()
    max_s = subset["Score_Aggregate"].max()
    if max_s > min_s:
        subset["Match_Score"] = 55 + 45 * ((subset["Score_Aggregate"] - min_s) / (max_s - min_s))
    else:
        subset["Match_Score"] = 85.0

    reasons = []
    for _, r in subset.iterrows():
        r_text = []
        if r["Job_Demand_Score"] >= 70:
            r_text.append(f"High job demand ({r['Job_Demand_Score']:.0f}/100)")
        if r["Average_Salary"] >= expected_salary * 0.9:
            r_text.append(f"Strong salary potential (₹{r['Average_Salary']:,.0f})")
        if r["Average_1BHK_Rent"] <= max_rent:
            r_text.append(f"Affordable 1BHK rent (₹{r['Average_1BHK_Rent']:,.0f})")
        if r["Quality_of_Life_Score"] >= 65:
            r_text.append("High quality of life & safety")
        if not r_text:
            r_text.append("Balanced living costs and steady employment opportunities")
        reasons.append(" • ".join(r_text))

    subset["Why_Recommended"] = reasons
    subset = subset.sort_values("Match_Score", ascending=False).reset_index(drop=True)
    subset["Rank"] = subset.index + 1

    out_cols = [
        "Rank", "City", "State", "Region", "Skill",
        "Match_Score", "Job_Demand_Score", "Average_Salary", "Minimum_Salary", "Maximum_Salary",
        "Average_1BHK_Rent", "Estimated_Monthly_Expenses", "Estimated_Monthly_Savings",
        "Healthcare_Score", "Transportation_Score", "Quality_of_Life_Score", "Safety_Score",
        "Affordability_Score", "Why_Recommended",
    ]
    return subset[out_cols].head(top_n).copy()


def get_city_profile(df: pd.DataFrame, city: str) -> pd.DataFrame:
    sel = df[df["City"].str.lower() == city.strip().lower()]
    if sel.empty:
        return pd.DataFrame()
    return sel.agg({
        "Average_Salary": "mean",
        "Average_1BHK_Rent": "mean",
        "Estimated_Monthly_Expenses": "mean",
        "Estimated_Monthly_Savings": "mean",
        "Job_Demand_Score": "mean",
        "Healthcare_Score": "mean",
        "Transportation_Score": "mean",
        "Quality_of_Life_Score": "mean",
        "Safety_Score": "mean",
        "Affordability_Score": "mean",
    }).round(2)


# ==========================================
# REAL DATA SCIENCE ML PIPELINE & EVALUATION
# ==========================================

_CACHED_ML_RESULTS = None


def train_and_evaluate_ml_models(df: pd.DataFrame):
    """
    Train and evaluate real Scikit-Learn models on the MigrationMatch dataset.
    Target: High_Potential_Relocation (1 if Savings > Median and Job Demand >= 60, else 0).
    """
    global _CACHED_ML_RESULTS
    if _CACHED_ML_RESULTS is not None:
        return _CACHED_ML_RESULTS

    df_ml = df.copy()

    # Define features
    feature_cols = [
        "Average_Salary",
        "Average_1BHK_Rent",
        "Estimated_Monthly_Expenses",
        "Healthcare_Score",
        "Transportation_Score",
        "Quality_of_Life_Score",
        "Safety_Score",
        "Affordability_Score",
    ]

    # Target variable: High Potential Relocation destination
    median_sav = df_ml["Estimated_Monthly_Savings"].median()
    df_ml["Target"] = (
        (df_ml["Estimated_Monthly_Savings"] >= median_sav)
        & (df_ml["Job_Demand_Score"] >= 58)
    ).astype(int)

    X = df_ml[feature_cols].fillna(0)
    y = df_ml["Target"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Scale for linear models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Models dictionary
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    }

    results = {
        "models": {},
        "comparison_table": [],
        "roc_curves": {},
        "confusion_matrices": {},
        "feature_importance": None,
        "trained_rf_model": None,
        "feature_names": feature_cols,
        "test_size": len(y_test),
        "train_size": len(y_train),
    }

    for name, clf in models.items():
        if name == "Logistic Regression":
            clf.fit(X_train_scaled, y_train)
            y_pred = clf.predict(X_test_scaled)
            y_prob = clf.predict_proba(X_test_scaled)[:, 1]
        else:
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            y_prob = clf.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred) * 100
        prec = precision_score(y_test, y_pred, zero_division=0) * 100
        rec = recall_score(y_test, y_pred, zero_division=0) * 100
        f1 = f1_score(y_test, y_pred, zero_division=0) * 100
        cm = confusion_matrix(y_test, y_pred)

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        results["models"][name] = {
            "accuracy": round(acc, 2),
            "precision": round(prec, 2),
            "recall": round(rec, 2),
            "f1": round(f1, 2),
            "auc": round(roc_auc, 3),
            "cm": cm,
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist(),
        }

        results["comparison_table"].append({
            "Model": name,
            "Accuracy (%)": round(acc, 2),
            "Precision (%)": round(prec, 2),
            "Recall (%)": round(rec, 2),
            "F1 Score (%)": round(f1, 2),
            "ROC AUC": round(roc_auc, 3),
        })

    # Extract Random Forest Feature Importances
    rf_model = models["Random Forest"]
    results["trained_rf_model"] = rf_model
    importances = rf_model.feature_importances_
    results["feature_importance"] = pd.DataFrame({
        "Feature": [f.replace("_", " ") for f in feature_cols],
        "Importance": importances,
    }).sort_values("Importance", ascending=True)

    _CACHED_ML_RESULTS = results
    return results


def predict_relocation_potential(model, feature_values: dict) -> dict:
    """Predict relocation success probability using trained Random Forest."""
    cols = [
        "Average_Salary",
        "Average_1BHK_Rent",
        "Estimated_Monthly_Expenses",
        "Healthcare_Score",
        "Transportation_Score",
        "Quality_of_Life_Score",
        "Safety_Score",
        "Affordability_Score",
    ]
    df_input = pd.DataFrame([[feature_values.get(c, 50) for c in cols]], columns=cols)
    prob = model.predict_proba(df_input)[0][1]
    pred = int(prob >= 0.5)

    return {
        "prediction": "High Potential Match" if pred == 1 else "Moderate / Low Potential Match",
        "probability": round(prob * 100, 1),
        "is_recommended": pred == 1,
    }