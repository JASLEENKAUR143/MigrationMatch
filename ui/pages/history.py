"""Search History Timeline Page — Professional & Classy."""
import pandas as pd
import streamlit as st

from ui.components import top_header_bar


def render(df: pd.DataFrame, df_feat: pd.DataFrame) -> None:
    top_header_bar("Search History")

    st.markdown(
        """
<div style="margin-bottom: 1.25rem;">
    <div style="font-size: 1.65rem; font-weight: 800; color: #0F172A; letter-spacing: -0.025em;">
        Search History & Queries Log
    </div>
    <div style="font-size: 0.9rem; color: #64748B;">
        A chronological record of your past skill-to-city evaluations. Review parameters and rerun previous queries.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    history = st.session_state.get("search_history", [])

    for i, item in enumerate(history):
        st.markdown(
            f"""
<div style="display: flex; gap: 16px; align-items: flex-start; margin-bottom: 1.25rem;">
    <div style="width: 100px; font-weight: 800; font-size: 0.8rem; color: #0D7A5F; padding-top: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">
        ● {item.get('timeframe', 'Today')}
    </div>
    <div class="history-timeline-card" style="flex: 1;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <div style="font-size: 1.05rem; font-weight: 800; color: #0F172A;">
                {item.get('title', 'Skill Query')}
            </div>
        </div>
        <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 0.75rem;">
            Parameters: {item.get('params', 'Standard evaluation')}
        </div>
        <div class="history-top-pill">
            <div style="font-size: 0.82rem;">
                <span style="color: #64748B; font-weight: 600; text-transform: uppercase; font-size: 0.7rem;">TOP RECOMMENDATION</span><br>
                <strong style="color: #0F172A; font-size: 0.95rem;">{item.get('top_city', 'Varanasi')}</strong>
            </div>
            <span class="score-pill score-pill-emerald">Score {item.get('top_score', 100)}/100</span>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        col_dummy, col_btn = st.columns([4, 1.2])
        with col_btn:
            if st.button(f"Rerun Query #{i+1}", key=f"rerun_hist_{i}", use_container_width=True):
                st.session_state.inputs["skill"] = item.get("skill", "Electrician")
                st.session_state.inputs["expected_salary"] = item.get("salary", 25000)
                st.session_state.inputs["max_rent"] = item.get("rent", 8000)
                st.session_state.last_results = None
                st.session_state.nav_page = "Get Recommendations"
                st.rerun()

    st.markdown(
        """
<div style="text-align: center; color: #94A3B8; font-size: 0.85rem; margin-top: 2rem;">
    End of recorded query history.
</div>
""",
        unsafe_allow_html=True,
    )