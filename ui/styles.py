"""Global CSS & Design System for MigrationMatch — Classy Emerald & Slate Theme."""
import streamlit as st

BRAND_EMERALD = "#0D7A5F"
BRAND_EMERALD_DARK = "#084C3B"
BRAND_EMERALD_LIGHT = "#E6F4EA"
BRAND_EMERALD_BORDER = "#A7F3D0"
BRAND_TEAL = "#059669"

GRAY_50 = "#F8FAFC"
GRAY_100 = "#F1F5F9"
GRAY_200 = "#E2E8F0"
GRAY_300 = "#CBD5E1"
GRAY_400 = "#94A3B8"
GRAY_500 = "#64748B"
GRAY_600 = "#475569"
GRAY_700 = "#334155"
GRAY_800 = "#1E293B"
GRAY_900 = "#0F172A"


def inject_styles() -> None:
    theme = st.session_state.get("theme", "Light")
    is_dark = theme == "Dark"

    bg_color = "#0B1120" if is_dark else GRAY_50
    card_bg = "#131E32" if is_dark else "#FFFFFF"
    text_primary = "#F8FAFC" if is_dark else GRAY_900
    text_secondary = "#94A3B8" if is_dark else GRAY_600
    border_color = "#1E293B" if is_dark else GRAY_200
    input_bg = "#1A263D" if is_dark else "#FFFFFF"
    subcard_bg = "#1E293B" if is_dark else GRAY_50

    st.markdown(
        f"""
<style>
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --subcard-bg: {subcard_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    --input-bg: {input_bg};
    --brand-emerald: {BRAND_EMERALD};
    --brand-emerald-dark: {BRAND_EMERALD_DARK};
    --brand-emerald-light: {BRAND_EMERALD_LIGHT};
    --focus-ring: {'#34D399' if is_dark else BRAND_EMERALD};
    color-scheme: {'dark' if is_dark else 'light'};
}}

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, .stText {{
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {text_primary};
    line-height: 1.55;
    background-color: {bg_color} !important;
}}

.stApp {{
    background-color: {bg_color} !important;
    color: {text_primary} !important;
}}

/* Streamlit and BaseWeb surfaces need explicit theme tokens. */
section[data-testid="stSidebar"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="dialog"],
[data-testid="stDialog"],
[data-testid="stModal"] {{
    background-color: {card_bg} !important;
    color: {text_primary} !important;
}}

[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="stForm"],
[data-testid="stExpander"],
[data-testid="stAlert"],
[data-testid="stNotification"] {{
    color: {text_primary};
}}

[data-baseweb="select"] *,
[data-baseweb="menu"] *,
[role="dialog"] *,
[data-testid="stDialog"] * {{
    color: {text_primary} !important;
}}

[data-baseweb="menu"] li:hover,
[data-baseweb="option"]:hover {{
    background-color: {subcard_bg} !important;
}}

[data-testid="stMarkdownContainer"] a {{
    color: {'#6EE7B7' if is_dark else BRAND_EMERALD} !important;
}}

[data-testid="stAlert"] {{
    background-color: {subcard_bg} !important;
    border: 1px solid {border_color} !important;
}}

/* Normalize Streamlit controls and legacy inline colors in dark mode. */
input, textarea, [data-baseweb="select"] > div {{
    background-color: {input_bg} !important;
    color: {text_primary} !important;
    border-color: {border_color} !important;
}}

input::placeholder, textarea::placeholder {{
    color: {text_secondary} !important;
    opacity: 1 !important;
}}

[data-testid="stSlider"] [role="slider"] {{
    background-color: {'#34D399' if is_dark else BRAND_EMERALD} !important;
}}

[data-testid="stTabs"] [role="tab"] {{
    color: {text_secondary} !important;
}}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    color: {'#6EE7B7' if is_dark else BRAND_EMERALD_DARK} !important;
}}

button:focus-visible, input:focus-visible, textarea:focus-visible {{
    outline: 2px solid var(--focus-ring) !important;
    outline-offset: 2px;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {border_color};
    border-radius: 12px;
    overflow: hidden;
}}

/* No page in the product exposes source code; suppress accidental code previews. */
[data-testid="stCodeBlock"] {{
    display: none !important;
}}

/* Inline legacy colors should still respect the active theme. */
[style*="#0F172A"], [style*="#0f172a"] {{ color: {text_primary} !important; }}
[style*="#475569"], [style*="#64748B"], [style*="#64748b"] {{ color: {text_secondary} !important; }}
[style*="#F8FAFC"], [style*="#f8fafc"] {{ background-color: {subcard_bg} !important; }}

/* Ensure all text inside markdown and cards adapts to theme */
p, span, div, h1, h2, h3, h4, h5, h6, label, strong {{
    color: inherit;
}}

.block-container {{
    padding-top: 1.8rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1400px !important;
}}

.dashboard-hero {{
    display: flex;
    align-items: stretch;
    justify-content: space-between;
    min-height: 265px;
    margin: 0 0 1.5rem;
    padding: 2rem 2.25rem;
    overflow: hidden;
    border: 1px solid {'#1F7663' if is_dark else '#B7E6D5'};
    border-radius: 24px;
    background:
        radial-gradient(circle at 85% 25%, rgba(52, 211, 153, .18), transparent 28%),
        linear-gradient(115deg, {'#102A32' if is_dark else '#073B37'} 0%, {'#0B1725' if is_dark else '#0D7A5F'} 100%);
    box-shadow: 0 16px 35px rgba(2, 44, 40, .16);
}}

.dashboard-hero-copy {{ max-width: 670px; position: relative; z-index: 2; }}
.dashboard-eyebrow {{
    color: #6EE7B7;
    font-size: .7rem;
    font-weight: 800;
    letter-spacing: .14em;
    margin-bottom: .8rem;
}}
.dashboard-hero h1 {{
    color: #FFFFFF !important;
    font-size: clamp(2rem, 4vw, 3.25rem);
    line-height: 1.05;
    letter-spacing: -.055em;
    margin: 0 0 .85rem;
}}
.dashboard-hero h1 span {{ color: #6EE7B7 !important; }}
.dashboard-hero p {{
    max-width: 590px;
    color: rgba(255,255,255,.76) !important;
    font-size: .96rem;
    margin: 0 0 1.25rem;
}}
.dashboard-hero-pills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.dashboard-hero-pills span {{
    padding: .42rem .7rem;
    border: 1px solid rgba(167,243,208,.28);
    border-radius: 999px;
    color: #D1FAE5 !important;
    background: rgba(255,255,255,.08);
    font-size: .72rem;
    font-weight: 700;
}}
.dashboard-hero-art {{ width: 280px; position: relative; min-width: 220px; }}
.hero-orbit {{
    position: absolute;
    border: 1px solid rgba(110,231,183,.25);
    border-radius: 50%;
    transform: rotate(-18deg);
}}
.hero-orbit-one {{ width: 250px; height: 130px; top: 30px; right: -20px; }}
.hero-orbit-two {{ width: 210px; height: 105px; top: 45px; right: 0; transform: rotate(28deg); }}
.hero-pin {{
    position: absolute;
    top: 65px;
    right: 105px;
    display: grid;
    place-items: center;
    width: 64px;
    height: 64px;
    border: 8px solid rgba(255,255,255,.12);
    border-radius: 50%;
    background: #10B981;
    font-size: 1.55rem;
    box-shadow: 0 0 0 12px rgba(16,185,129,.12), 0 10px 25px rgba(0,0,0,.25);
}}
.hero-city-label {{
    position: absolute;
    padding: .35rem .6rem;
    border: 1px solid rgba(167,243,208,.3);
    border-radius: 7px;
    color: #ECFDF5 !important;
    background: rgba(3, 35, 33, .6);
    font-size: .68rem;
    font-weight: 700;
}}
.hero-city-one {{ top: 20px; right: 20px; }}
.hero-city-two {{ top: 178px; right: 15px; }}
.hero-city-three {{ top: 132px; left: 8px; }}

@media (max-width: 760px) {{
    .dashboard-hero {{ padding: 1.5rem; }}
    .dashboard-hero-art {{ display: none; }}
}}

/* Keep the product polished on tablets and narrow browser windows. */
@media (max-width: 900px) {{
    .block-container {{ padding-left: 1rem !important; padding-right: 1rem !important; }}
    .top-header-bar {{ margin-bottom: 1rem; }}
}}

@media (max-width: 640px) {{
    .block-container {{ padding-top: 1rem !important; }}
    .stat-kpi-value {{ font-size: 1.2rem; }}
    .city-explorer-card {{ margin-bottom: 0.75rem; }}
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: {'#131E32' if is_dark else GRAY_100};
}}
::-webkit-scrollbar-thumb {{
    background: {'#334155' if is_dark else GRAY_300};
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {'#475569' if is_dark else GRAY_400};
}}

/* Sidebar Styling */
section[data-testid="stSidebar"] {{
    background: {card_bg} !important;
    border-right: 1px solid {border_color} !important;
    box-shadow: 2px 0 10px rgba(0, 0, 0, {'0.3' if is_dark else '0.02'}) !important;
}}

section[data-testid="stSidebar"] .block-container {{
    padding-top: 1.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}}

.sidebar-logo-container {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.25rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid {border_color};
}}

.sidebar-logo-icon {{
    background: {BRAND_EMERALD};
    color: white;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    box-shadow: 0 3px 8px rgba(13, 122, 95, 0.25);
}}

.sidebar-logo-text {{
    display: flex;
    flex-direction: column;
}}

.sidebar-nav-title {{
    margin: .9rem 0 .45rem;
    color: {text_secondary} !important;
    font-size: .65rem;
    font-weight: 800;
    letter-spacing: .12em;
}}

section[data-testid="stSidebar"] .stButton > button {{
    text-align: left !important;
    min-height: 2.35rem;
    margin: .12rem 0;
}}

.sidebar-logo-title {{
    font-size: 1.12rem;
    font-weight: 800;
    color: {text_primary};
    letter-spacing: -0.02em;
    line-height: 1.2;
}}

.sidebar-logo-sub {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {BRAND_EMERALD};
    font-weight: 700;
}}

/* REMOVE RADIO BULLET / TICK COMPLETELY ON SIDEBAR NAVIGATION */
[data-testid="stSidebar"] [data-testid="stRadioButton"] input[type="radio"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child,
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {{
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    visibility: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
    gap: 4px !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 0.55rem 0.85rem !important;
    margin-bottom: 2px !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {{
    background: {'#1E2D48' if is_dark else GRAY_100} !important;
    border-color: {border_color} !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {{
    background: {'#0A382A' if is_dark else BRAND_EMERALD_LIGHT} !important;
    border-color: {BRAND_EMERALD_BORDER if not is_dark else BRAND_EMERALD} !important;
}}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) div {{
    color: {'#34D399' if is_dark else BRAND_EMERALD_DARK} !important;
    font-weight: 700 !important;
}}

/* Top Header Bar */
.top-header-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 0.65rem 1.25rem;
    margin-top: 0.5rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,{'0.2' if is_dark else '0.03'});
}}

.top-user-chip {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: {subcard_bg};
    border: 1px solid {border_color};
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    font-size: 0.84rem;
    font-weight: 600;
    color: {text_primary};
}}

.top-user-avatar {{
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: {BRAND_EMERALD};
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
}}

/* Main Card Containers */
.mm-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, {'0.2' if is_dark else '0.03'});
    transition: all 0.2s ease;
    margin-bottom: 1rem;
}}

.mm-card:hover {{
    box-shadow: 0 4px 12px rgba(0, 0, 0, {'0.3' if is_dark else '0.06'});
    border-color: {'#334155' if is_dark else GRAY_300};
}}

.stat-kpi-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, {'0.2' if is_dark else '0.03'});
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}}

.stat-kpi-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}}

.stat-kpi-value {{
    font-size: 1.5rem;
    font-weight: 800;
    color: {text_primary};
    line-height: 1.1;
    margin-bottom: 0.2rem;
}}

.stat-kpi-label {{
    font-size: 0.75rem;
    font-weight: 600;
    color: {text_secondary};
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

/* Featured Hero City Card */
.featured-hero-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    box-shadow: 0 2px 8px rgba(0, 0, 0, {'0.2' if is_dark else '0.04'});
    margin-bottom: 1.5rem;
}}

.featured-hero-img {{
    width: 38%;
    min-height: 210px;
    background-size: cover;
    background-position: center;
    position: relative;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}}

.featured-hero-img::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.75) 100%);
}}

.featured-hero-city-title {{
    position: relative;
    z-index: 2;
    color: #FFFFFF;
    font-size: 1.45rem;
    font-weight: 800;
}}

.featured-hero-city-sub {{
    position: relative;
    z-index: 2;
    color: rgba(255,255,255,0.85);
    font-size: 0.82rem;
}}

.featured-hero-content {{
    width: 62%;
    padding: 1.35rem 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

/* Score Radial and Pills */
.score-pill {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 0.2rem 0.6rem;
    border-radius: 16px;
    font-size: 0.76rem;
    font-weight: 700;
}}

.score-pill-emerald {{
    background: {'#0A382A' if is_dark else BRAND_EMERALD_LIGHT};
    color: {'#34D399' if is_dark else BRAND_EMERALD_DARK};
    border: 1px solid {'#0D7A5F' if is_dark else BRAND_EMERALD_BORDER};
}}

.score-radial {{
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 3px solid {BRAND_EMERALD};
    background: {'#0A382A' if is_dark else BRAND_EMERALD_LIGHT};
    color: {'#34D399' if is_dark else BRAND_EMERALD_DARK};
    font-weight: 800;
    font-size: 0.92rem;
    line-height: 1;
}}

.score-radial span {{
    font-size: 0.52rem;
    font-weight: 600;
    color: {text_secondary};
}}

/* City Explorer Card */
.city-explorer-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.2s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}}

.city-explorer-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, {'0.3' if is_dark else '0.06'});
    border-color: {BRAND_EMERALD};
}}

.city-card-header-img {{
    height: 125px;
    background-size: cover;
    background-position: center;
    position: relative;
    padding: 0.65rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.city-card-header-img::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.65) 100%);
}}

.city-card-city-name {{
    position: absolute;
    bottom: 0.65rem;
    left: 0.65rem;
    color: #FFFFFF;
    font-size: 1.1rem;
    font-weight: 800;
    z-index: 2;
    text-shadow: 0 1px 3px rgba(0,0,0,0.5);
}}

.city-card-location {{
    position: absolute;
    bottom: 0.15rem;
    left: 0.65rem;
    color: rgba(255,255,255,0.85);
    font-size: 0.7rem;
    z-index: 2;
}}

.city-card-body {{
    padding: 0.9rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.sector-tag {{
    display: inline-block;
    background: {subcard_bg};
    color: {text_primary};
    border: 1px solid {border_color};
    font-size: 0.68rem;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    margin-right: 4px;
    margin-bottom: 4px;
}}

/* Timeline History Card */
.history-timeline-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}}

.history-timeline-card:hover {{
    border-color: {BRAND_EMERALD};
    box-shadow: 0 4px 12px rgba(0,0,0,{'0.2' if is_dark else '0.04'});
}}

.history-top-pill {{
    background: {subcard_bg};
    border: 1px solid {border_color};
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.6rem;
}}

/* Document Report Container */
.report-sheet {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 1.75rem 2rem;
    box-shadow: 0 3px 12px rgba(0,0,0,{'0.25' if is_dark else '0.04'});
    font-size: 0.88rem;
    color: {text_primary};
}}

.profile-card {{
    text-align: center;
    padding: 1.5rem 1.25rem;
}}

.profile-avatar {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, {BRAND_EMERALD} 0%, #10B981 100%);
    color: #FFFFFF;
    font-size: 1.6rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.75rem auto;
}}

.profile-name {{ font-size: 1.25rem; font-weight: 800; margin-bottom: 0.2rem; }}
.profile-role {{ color: {BRAND_EMERALD}; font-size: 0.8rem; font-weight: 700; margin-bottom: 0.35rem; }}
.profile-email {{ color: {text_secondary}; font-size: 0.82rem; margin-bottom: 1rem; }}
.profile-details {{
    background: {subcard_bg};
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: left;
    line-height: 1.6;
}}

/* Author Attribution Card */
.author-attribution-card {{
    background: linear-gradient(135deg, {card_bg} 0%, {'#0A382A' if is_dark else BRAND_EMERALD_LIGHT} 100%);
    border: 1px solid {'#0D7A5F' if is_dark else BRAND_EMERALD_BORDER};
    border-radius: 12px;
    padding: 1.1rem 1.35rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2rem;
}}

.author-name-tag {{
    font-size: 1.1rem;
    font-weight: 800;
    color: {'#34D399' if is_dark else BRAND_EMERALD_DARK};
}}

.author-details-sub {{
    font-size: 0.8rem;
    color: {text_secondary};
}}

/* Buttons */
.stButton > button {{
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 0.95rem !important;
    transition: all 0.15s ease !important;
}}

.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] {{
    border-radius: 9px !important;
}}

.stButton > button[kind="primary"] {{
    background-color: {BRAND_EMERALD} !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(13, 122, 95, 0.25) !important;
}}

.stButton > button[kind="primary"]:hover {{
    background-color: {BRAND_EMERALD_DARK} !important;
}}

.stButton > button[kind="secondary"] {{
    background-color: {input_bg} !important;
    border: 1px solid {border_color} !important;
    color: {text_primary} !important;
}}

.stButton > button[kind="secondary"]:hover {{
    border-color: {BRAND_EMERALD} !important;
    color: {BRAND_EMERALD} !important;
}}

/* Inputs & Selects */
.stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput input {{
    background-color: {input_bg} !important;
    color: {text_primary} !important;
    border-color: {border_color} !important;
}}

/* Headers */
.page-title {{
    font-size: 1.55rem;
    font-weight: 800;
    color: {text_primary};
    letter-spacing: -0.025em;
    margin-bottom: 0.15rem;
}}

.page-subtitle {{
    font-size: 0.88rem;
    color: {text_secondary};
    margin-bottom: 1.15rem;
    font-weight: 400;
}}

.section-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {text_primary};
    margin: 1.15rem 0 0.65rem 0;
    letter-spacing: -0.01em;
}}
</style>
""",
        unsafe_allow_html=True,
    )
