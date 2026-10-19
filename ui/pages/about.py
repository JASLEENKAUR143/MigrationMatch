"""About Us & Project Information Page — Professional Overview & Attribution."""
import pandas as pd
import streamlit as st

from ui.components import author_attribution_box, top_header_bar


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("About Project")

    # Hero Banner
    st.markdown(
        """
<div class="mm-card" style="padding: 1.75rem; margin-bottom: 1.5rem; border-left: 4px solid #0D7A5F;">
    <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: #0D7A5F; letter-spacing: 0.08em; margin-bottom: 0.25rem;">
        MINOR PROJECT • BCA (2024–2027)
    </div>
    <div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; letter-spacing: -0.03em; line-height: 1.2;">
        MigrationMatch: Skill-to-City Relocation Platform
    </div>
    <div style="font-size: 0.92rem; color: #475569; margin-top: 0.5rem; max-width: 850px; line-height: 1.6;">
        A Data Science based Decision Support System (DSS) designed to help blue-collar workers and families identify the most suitable Indian cities for relocation through explainable, data-driven recommendations.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # 4-Step "How It Works" Workflow
    st.markdown(
        """
<div class="mm-card" style="margin-bottom: 1.5rem;">
    <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 1rem;">
        How It Works
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; font-size: 0.82rem;">
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #0D7A5F; margin-bottom: 0.35rem;">Step 1</div>
            <strong style="color: #0F172A; font-size: 0.92rem;">Enter Profile</strong>
            <div style="color: #64748B; margin-top: 0.25rem;">Input trade skill, experience level, salary expectation, and rent budget.</div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #0D7A5F; margin-bottom: 0.35rem;">Step 2</div>
            <strong style="color: #0F172A; font-size: 0.92rem;">Data Analytics</strong>
            <div style="color: #64748B; margin-top: 0.25rem;">Multi-dimensional evaluation across 45+ cities for employment, cost of living, and quality of life.</div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #0D7A5F; margin-bottom: 0.35rem;">Step 3</div>
            <strong style="color: #0F172A; font-size: 0.92rem;">Smart Matching</strong>
            <div style="color: #64748B; margin-top: 0.25rem;">Hybrid scoring engine calculates calibrated MigrationMatch scores.</div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #0D7A5F; margin-bottom: 0.35rem;">Step 4</div>
            <strong style="color: #0F172A; font-size: 0.92rem;">Relocation Insights</strong>
            <div style="color: #64748B; margin-top: 0.25rem;">Discover optimal cities with explainable rationale and financial savings projections.</div>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # 4 Data Sources Cards
    st.markdown(
        """
<div class="mm-card" style="margin-bottom: 1.5rem;">
    <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 1rem;">
        Integrated Data Sources
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; font-size: 0.82rem;">
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem;">
            <strong style="color: #0D7A5F;">Jobs & Vacancies Data</strong>
            <div style="color: #64748B; margin-top: 0.2rem;">50,000+ active employment opportunities aggregated across trades.</div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem;">
            <strong style="color: #0D7A5F;">City Socio-Economic Metrics</strong>
            <div style="color: #64748B; margin-top: 0.2rem;">45+ Indian tier 1, tier 2, and industrial hubs with 20+ economic indicators.</div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem;">
            <strong style="color: #0D7A5F;">Skill Demand Index</strong>
            <div style="color: #64748B; margin-top: 0.2rem;">Industry demand index, vacancy counts, and year-over-year expansion rates.</div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem;">
            <strong style="color: #0D7A5F;">Living Cost & Migration Stats</strong>
            <div style="color: #64748B; margin-top: 0.2rem;">Regional salary baselines, rental pricing, and cost-of-living breakdowns.</div>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Project Details (Objectives, Rationale, Methodology)
    col_syn1, col_syn2 = st.columns(2)

    with col_syn1:
        st.markdown(
            """
<div class="mm-card" style="height: 100%;">
    <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A; margin-bottom: 0.5rem;">
        Project Objectives & Rationale
    </div>
    <div style="font-size: 0.84rem; color: #475569; line-height: 1.6;">
        <ul style="padding-left: 1.2rem; margin: 0;">
            <li><strong>Informed Decision Making:</strong> Help internal migrants avoid financial distress and unemployment resulting from uninformed migration decisions.</li>
            <li><strong>Holistic Socio-Economic Analysis:</strong> Integrate salary, rental affordability, food, utilities, transit reliability, healthcare, and safety into a unified index.</li>
            <li><strong>Explainable AI (XAI):</strong> Provide transparent recommendations through the MigrationMatch Score so users understand the key factors behind each suggested destination.</li>
            <li><strong>Interactive Decision Support System:</strong> Equip workers with head-to-head city comparison, savings estimation, and exportable intelligence reports.</li>
        </ul>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_syn2:
        st.markdown(
            """
<div class="mm-card" style="height: 100%;">
    <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A; margin-bottom: 0.5rem;">
        Technology Stack & Architecture
    </div>
    <div style="font-size: 0.84rem; color: #475569; line-height: 1.6;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.5rem;">
            <span class="sector-tag">Python 3.12+</span>
            <span class="sector-tag">Streamlit</span>
            <span class="sector-tag">Pandas & NumPy</span>
            <span class="sector-tag">Scikit-Learn</span>
            <span class="sector-tag">Plotly Express</span>
            <span class="sector-tag">SQLite / CSV Data</span>
            <span class="sector-tag">Joblib</span>
        </div>
        <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #64748B;">
            System Pipeline: Data Preprocessing $\\rightarrow$ Exploratory Data Analysis (EDA) $\\rightarrow$ Feature Engineering $\\rightarrow$ Random Forest Classifier & Hybrid Recommender $\\rightarrow$ Streamlit Decision Support UI.
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # Attribution Box in the bottom right corner
    author_attribution_box()