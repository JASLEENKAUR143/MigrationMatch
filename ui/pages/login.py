"""User and administrator login and registration."""
import re

import streamlit as st

from data.database import load_users, save_user, verify_password

BLUE_COLLAR_PROFESSIONS = [
    "Barber",
    "Electrician",
    "Plumber",
    "AC Technician",
    "Mechanic",
    "Driver",
    "Factory Worker",
    "Carpenter",
    "Welder",
    "Painter",
    "Mason",
    "Other",
]


def _sign_in_user(email: str, user_info: dict) -> None:
    st.session_state.user.update(
        {
            "name": user_info["name"],
            "email": email,
            "role": "Blue-collar worker",
            "skill": user_info.get("skill") or "Other",
            "is_logged_in": True,
        }
    )
    st.session_state.admin_authenticated = False
    if user_info.get("skill"):
        st.session_state.inputs["skill"] = user_info["skill"]
    st.session_state.nav_page = "Dashboard"
    st.rerun()


def render(df=None, df_feat=None) -> None:
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 1.4, 1])
    with col_center:
        st.markdown(
            """
<div class="mm-card" style="padding: 2rem 1.75rem; text-align: center; border-radius: 16px;">
    <div style="width: 50px; height: 50px; background: #0D7A5F; color: white; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; margin: 0 auto 0.75rem auto; box-shadow: 0 4px 12px rgba(13, 122, 95, 0.25);">
        📍
    </div>
    <div style="font-size: 1.45rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">
        MigrationMatch
    </div>
    <div style="font-size: 0.72rem; color: #0D7A5F; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.25rem;">
        Skill-to-City Relocation Platform
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        login_tab, register_tab = st.tabs(["Login / Switch User", "Create User Account"])

        with login_tab:
            account_type = st.radio(
                "Sign in as",
                ["User", "Admin"],
                horizontal=True,
                key="login_account_type",
            )

            if account_type == "Admin":
                with st.form("admin_login_form"):
                    admin_pin = st.text_input("Administrator PIN", type="password")
                    if st.form_submit_button(
                        "Sign In as Admin", type="primary", use_container_width=True
                    ):
                        if admin_pin == st.session_state.get("admin_pin", "1234"):
                            st.session_state.user.update(
                                {
                                    "name": "Administrator",
                                    "email": "admin@migrationmatch.local",
                                    "role": "Admin",
                                    "is_logged_in": True,
                                }
                            )
                            st.session_state.admin_authenticated = True
                            st.session_state.nav_page = "Admin"
                            st.rerun()
                        st.error("Invalid administrator PIN.")
            else:
                with st.form("user_login_form"):
                    email = st.text_input(
                        "Email Address",
                        value=st.session_state.user.get("email", ""),
                    ).strip().lower()
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button(
                        "Sign In as User", type="primary", use_container_width=True
                    ):
                        user_info = st.session_state.get("user_database", {}).get(email)
                        if user_info and verify_password(
                            password, user_info.get("password_hash", "")
                        ):
                            _sign_in_user(email, user_info)
                        st.error("Email or password is incorrect.")

        with register_tab:
            with st.form("user_register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. Your name")
                reg_email = st.text_input("Email Address", placeholder="name@example.com")
                reg_skill = st.selectbox(
                    "Blue-collar trade / profession", BLUE_COLLAR_PROFESSIONS
                )
                reg_password = st.text_input(
                    "Create Password", type="password", placeholder="At least 6 characters"
                )

                if st.form_submit_button(
                    "Create User Account", type="primary", use_container_width=True
                ):
                    normalized_email = reg_email.strip().lower()
                    if not reg_name.strip():
                        st.error("Enter your full name.")
                    elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized_email):
                        st.error("Enter a valid email address.")
                    elif len(reg_password) < 6:
                        st.error("Your password must contain at least 6 characters.")
                    elif normalized_email in st.session_state.user_database:
                        st.error("An account with this email already exists.")
                    else:
                        role = "Blue-collar worker"
                        save_user(
                            normalized_email,
                            reg_name.strip(),
                            role,
                            reg_skill,
                            reg_password,
                        )
                        st.session_state.user_database = load_users()
                        st.session_state.user.update(
                            {
                                "name": reg_name.strip(),
                                "email": normalized_email,
                                "role": role,
                                "skill": reg_skill,
                                "is_logged_in": True,
                            }
                        )
                        st.session_state.admin_authenticated = False
                        st.session_state.inputs["skill"] = reg_skill
                        st.session_state.nav_page = "Dashboard"
                        st.success(f"Welcome to MigrationMatch, {reg_name.strip()}!")
                        st.rerun()

        st.caption("Demo user account: jasleen@gmail.com · Password: password")
