"""Sidebar navigation for MigrationMatch — Professional & Classy."""
import streamlit as st

from ui.session import clear_session

# Exact requested navigation items and order
NAV_ITEMS = [
    ("Dashboard", "Dashboard"),
    ("My Profile", "My Profile"),
    ("Get Recommendations", "Get Recommendations"),
    ("Search and Compare", "Search and Compare"),
    ("City Explorer", "City Explorer"),
    ("Market Analysis", "Market Analysis"),
    ("Saved Results", "Saved Results"),
    ("Search History", "Search History"),
    ("Report Generator", "Report Generator"),
    ("About Project", "About Project"),
]
NAV_EMOJI = {
    "Dashboard": "🏠", "My Profile": "👤", "Get Recommendations": "🎯",
    "Search and Compare": "⚖️", "City Explorer": "🏙️", "Market Analysis": "📊",
    "Saved Results": "🔖", "Search History": "🕘",
    "Report Generator": "📄", "Admin": "⚙️", "About Project": "💡",
}


def render_sidebar() -> str:
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Dashboard"

    with st.sidebar:
        st.markdown(
            """
<div class="sidebar-logo-container">
    <div class="sidebar-logo-icon">📍</div>
    <div class="sidebar-logo-text">
        <span class="sidebar-logo-title">MigrationMatch</span>
        <span class="sidebar-logo-sub">Skill-to-City Relocation Platform</span>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button("+ New Relocation Plan", type="primary", use_container_width=True):
            st.session_state.nav_page = "Get Recommendations"
            st.rerun()

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        user = st.session_state.get("user", {})
        is_admin = user.get("is_logged_in", False) and user.get("role") == "Admin"
        keys = [k for k, _ in NAV_ITEMS]
        if is_admin:
            keys.insert(-1, "Admin")
        curr_page = st.session_state.nav_page
        if curr_page == "Get Recommendation":
            curr_page = "Get Recommendations"
        elif curr_page == "Search & Compare":
            curr_page = "Search and Compare"
        elif curr_page == "Analytics":
            curr_page = "Market Analysis"
        elif curr_page == "History":
            curr_page = "Search History"
        elif curr_page == "About Us":
            curr_page = "About Project"
        elif curr_page == "ML Dashboard":
            curr_page = "Admin" if is_admin else "Dashboard"

        if curr_page == "Admin" and not is_admin:
            curr_page = "Dashboard"
            st.session_state.nav_page = curr_page

        st.markdown('<div class="sidebar-nav-title">EXPLORE</div>', unsafe_allow_html=True)
        for key in keys:
            selected = key == curr_page
            label = f"{NAV_EMOJI[key]}  {key}"
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if selected else "secondary",
            ):
                st.session_state.nav_page = key
                st.rerun()

        st.markdown("---")

        user = st.session_state.get("user", {"name": "Jasleen Kaur", "is_logged_in": True})
        is_logged_in = user.get("is_logged_in", True)

        if is_logged_in:
            if st.button("Logout / Switch User", use_container_width=True):
                clear_session()
                st.rerun()
        else:
            if st.button("Sign In / Register", type="primary", use_container_width=True):
                st.session_state.nav_page = "Login"
                st.rerun()

        st.markdown(
            """
<div style="font-size: 0.72rem; color: #94A3B8; text-align: center; margin-top: 1.25rem;">
    MigrationMatch • PCTE BCA Project<br>
    Developed by <strong>Jasleen Kaur</strong>
</div>
""",
            unsafe_allow_html=True,
        )

    return st.session_state.nav_page
