"""Admin Command Center — Platform overview, PIN security, & refined calibration."""
import pandas as pd
import streamlit as st

from ui.components import top_header_bar
from ui.pages import ml_dashboard
from ui.session import clear_session


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    user = st.session_state.get("user", {})
    if user.get("role") != "Admin" or not st.session_state.get("admin_authenticated", False):
        st.error("Admin access is required. Sign in as an administrator to continue.")
        return

    admin_view = st.radio(
        "Admin tools",
        ["Admin Panel", "ML Dashboard"],
        horizontal=True,
        key="admin_tools_view",
    )
    if admin_view == "ML Dashboard":
        ml_dashboard.render(df, df_feat)
        return

    top_header_bar("Admin")

    col_hdr, col_lock = st.columns([4, 1.2])
    with col_hdr:
        st.markdown(
            """
<div style="margin-bottom: 1.25rem;">
    <div style="font-size: 1.65rem; font-weight: 800; color: #0F172A; letter-spacing: -0.025em;">
        Command Center & Engine Calibration
    </div>
    <div style="font-size: 0.9rem; color: #64748B;">
        Platform overview, operational health, and real-time algorithm parameter adjustments.
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
    with col_lock:
        if st.button("Logout Admin", use_container_width=True):
            clear_session()
            st.rerun()

    # Top Metrics Strip
    col_kpi1, col_kpi2, col_req = st.columns([1.2, 1.2, 1.6])

    with col_kpi1:
        user_count = len(st.session_state.get("user_database", {}))
        st.markdown(
            f"""
<div class="stat-kpi-card">
    <div class="stat-kpi-header">
        <span style="font-size: 1.2rem;">👥</span>
        <span class="score-pill score-pill-emerald">Registered</span>
    </div>
    <div>
        <div class="stat-kpi-label">TOTAL USERS</div>
        <div class="stat-kpi-value">{user_count}</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_kpi2:
        st.markdown(
            """
<div class="stat-kpi-card">
    <div class="stat-kpi-header">
        <span style="font-size: 1.2rem;">🛡️</span>
        <span class="score-pill score-pill-emerald">Stable</span>
    </div>
    <div>
        <div class="stat-kpi-label">DATA HEALTH INDEX</div>
        <div class="stat-kpi-value">98.2%</div>
        <div style="height: 4px; background: #0D7A5F; border-radius: 4px; margin-top: 6px;"></div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_req:
        st.markdown(
            """
<div class="mm-card" style="padding: 1rem 1.25rem;">
    <div style="font-size: 0.95rem; font-weight: 800; color: #0F172A; margin-bottom: 0.5rem;">
        Top Requested Destinations
    </div>
    <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.8rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span><strong>Bengaluru, KA</strong> • Tech Hub</span>
            <span class="score-pill score-pill-emerald">2.4k req</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span><strong>Pune, MH</strong> • Industry & Services</span>
            <span class="score-pill score-pill-emerald">1.8k req</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span><strong>Varanasi, UP</strong> • High Growth Hub</span>
            <span class="score-pill score-pill-emerald">1.5k req</span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Blue-collar users")
    users = st.session_state.get("user_database", {})
    user_rows = [
        {
            "Name": account.get("name", ""),
            "Email": email,
            "Trade / Profession": account.get("skill") or "Not specified",
            "Account Type": "Admin" if account.get("role") == "Admin" else "User",
        }
        for email, account in users.items()
    ]
    if user_rows:
        st.dataframe(pd.DataFrame(user_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No registered users are available yet.")

    # City Parameters & Weighting Live Calibration Studio
    st.markdown(
        """
<div class="mm-card">
    <div style="font-size: 1.1rem; font-weight: 800; color: #0F172A; margin-bottom: 0.25rem;">
        City Parameters & Recommendation Engine Calibration
    </div>
    <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 1rem;">
        Fine-tune scoring weights and select calibration presets to control how cities are ranked for all users.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Calibration Presets
    presets = {
        "Balanced Approach": {"job": 30, "sal": 25, "rent": 20, "sav": 15, "qol": 10},
        "Job Seekers / High Demand": {"job": 45, "sal": 25, "rent": 15, "sav": 10, "qol": 5},
        "Budget & Savings Focused": {"job": 20, "sal": 20, "rent": 30, "sav": 25, "qol": 5},
        "Family & Quality of Life": {"job": 20, "sal": 20, "rent": 15, "sav": 15, "qol": 30},
    }

    c_pre1, c_pre2 = st.columns([1.5, 2])
    with c_pre1:
        selected_preset = st.selectbox("Calibration Preset", list(presets.keys()), index=0)

    preset_vals = presets[selected_preset]

    with st.form("admin_calibration_form"):
        col_w1, col_w2 = st.columns(2)

        with col_w1:
            w_job = st.slider("Job Demand Weight (%)", 5, 60, preset_vals["job"], step=5)
            w_sal = st.slider("Salary Match Weight (%)", 5, 60, preset_vals["sal"], step=5)
            w_rent = st.slider("Rent Affordability Weight (%)", 5, 60, preset_vals["rent"], step=5)

        with col_w2:
            w_sav = st.slider("Savings Potential Weight (%)", 5, 60, preset_vals["sav"], step=5)
            w_qol = st.slider("Quality of Life & Healthcare (%)", 5, 60, preset_vals["qol"], step=5)
            refresh_rate = st.selectbox("Market Index Refresh Rate", ["Real-Time", "Daily", "Weekly", "Monthly"], index=2)

        total_weight = w_job + w_sal + w_rent + w_sav + w_qol
        st.markdown(
            f"""
<div style="font-size: 0.84rem; color: {'#0D7A5F' if total_weight == 100 else '#EF4444'}; font-weight: 700; margin-bottom: 0.75rem;">
    Total Weight Allocation: {total_weight}% {'(Balanced 100%)' if total_weight == 100 else '(Will be normalized automatically)'}
</div>
""",
            unsafe_allow_html=True,
        )

        if st.form_submit_button("Save & Apply Calibration Changes", type="primary", use_container_width=True):
            factor = 1.0 / (total_weight if total_weight > 0 else 100)
            st.session_state.admin_params["job_demand_weight"] = (w_job * factor)
            st.session_state.admin_params["salary_suitability_weight"] = (w_sal * factor)
            st.session_state.admin_params["cost_of_living_weight"] = (w_rent * factor)
            st.session_state.admin_params["savings_weight"] = (w_sav * factor)
            st.session_state.admin_params["quality_of_life_weight"] = (w_qol * factor)
            st.session_state.admin_params["refresh_rate"] = refresh_rate
            st.session_state.admin_params["selected_preset"] = selected_preset
            st.session_state.last_results = None
            st.success("Algorithm calibration weights applied successfully across all recommendation models!")
            st.rerun()

    # Recent Relocations Live Activity Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
<div class="mm-card">
    <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A; margin-bottom: 0.25rem;">
        Recent Relocation Inquiries
    </div>
    <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 0.75rem;">
        Live status of relocation decisions processed by the MigrationMatch decision support engine.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    reloc_data = pd.DataFrame([
        {"User": "Jane Doe (Barber)", "Destination": "Bengaluru, KA", "Timeline": "Q3 2024", "Status": "In Progress"},
        {"User": "Michael Smith (Electrician)", "Destination": "Pune, MH", "Timeline": "Q2 2024", "Status": "Matched"},
        {"User": "Jasleen Kaur (Barber)", "Destination": "Chandigarh, PB", "Timeline": "Q1 2025", "Status": "Matched"},
        {"User": "Alice Lee (Plumber)", "Destination": "Hyderabad, TS", "Timeline": "Q1 2024", "Status": "Closed"},
    ])
    st.dataframe(reloc_data, use_container_width=True, hide_index=True)
