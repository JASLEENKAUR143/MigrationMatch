"""Plotly chart builders for MigrationMatch — Dark & Light Theme Adaptive."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Color tokens
EMERALD = "#0D7A5F"
EMERALD_LIGHT = "#34D399"
SLATE_DARK = "#0F172A"
SLATE_LIGHT = "#64748B"
BLUE = "#3B82F6"
AMBER = "#F59E0B"
ROSE = "#EF4444"


def _get_theme_settings():
    is_dark = st.session_state.get("theme", "Light") == "Dark"
    bg_color = "rgba(0,0,0,0)"
    grid_color = "#1E293B" if is_dark else "#F1F5F9"
    text_color = "#F8FAFC" if is_dark else "#0F172A"
    font_color = "#94A3B8" if is_dark else "#64748B"
    template = "plotly_dark" if is_dark else "plotly_white"
    return bg_color, grid_color, text_color, font_color, template


def city_comparison_overview_chart(results: pd.DataFrame) -> go.Figure:
    """Multi-metric combo chart: Grouped bars for Salary, Rent, Expenses + line for Job Demand."""
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    df_top = results.head(5).copy()
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Avg. Salary (₹)",
        x=df_top["City"],
        y=df_top["Average_Salary"],
        marker_color=EMERALD,
        yaxis="y1",
    ))

    fig.add_trace(go.Bar(
        name="Avg. Rent (₹)",
        x=df_top["City"],
        y=df_top["Average_1BHK_Rent"],
        marker_color="#F87171",
        yaxis="y1",
    ))

    fig.add_trace(go.Bar(
        name="Cost of Living (₹)",
        x=df_top["City"],
        y=df_top["Estimated_Monthly_Expenses"],
        marker_color="#60A5FA",
        yaxis="y1",
    ))

    fig.add_trace(go.Scatter(
        name="Job Demand (0-100)",
        x=df_top["City"],
        y=df_top["Job_Demand_Score"],
        mode="lines+markers",
        line=dict(color="#A78BFA", width=3),
        marker=dict(size=8, color="#8B5CF6"),
        yaxis="y2",
    ))

    fig.update_layout(
        template=template,
        barmode="group",
        height=380,
        margin=dict(l=10, r=20, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=font_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        yaxis=dict(title="Amount (₹)", showgrid=True, gridcolor=grid_color, color=font_color),
        yaxis2=dict(
            title="Job Demand Score",
            overlaying="y",
            side="right",
            range=[0, 100],
            showgrid=False,
            color=font_color,
        ),
        xaxis=dict(color=font_color),
    )
    return fig


def regional_salary_trends_chart(df: pd.DataFrame) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    regions = ["North", "South", "East", "West", "Central"]
    avg_sal = [14200, 15800, 13400, 16200, 13900]
    avg_cost = [6200, 7800, 5900, 8100, 6400]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Avg Salary (₹)",
        x=[f"{r} Region" for r in regions],
        y=avg_sal,
        marker_color=EMERALD,
    ))
    fig.add_trace(go.Bar(
        name="Cost of Living (₹)",
        x=[f"{r} Region" for r in regions],
        y=avg_cost,
        marker_color=EMERALD_LIGHT,
    ))

    fig.update_layout(
        template=template,
        barmode="group",
        height=320,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=font_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        yaxis=dict(title="Monthly Compensation (₹)", showgrid=True, gridcolor=grid_color, color=font_color),
        xaxis=dict(color=font_color),
    )
    return fig


def cost_breakdown_donut(city_name: str = "Varanasi", total_exp: float = 9200) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    labels = ["Rent (45%)", "Food (30%)", "Transport (15%)", "Misc (10%)"]
    values = [45, 30, 15, 10]
    colors = [EMERALD, EMERALD_LIGHT, "#99F6E4", "#CBD5E1"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.68,
        marker=dict(colors=colors),
        textinfo="none",
    )])

    fig.update_layout(
        template=template,
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, font=dict(color=font_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        annotations=[dict(
            text=f"<b>Total Avg</b><br><span style='font-size:1.15rem;color:#0D7A5F;'>₹{total_exp:,.0f}</span>",
            x=0.5, y=0.5,
            font_size=11,
            showarrow=False,
            font=dict(color=text_color),
        )],
    )
    return fig


def rental_fluctuation_line_chart() -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    varanasi = [3800, 3850, 3880, 3900, 3950, 4100, 4050, 4120, 4180, 4220, 4260, 4300]
    lucknow = [3300, 3350, 3400, 3450, 3480, 3550, 3580, 3620, 3670, 3720, 3750, 3800]
    patna = [4400, 4450, 4500, 4550, 4600, 4700, 4750, 4800, 4850, 4920, 5000, 5100]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=varanasi,
        mode="lines+markers",
        name="Varanasi",
        line=dict(color=EMERALD, width=3),
        marker=dict(size=6),
    ))
    fig.add_trace(go.Scatter(
        x=months, y=lucknow,
        mode="lines",
        name="Lucknow",
        line=dict(color=BLUE, width=2, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=months, y=patna,
        mode="lines",
        name="Patna",
        line=dict(color=SLATE_LIGHT, width=2, dash="dash"),
    ))

    fig.update_layout(
        template=template,
        height=300,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(color=font_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        yaxis=dict(title="Rent (₹)", showgrid=True, gridcolor=grid_color, color=font_color),
        xaxis=dict(color=font_color),
    )
    return fig


def top_skills_demand_chart(df: pd.DataFrame) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    top_skills = df.groupby("Skill")["Job_Demand_Score"].mean().nlargest(5).reset_index()
    top_skills = top_skills.sort_values("Job_Demand_Score", ascending=True)

    fig = go.Figure(go.Bar(
        x=top_skills["Job_Demand_Score"],
        y=top_skills["Skill"],
        orientation="h",
        marker_color="#8B5CF6",
        text=[f"{v:.1f}" for v in top_skills["Job_Demand_Score"]],
        textposition="outside",
    ))
    fig.update_layout(
        template=template,
        height=260,
        margin=dict(l=10, r=30, t=10, b=10),
        xaxis=dict(title="Avg Demand Score (0-100)", range=[0, 100], gridcolor=grid_color, color=font_color),
        yaxis=dict(color=font_color),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
    )
    return fig


def vacancies_by_skill_chart(df: pd.DataFrame) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    top_vac = df.groupby("Skill")["Job_Availability"].sum().nlargest(5).reset_index()
    top_vac = top_vac.sort_values("Job_Availability", ascending=True)

    fig = go.Figure(go.Bar(
        x=top_vac["Job_Availability"],
        y=top_vac["Skill"],
        orientation="h",
        marker_color="#F97316",
        text=[f"{v:,}" for v in top_vac["Job_Availability"]],
        textposition="outside",
    ))
    fig.update_layout(
        template=template,
        height=260,
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis=dict(title="Active Openings", gridcolor=grid_color, color=font_color),
        yaxis=dict(color=font_color),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
    )
    return fig


# REAL ML CHART BUILDERS
def ml_model_comparison_chart_real(comparison_df: pd.DataFrame) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Accuracy (%)", x=comparison_df["Model"], y=comparison_df["Accuracy (%)"], marker_color=BLUE))
    fig.add_trace(go.Bar(name="F1 Score (%)", x=comparison_df["Model"], y=comparison_df["F1 Score (%)"], marker_color=EMERALD))

    fig.update_layout(
        template=template,
        barmode="group",
        height=320,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color=font_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        yaxis=dict(range=[60, 100], title="Score (%)", gridcolor=grid_color, color=font_color),
        xaxis=dict(color=font_color),
    )
    return fig


def ml_confusion_matrix_heatmap_real(cm: np.ndarray, model_name: str = "Random Forest") -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    x = ["Predicted: No Match", "Predicted: High Match"]
    y = ["Actual: No Match", "Actual: High Match"]

    fig = px.imshow(
        cm,
        x=x,
        y=y,
        color_continuous_scale="Greens",
        text_auto=True,
        aspect="auto",
    )
    fig.update_layout(
        template=template,
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        coloraxis_showscale=False,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        xaxis=dict(color=font_color),
        yaxis=dict(color=font_color),
    )
    return fig


def ml_feature_importance_chart_real(fi_df: pd.DataFrame) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    fig = go.Figure(go.Bar(
        x=fi_df["Importance"] * 100,
        y=fi_df["Feature"],
        orientation="h",
        marker_color=EMERALD,
        text=[f"{v*100:.1f}%" for v in fi_df["Importance"]],
        textposition="outside",
    ))
    fig.update_layout(
        template=template,
        height=320,
        margin=dict(l=10, r=30, t=10, b=10),
        xaxis=dict(title="Importance Weight (%)", gridcolor=grid_color, color=font_color),
        yaxis=dict(color=font_color),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
    )
    return fig


def ml_roc_curves_chart_real(ml_results: dict) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    fig = go.Figure()
    colors = {"Random Forest": EMERALD, "Gradient Boosting": BLUE, "Decision Tree": AMBER, "Logistic Regression": "#8B5CF6"}

    for name, m in ml_results["models"].items():
        c = colors.get(name, BLUE)
        fig.add_trace(go.Scatter(
            x=m["fpr"],
            y=m["tpr"],
            mode="lines",
            name=f"{name} (AUC = {m['auc']})",
            line=dict(color=c, width=2.2),
        ))

    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random Baseline", line=dict(color=SLATE_LIGHT, dash="dash")))

    fig.update_layout(
        template=template,
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, font_size=10, font=dict(color=font_color)),
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        xaxis=dict(gridcolor=grid_color, color=font_color),
        yaxis=dict(gridcolor=grid_color, color=font_color),
    )
    return fig


def radar_compare(cmp_df: pd.DataFrame, cities: list) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    metrics = ["Job_Demand_Score", "Healthcare_Score", "Transportation_Score", "Quality_of_Life_Score", "Affordability_Score"]
    labels = ["Job Demand", "Healthcare", "Transport", "Quality of Life", "Affordability"]
    colors = [EMERALD, BLUE, AMBER, ROSE, "#8B5CF6"]

    fig = go.Figure()
    for i, city in enumerate(cities):
        row = cmp_df[cmp_df["City"] == city]
        if row.empty:
            continue
        vals = [float(row[m].values[0]) for m in metrics]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=city,
            line_color=colors[i % len(colors)],
            opacity=0.65,
        ))

    fig.update_layout(
        template=template,
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor=grid_color)),
        height=380,
        margin=dict(t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, font=dict(color=font_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
    )
    return fig


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    bg_color, grid_color, text_color, font_color, template = _get_theme_settings()
    cols = ["Average_Salary", "Average_1BHK_Rent", "Estimated_Monthly_Expenses", "Job_Demand_Score", "Quality_of_Life_Score"]
    corr = df[cols].corr().round(2)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Purples",
        aspect="auto",
    )
    fig.update_layout(
        template=template,
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        xaxis=dict(color=font_color),
        yaxis=dict(color=font_color),
    )
    return fig