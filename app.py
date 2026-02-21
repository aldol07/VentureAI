import streamlit as st
import json
from pathlib import Path

from core.idea_refiner import IdeaRefiner
from core.mentor_engine import MentorEngine
from core.scoring_engine import ScoringEngine
from core.prototype_router import PrototypeRouter

# Page configuration
st.set_page_config(
    page_title="VenturePilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_theme_css(is_dark: bool) -> str:
    """Generate theme-aware CSS."""
    if is_dark:
        return """
        <style>
            /* Dark Theme Variables */
            :root {
                --bg-primary: #0e1117;
                --bg-secondary: #1a1d24;
                --bg-card: #21262d;
                --text-primary: #e6edf3;
                --text-secondary: #8b949e;
                --accent-primary: #7c3aed;
                --accent-secondary: #a855f7;
                --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%);
                --border-color: #30363d;
                --success-bg: #1a3d2e;
                --success-border: #238636;
                --warning-bg: #3d2e1a;
                --warning-border: #d29922;
                --info-bg: #1a2d3d;
                --info-border: #388bfd;
                --shadow-color: rgba(0, 0, 0, 0.4);
                --glow-color: rgba(124, 58, 237, 0.3);
            }
            
            /* Global Styles */
            .stApp {
                background: var(--bg-primary) !important;
            }
            
            .main .block-container {
                background: var(--bg-primary);
                padding-top: 2rem;
            }
            
            /* Main Header with Glow Effect */
            .main-header {
                font-size: 3rem;
                font-weight: 800;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                padding: 1.5rem 0;
                text-shadow: 0 0 40px var(--glow-color);
                letter-spacing: -1px;
            }
            
            .main-subtitle {
                text-align: center;
                color: var(--text-secondary);
                font-size: 1.1rem;
                margin-bottom: 2rem;
                font-weight: 400;
            }
            
            /* Hero Section */
            .hero-section {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 4px 20px var(--shadow-color);
            }
            
            /* Step Header */
            .step-header {
                font-size: 1.6rem;
                font-weight: 700;
                color: var(--text-primary);
                border-bottom: 3px solid var(--accent-primary);
                padding-bottom: 0.75rem;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            /* Cards */
            .feature-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.5rem;
                margin: 0.5rem 0;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px var(--shadow-color);
            }
            
            .feature-card:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 20px var(--glow-color);
                transform: translateY(-2px);
            }
            
            /* Timeline Day Badge */
            .timeline-day {
                background: var(--accent-gradient);
                color: white;
                padding: 0.6rem 1.2rem;
                border-radius: 25px;
                font-weight: 700;
                display: inline-block;
                margin-bottom: 0.75rem;
                font-size: 0.9rem;
                box-shadow: 0 2px 10px var(--glow-color);
            }
            
            /* Timeline Card */
            .timeline-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1rem;
                height: 100%;
                transition: all 0.3s ease;
            }
            
            .timeline-card:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 15px var(--glow-color);
            }
            
            /* Pivot Card */
            .pivot-card {
                background: var(--bg-card);
                border-left: 4px solid var(--accent-primary);
                border-radius: 0 12px 12px 0;
                padding: 1.25rem;
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            
            .pivot-card:hover {
                background: var(--bg-secondary);
                box-shadow: 0 4px 15px var(--shadow-color);
            }
            
            /* Reality Warning */
            .reality-warning {
                background: var(--warning-bg);
                border: 1px solid var(--warning-border);
                border-radius: 12px;
                padding: 1.25rem;
                margin: 1rem 0;
            }
            
            /* Score Card */
            .score-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .score-card:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 15px var(--glow-color);
            }
            
            .score-value {
                font-size: 2.5rem;
                font-weight: 800;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .score-label {
                color: var(--text-secondary);
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }
            
            /* Buttons */
            .stButton > button {
                background: var(--accent-gradient) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.6rem 1.5rem !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 2px 10px var(--glow-color) !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 20px var(--glow-color) !important;
            }
            
            .stButton > button[kind="secondary"] {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                box-shadow: none !important;
            }
            
            .stButton > button[kind="secondary"]:hover {
                border-color: var(--accent-primary) !important;
                box-shadow: 0 2px 10px var(--glow-color) !important;
            }
            
            /* Input Fields */
            .stTextArea textarea, .stTextInput input, .stSelectbox select {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                border-radius: 10px !important;
                color: var(--text-primary) !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextArea textarea:focus, .stTextInput input:focus {
                border-color: var(--accent-primary) !important;
                box-shadow: 0 0 0 2px var(--glow-color) !important;
            }
            
            /* Sidebar */
            section[data-testid="stSidebar"] {
                background: var(--bg-secondary) !important;
                border-right: 1px solid var(--border-color);
            }
            
            section[data-testid="stSidebar"] .stButton > button {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                box-shadow: none !important;
            }
            
            section[data-testid="stSidebar"] .stButton > button:hover {
                border-color: var(--accent-primary) !important;
                background: var(--bg-primary) !important;
            }
            
            /* Progress Bar */
            .stProgress > div > div {
                background: var(--accent-gradient) !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                border-radius: 10px !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background: var(--bg-card);
                border-radius: 10px;
                padding: 0.25rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                color: var(--text-secondary) !important;
                border-radius: 8px !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: var(--accent-gradient) !important;
                color: white !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            
            /* Info/Success/Warning boxes */
            .stAlert {
                border-radius: 10px !important;
            }
            
            /* Code blocks */
            .stCodeBlock {
                border-radius: 10px !important;
            }
            
            /* Theme Toggle Button */
            .theme-toggle {
                position: fixed;
                top: 0.75rem;
                right: 1rem;
                z-index: 999999;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 50px;
                padding: 0.5rem 1rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                color: var(--text-primary);
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px var(--shadow-color);
            }
            
            .theme-toggle:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 15px var(--glow-color);
            }
            
            /* Stat Badge */
            .stat-badge {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 50px;
                padding: 0.4rem 1rem;
                font-size: 0.85rem;
                color: var(--text-secondary);
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            /* Glowing Border Animation */
            @keyframes glow-pulse {
                0%, 100% { box-shadow: 0 0 5px var(--glow-color); }
                50% { box-shadow: 0 0 20px var(--glow-color); }
            }
            
            .glow-border {
                animation: glow-pulse 2s ease-in-out infinite;
            }
        </style>
        """
    else:
        return """
        <style>
            /* Light Theme Variables */
            :root {
                --bg-primary: #ffffff;
                --bg-secondary: #f8fafc;
                --bg-card: #ffffff;
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --accent-primary: #7c3aed;
                --accent-secondary: #a855f7;
                --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%);
                --border-color: #e2e8f0;
                --success-bg: #f0fdf4;
                --success-border: #22c55e;
                --warning-bg: #fffbeb;
                --warning-border: #f59e0b;
                --info-bg: #eff6ff;
                --info-border: #3b82f6;
                --shadow-color: rgba(0, 0, 0, 0.08);
                --glow-color: rgba(124, 58, 237, 0.2);
            }
            
            /* Global Styles */
            .stApp {
                background: var(--bg-secondary) !important;
            }
            
            .main .block-container {
                background: var(--bg-secondary);
                padding-top: 2rem;
            }
            
            /* Main Header with Glow Effect */
            .main-header {
                font-size: 3rem;
                font-weight: 800;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                padding: 1.5rem 0;
                letter-spacing: -1px;
            }
            
            .main-subtitle {
                text-align: center;
                color: var(--text-secondary);
                font-size: 1.1rem;
                margin-bottom: 2rem;
                font-weight: 400;
            }
            
            /* Hero Section */
            .hero-section {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: 0 4px 20px var(--shadow-color);
            }
            
            /* Step Header */
            .step-header {
                font-size: 1.6rem;
                font-weight: 700;
                color: var(--text-primary);
                border-bottom: 3px solid var(--accent-primary);
                padding-bottom: 0.75rem;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            /* Cards */
            .feature-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.5rem;
                margin: 0.5rem 0;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px var(--shadow-color);
            }
            
            .feature-card:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 20px var(--glow-color);
                transform: translateY(-2px);
            }
            
            /* Timeline Day Badge */
            .timeline-day {
                background: var(--accent-gradient);
                color: white;
                padding: 0.6rem 1.2rem;
                border-radius: 25px;
                font-weight: 700;
                display: inline-block;
                margin-bottom: 0.75rem;
                font-size: 0.9rem;
                box-shadow: 0 2px 10px var(--glow-color);
            }
            
            /* Timeline Card */
            .timeline-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1rem;
                height: 100%;
                transition: all 0.3s ease;
            }
            
            .timeline-card:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 15px var(--glow-color);
            }
            
            /* Pivot Card */
            .pivot-card {
                background: var(--bg-card);
                border-left: 4px solid var(--accent-primary);
                border-radius: 0 12px 12px 0;
                padding: 1.25rem;
                margin: 1rem 0;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px var(--shadow-color);
            }
            
            .pivot-card:hover {
                box-shadow: 0 4px 15px var(--glow-color);
            }
            
            /* Reality Warning */
            .reality-warning {
                background: var(--warning-bg);
                border: 1px solid var(--warning-border);
                border-radius: 12px;
                padding: 1.25rem;
                margin: 1rem 0;
            }
            
            /* Score Card */
            .score-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px var(--shadow-color);
            }
            
            .score-card:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 15px var(--glow-color);
            }
            
            .score-value {
                font-size: 2.5rem;
                font-weight: 800;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .score-label {
                color: var(--text-secondary);
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }
            
            /* Buttons */
            .stButton > button {
                background: var(--accent-gradient) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.6rem 1.5rem !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 2px 10px var(--glow-color) !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 20px var(--glow-color) !important;
            }
            
            .stButton > button[kind="secondary"] {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                color: var(--text-primary) !important;
                box-shadow: none !important;
            }
            
            .stButton > button[kind="secondary"]:hover {
                border-color: var(--accent-primary) !important;
                box-shadow: 0 2px 10px var(--glow-color) !important;
            }
            
            /* Input Fields */
            .stTextArea textarea, .stTextInput input, .stSelectbox select {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                border-radius: 10px !important;
                color: var(--text-primary) !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextArea textarea:focus, .stTextInput input:focus {
                border-color: var(--accent-primary) !important;
                box-shadow: 0 0 0 2px var(--glow-color) !important;
            }
            
            /* Sidebar */
            section[data-testid="stSidebar"] {
                background: var(--bg-card) !important;
                border-right: 1px solid var(--border-color);
            }
            
            section[data-testid="stSidebar"] .stButton > button {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border-color) !important;
                color: var(--text-primary) !important;
                box-shadow: none !important;
            }
            
            section[data-testid="stSidebar"] .stButton > button:hover {
                border-color: var(--accent-primary) !important;
                background: var(--bg-card) !important;
            }
            
            /* Progress Bar */
            .stProgress > div > div {
                background: var(--accent-gradient) !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-color) !important;
                border-radius: 10px !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background: var(--bg-card);
                border-radius: 10px;
                padding: 0.25rem;
                border: 1px solid var(--border-color);
            }
            
            .stTabs [data-baseweb="tab"] {
                color: var(--text-secondary) !important;
                border-radius: 8px !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: var(--accent-gradient) !important;
                color: white !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            
            /* Info/Success/Warning boxes */
            .stAlert {
                border-radius: 10px !important;
            }
            
            /* Code blocks */
            .stCodeBlock {
                border-radius: 10px !important;
            }
            
            /* Theme Toggle Button */
            .theme-toggle {
                position: fixed;
                top: 0.75rem;
                right: 1rem;
                z-index: 999999;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 50px;
                padding: 0.5rem 1rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                color: var(--text-primary);
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px var(--shadow-color);
            }
            
            .theme-toggle:hover {
                border-color: var(--accent-primary);
                box-shadow: 0 4px 15px var(--glow-color);
            }
            
            /* Stat Badge */
            .stat-badge {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 50px;
                padding: 0.4rem 1rem;
                font-size: 0.85rem;
                color: var(--text-secondary);
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                box-shadow: 0 2px 5px var(--shadow-color);
            }
        </style>
        """


def render_theme_toggle():
    """Render the theme toggle in sidebar."""
    is_dark = st.session_state.get("dark_mode", True)
    theme_css = get_theme_css(is_dark)
    st.markdown(theme_css, unsafe_allow_html=True)


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "current_step": 1,
        "idea_text": "",
        "student_class": 8,
        "idea_type": "App or Website",
        "refined_idea": None,
        "scores": None,
        "reality_check": None,
        "pivots": [],
        "timeline": [],
        "mentor_questions": [],
        "mentor_answers": {},
        "mentor_feedback": {},
        "current_question_idx": 0,
        "mentor_complete": False,
        "prototype_generated": False,
        "prototype_code": None,
        "show_scores": False,
        "dark_mode": True
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_app():
    """Reset all session state to start fresh."""
    keys_to_reset = list(st.session_state.keys())
    for key in keys_to_reset:
        del st.session_state[key]


def can_navigate_to_step(step: int) -> bool:
    """Check if user can navigate to a specific step."""
    if step == 1:
        return True
    elif step == 2:
        return len(st.session_state.get("idea_text", "").strip()) >= 20
    elif step == 3:
        return st.session_state.get("refined_idea") is not None
    elif step == 4:
        return st.session_state.get("mentor_complete", False)
    return False


def navigate_to_step(step: int):
    """Navigate to a specific step if allowed."""
    if can_navigate_to_step(step):
        st.session_state.current_step = step
        st.rerun()


def render_sidebar():
    """Render the sidebar with progress tracker, navigation, and theme toggle."""
    with st.sidebar:
        # Theme Toggle at the top
        st.markdown("### 🎨 Theme")
        col1, col2 = st.columns([3, 1])
        with col1:
            is_dark = st.session_state.get("dark_mode", True)
            theme_label = "Dark Mode" if is_dark else "Light Mode"
            theme_icon = "🌙" if is_dark else "☀️"
            st.caption(f"{theme_icon} {theme_label}")
        with col2:
            if st.button("🔄", key="theme_toggle", help="Toggle theme"):
                st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Progress Tracker")
        
        steps = [
            ("1️⃣", "Idea Input", 1),
            ("2️⃣", "Idea Refinement", 2),
            ("3️⃣", "Mentor Session", 3),
            ("4️⃣", "Prototype", 4)
        ]
        
        for icon, name, step_num in steps:
            can_nav = can_navigate_to_step(step_num)
            is_current = st.session_state.current_step == step_num
            is_complete = st.session_state.current_step > step_num
            
            if is_complete:
                if st.button(f" {icon} {name}", key=f"nav_{step_num}", use_container_width=True):
                    navigate_to_step(step_num)
            elif is_current:
                st.info(f"{icon} {name} ◀ Current")
            elif can_nav:
                if st.button(f"🔓 {icon} {name}", key=f"nav_{step_num}", use_container_width=True):
                    navigate_to_step(step_num)
            else:
                st.text(f"🔒 {icon} {name}")
        
        st.markdown("---")
        
        # Show scores only after mentor session
        if st.session_state.get("show_scores") and st.session_state.scores:
            st.markdown("### 📈 Readiness Scores")
            scores = st.session_state.scores
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Clarity", f"{scores['clarity']}/10")
                st.metric("Feasibility", f"{scores['feasibility']}/10")
            with col2:
                st.metric("Innovation", f"{scores['innovation']}/10")
                st.metric("Overall", f"{scores['overall']}/10")
            st.markdown("---")
        
        # Restart button
        if st.button("🔄 Start Over", use_container_width=True, type="secondary"):
            reset_app()
            st.rerun()
        
        # # Quick info
        # if st.session_state.get("idea_type"):
        #     st.caption(f"📌 Type: {st.session_state.idea_type}")
        # if st.session_state.get("student_class"):
        #     st.caption(f"🎓 Class: {st.session_state.student_class}")


def step1_idea_input():
    """Step 1: Collect startup idea and metadata."""
    is_dark = st.session_state.get("dark_mode", True)
    
    # Hero section with step header
    st.markdown(
        '''
        <div class="hero-section">
            <p class="step-header">💡 Step 1: Share Your Startup Idea</p>
            <p style="color: var(--text-secondary); margin-top: -0.5rem;">
                Tell us about your brilliant idea and we'll help you turn it into reality!
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    # Input method selection with cards
    st.markdown("#### 📝 Choose Input Method")
    input_method = st.radio(
        "How would you like to share your idea?",
        ["✍️ Type it", "🎤 Voice Input", "📄 Upload PDF"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            '''
            <div class="feature-card">
                <h4 style="margin-top: 0; color: var(--text-primary);">📝 Your Idea</h4>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        if input_method == "✍️ Type it":
            st.session_state.idea_text = st.text_area(
                "Describe your startup idea",
                value=st.session_state.idea_text,
                height=180,
                placeholder="Example: An app that helps students find study partners based on their subjects and learning style...\n\nTip: Be specific about the problem you're solving and who you're helping!"
            )
        
        elif input_method == "🎤 Voice Input":
            st.markdown(
                '''
                <div style="background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(236, 72, 153, 0.1)); 
                            border: 1px dashed var(--accent-primary); border-radius: 12px; padding: 1.5rem; text-align: center;">
                    <p style="font-size: 2rem; margin: 0;">🎤</p>
                    <p style="color: var(--accent-primary); font-weight: 600; margin: 0.5rem 0;">Voice Input - Coming Soon!</p>
                    <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0;">Speak your idea naturally and we'll transcribe it.</p>
                </div>
                ''',
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.session_state.idea_text = st.text_area(
                "Or type your idea:",
                value=st.session_state.idea_text,
                height=120,
                key="voice_fallback"
            )
        
        elif input_method == "📄 Upload PDF":
            st.markdown(
                '''
                <div style="background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(236, 72, 153, 0.1)); 
                            border: 1px dashed var(--accent-primary); border-radius: 12px; padding: 1.5rem; text-align: center;">
                    <p style="font-size: 2rem; margin: 0;">📄</p>
                    <p style="color: var(--accent-primary); font-weight: 600; margin: 0.5rem 0;">PDF Upload - Coming Soon!</p>
                    <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0;">Upload a business plan document.</p>
                </div>
                ''',
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.session_state.idea_text = st.text_area(
                "Or type your idea:",
                value=st.session_state.idea_text,
                height=120,
                key="pdf_fallback"
            )
        
        # Idea examples
        with st.expander("💡 Need inspiration? See example ideas"):
            st.markdown("""
            **App or Website Ideas:**
            - Study buddy finder app for students
            - Local food delivery from home cooks
            - Pet sitting service connector
            
            **AI Tool Ideas:**
            - Homework helper that explains concepts
            - Story generator for creative writing
            - Language learning chatbot
            
            **Marketplace Ideas:**
            - Student tutoring marketplace
            - Handmade crafts from students
            - Used textbook exchange platform
            """)
    
    with col2:
        # Settings card
        st.markdown(
            '''
            <div class="feature-card">
                <h4 style="margin-top: 0; color: var(--text-primary);">⚙️ Settings</h4>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        st.session_state.student_class = st.selectbox(
            "🎓 Your Class",
            options=list(range(6, 13)),
            index=st.session_state.student_class - 6,
            help="We'll adjust complexity based on your grade level"
        )
        
        st.session_state.idea_type = st.selectbox(
            "🎯 Idea Type",
            options=["App or Website", "AI Tool", "Marketplace"],
            index=["App or Website", "AI Tool", "Marketplace"].index(st.session_state.idea_type)
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Age-adaptive indicator with visual styling
        st.markdown(
            '''
            <div class="feature-card" style="background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(236, 72, 153, 0.1));">
                <h5 style="margin-top: 0; color: var(--accent-primary);"> AI Mode</h5>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        if st.session_state.student_class <= 7:
            mode_icon = "🌟"
            mode_name = "Junior Mode"
            mode_desc = "Simple language, fun activities, family involvement"
            mode_color = "#22c55e"
        elif st.session_state.student_class <= 9:
            mode_icon = "🚀"
            mode_name = "Middle Mode"
            mode_desc = "Practical guidance, surveys, basic prototyping"
            mode_color = "#3b82f6"
        else:
            mode_icon = "💼"
            mode_name = "Senior Mode"
            mode_desc = "Startup methodology, metrics, investor-ready"
            mode_color = "#a855f7"
        
        st.markdown(
            f'''
            <div style="text-align: center; padding: 0.5rem;">
                <span style="font-size: 1.5rem;">{mode_icon}</span>
                <p style="font-weight: 700; color: {mode_color}; margin: 0.25rem 0;">{mode_name}</p>
                <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0;">{mode_desc}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # What you'll get section
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '''
            <div class="feature-card">
                <h5 style="margin-top: 0; color: var(--text-primary);">✨ What You'll Get</h5>
                <ul style="color: var(--text-secondary); font-size: 0.85rem; padding-left: 1.2rem; margin: 0;">
                    <li>Structured business plan</li>
                    <li>5-day action timeline</li>
                    <li>Pivot suggestions</li>
                    <li>Mentor Q&A session</li>
                    <li>Working prototype code</li>
                </ul>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Refine My Idea & Generate Plan", type="primary", use_container_width=True):
            if len(st.session_state.idea_text.strip()) < 20:
                st.error("⚠️ Please describe your idea in at least 20 characters.")
            else:
                st.session_state.current_step = 2
                st.rerun()


def step2_idea_refinement():
    """Step 2: Generate structured idea refinement with new features."""
    # Hero section
    st.markdown(
        '''
        <div class="hero-section">
            <p class="step-header">📋 Step 2: Your Refined Startup Plan</p>
            <p style="color: var(--text-secondary); margin-top: -0.5rem;">
                AI has analyzed your idea and created a structured plan with timeline and pivot options!
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    if st.session_state.refined_idea is None:
        with st.spinner("🧠 AI is analyzing your idea with Reality Check, Pivot Engine, and Timeline..."):
            refiner = IdeaRefiner()
            result = refiner.refine(
                idea=st.session_state.idea_text,
                student_class=st.session_state.student_class,
                idea_type=st.session_state.idea_type
            )
            st.session_state.refined_idea = result["refined_idea"]
            st.session_state.scores = result["scores"]
            st.session_state.reality_check = result.get("reality_check", {})
            st.session_state.pivots = result.get("pivots", [])
            st.session_state.timeline = result.get("timeline", [])
            
            # Generate mentor questions
            mentor = MentorEngine()
            st.session_state.mentor_questions = mentor.generate_questions(
                st.session_state.refined_idea,
                st.session_state.student_class
            )
    
    refined = st.session_state.refined_idea
    reality_check = st.session_state.reality_check
    
    # Reality Simplifier Warning (if idea was simplified)
    if reality_check and not reality_check.get("is_realistic", True):
        st.markdown(
            f'''
            <div class="reality-warning">
                <h4 style="margin-top: 0; color: #d29922;">⚠️ Reality Simplifier Activated</h4>
                <p><strong>Original scope:</strong> {reality_check.get('original_scope', 'N/A')}</p>
                <p><strong>Why we simplified:</strong> {reality_check.get('simplification_reason', 'To make it achievable for a student project.')}</p>
                <p style="margin-bottom: 0;">✅ <strong>Your achievable version is below!</strong></p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    # Main Plan Display in cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'''
            <div class="feature-card">
                <h4 style="margin-top: 0; color: var(--accent-primary);">🎯 Problem Statement</h4>
                <p style="color: var(--text-primary); margin-bottom: 0;">{refined["problem_statement"]}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'''
            <div class="feature-card">
                <h4 style="margin-top: 0; color: var(--accent-primary);">👥 Target User</h4>
                <p style="color: var(--text-primary); margin-bottom: 0;">{refined["target_user"]}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    # Core Features
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ⭐ Core Features")
    feature_cols = st.columns(3)
    for i, feature in enumerate(refined["core_features"]):
        with feature_cols[i % 3]:
            st.markdown(
                f'''
                <div class="feature-card" style="text-align: center;">
                    <span style="font-size: 1.5rem; color: var(--accent-primary);">{i+1}</span>
                    <p style="color: var(--text-primary); margin: 0.5rem 0 0 0; font-size: 0.95rem;">{feature}</p>
                </div>
                ''',
                unsafe_allow_html=True
            )
    
    # Revenue Model
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'''
        <div class="feature-card" style="border-left: 4px solid #22c55e;">
            <h4 style="margin-top: 0; color: #22c55e;">💰 Revenue Model</h4>
            <p style="color: var(--text-primary); margin-bottom: 0;">{refined["revenue_model"]}</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    # Realism note
    if refined.get("realism_note"):
        st.caption(f"💡 {refined['realism_note']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # TIMELINE VISUALIZER
    st.markdown("### 📅 From Idea to Demo: 5-Day Timeline")
    
    timeline = st.session_state.timeline
    if timeline:
        timeline_cols = st.columns(5)
        for i, day in enumerate(timeline[:5]):
            with timeline_cols[i]:
                day_num = day.get("day", i + 1)
                theme = day.get('theme', 'Activity')
                tasks = day.get("tasks", [])
                outcome = day.get("outcome", "")
                tip = day.get("tip", "")
                
                tasks_html = "".join([f'<li style="color: var(--text-secondary); font-size: 0.8rem;">{task}</li>' for task in tasks[:3]])
                
                st.markdown(
                    f'''
                    <div class="timeline-card">
                        <div class="timeline-day">Day {day_num}</div>
                        <p style="font-weight: 700; color: var(--text-primary); margin: 0.5rem 0; font-size: 0.95rem;">{theme}</p>
                        <ul style="padding-left: 1rem; margin: 0.5rem 0;">{tasks_html}</ul>
                        {f'<div style="background: rgba(34, 197, 94, 0.1); border-radius: 8px; padding: 0.5rem; margin-top: 0.5rem;"><span style="color: #22c55e; font-size: 0.8rem;">✓ {outcome}</span></div>' if outcome else ''}
                        {f'<p style="color: var(--accent-primary); font-size: 0.75rem; margin: 0.5rem 0 0 0;">💡 {tip}</p>' if tip else ''}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
    else:
        # Fallback to simple action plan
        plan_cols = st.columns(5)
        for i, step in enumerate(refined.get("five_day_action_plan", [])[:5], 1):
            with plan_cols[i-1]:
                step_text = step
                for prefix in [f"day {i}:", f"day {i} -", f"day{i}:"]:
                    if step.lower().startswith(prefix):
                        step_text = step[len(prefix):].strip()
                        break
                st.markdown(
                    f'''
                    <div class="timeline-card">
                        <div class="timeline-day">Day {i}</div>
                        <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0.5rem 0 0 0;">{step_text}</p>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PIVOT SUGGESTION ENGINE
    st.markdown("### 🔄 Pivot Suggestions")
    st.caption("Every great startup has a backup plan. Here are pivot directions if your main idea needs adjustment:")
    
    pivots = st.session_state.pivots
    if pivots:
        pivot_cols = st.columns(len(pivots[:3]))
        for i, pivot in enumerate(pivots[:3]):
            with pivot_cols[i]:
                direction = pivot.get('direction', 'Alternative')
                description = pivot.get('description', '')
                why = pivot.get('why_it_might_work', '')
                
                st.markdown(
                    f'''
                    <div class="pivot-card">
                        <h5 style="margin: 0; color: var(--accent-primary);">Pivot {i+1}: {direction}</h5>
                        <p style="color: var(--text-primary); margin: 0.5rem 0; font-size: 0.9rem;">{description}</p>
                        {f'<p style="color: #22c55e; font-size: 0.8rem; margin: 0;">✓ {why}</p>' if why else ''}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
    else:
        st.caption("Pivot suggestions will appear after AI analysis.")
    
    st.markdown("---")
    
    # Download option
    with st.expander("📥 Download Full Plan"):
        full_data = {
            "refined_idea": refined,
            "timeline": timeline,
            "pivots": pivots,
            "reality_check": reality_check
        }
        st.download_button(
            label="Download JSON",
            data=json.dumps(full_data, indent=2, ensure_ascii=False),
            file_name="venturepilot_plan.json",
            mime="application/json"
        )
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Idea Input", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with col2:
        if st.button("👨‍🏫 Start Mentor Session ➡️", type="primary", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()


def step3_mentor_session():
    """Step 3: Interactive mentor Q&A session."""
    # Hero section
    st.markdown(
        '''
        <div class="hero-section">
            <p class="step-header"> Step 3: Mentor Session</p>
            <p style="color: var(--text-secondary); margin-top: -0.5rem;">
                Answer strategic questions to strengthen your startup idea!
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    mentor = MentorEngine()
    questions = st.session_state.mentor_questions
    current_idx = st.session_state.current_question_idx
    
    # Progress with visual enhancement
    progress_value = current_idx / len(questions) if questions else 0
    st.progress(progress_value)
    st.markdown(
        f'''
        <div style="display: flex; justify-content: space-between; margin-top: -0.5rem;">
            <span class="stat-badge">Question {min(current_idx + 1, len(questions))} of {len(questions)}</span>
            <span class="stat-badge">{int(progress_value * 100)}% Complete</span>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Previous Q&A
    if current_idx > 0:
        st.markdown("#### ✅ Previous Answers")
        for i in range(current_idx):
            q = questions[i]
            with st.expander(f"Q{i+1}: {q['question']}", expanded=False):
                st.markdown(
                    f'''
                    <div class="feature-card">
                        <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0;">Your Answer:</p>
                        <p style="color: var(--text-primary); margin: 0.5rem 0;">{st.session_state.mentor_answers.get(i, '')}</p>
                        <hr style="border-color: var(--border-color); margin: 1rem 0;">
                        <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0;">Mentor Feedback:</p>
                        <p style="color: #22c55e; margin: 0.5rem 0 0 0;">{st.session_state.mentor_feedback.get(i, '')}</p>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
    
    # Current question
    if current_idx < len(questions):
        q = questions[current_idx]
        
        st.markdown(
            f'''
            <div class="feature-card" style="border-left: 4px solid var(--accent-primary);">
                <h3 style="margin-top: 0; color: var(--text-primary);">💭 {q['question']}</h3>
                <p style="color: var(--accent-primary); font-size: 0.9rem; margin: 0;">
                    💡 Hint: {q['context']}
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        answer = st.text_area(
            "Your answer:",
            key=f"answer_{current_idx}",
            height=150,
            placeholder="Think carefully and share your thoughts... Be specific and detailed!"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("⬅️ Back to Plan", use_container_width=True, type="secondary"):
                st.session_state.current_step = 2
                st.rerun()
        with col2:
            if st.button("Submit Answer ✓", type="primary", use_container_width=True):
                if len(answer.strip()) < 10:
                    st.error("⚠️ Please provide a more detailed answer (at least 10 characters).")
                else:
                    with st.spinner("🤔 Mentor is reviewing your answer..."):
                        feedback = mentor.get_feedback(
                            question=q["question"],
                            answer=answer,
                            refined_idea=st.session_state.refined_idea,
                            student_class=st.session_state.student_class
                        )
                    
                    st.session_state.mentor_answers[current_idx] = answer
                    st.session_state.mentor_feedback[current_idx] = feedback
                    st.session_state.current_question_idx += 1
                    
                    if st.session_state.current_question_idx >= len(questions):
                        st.session_state.mentor_complete = True
                        st.session_state.show_scores = True
                    
                    st.rerun()
    
    # Completed
    if st.session_state.mentor_complete:
        st.markdown(
            '''
            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)); 
                        border: 1px solid #22c55e; border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1.5rem;">
                <p style="font-size: 2rem; margin: 0;">🎉</p>
                <h3 style="color: #22c55e; margin: 0.5rem 0;">Mentor Session Complete!</h3>
                <p style="color: var(--text-secondary); margin: 0;">Great job answering all the strategic questions!</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Show scores with enhanced cards
        st.markdown("### 📈 Your Startup Readiness Scores")
        scores = st.session_state.scores
        
        score_cols = st.columns(4)
        score_data = [
            ("💡", "Clarity", scores['clarity'], scores.get('clarity_reason', ''), "#3b82f6"),
            ("⚙️", "Feasibility", scores['feasibility'], scores.get('feasibility_reason', ''), "#22c55e"),
            ("✨", "Innovation", scores['innovation'], scores.get('innovation_reason', ''), "#a855f7"),
            ("🎯", "Overall", scores['overall'], "Ready to prototype!" if scores['overall'] >= 7 else "Keep improving!", "#ec4899")
        ]
        
        for i, (icon, label, value, reason, color) in enumerate(score_data):
            with score_cols[i]:
                st.markdown(
                    f'''
                    <div class="score-card">
                        <span style="font-size: 1.5rem;">{icon}</span>
                        <div class="score-value">{value}/10</div>
                        <div class="score-label">{label}</div>
                        <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">{reason[:80]}...</p>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary
        with st.expander("📝 Session Summary", expanded=False):
            for i, q in enumerate(questions):
                st.markdown(
                    f'''
                    <div class="feature-card" style="margin-bottom: 1rem;">
                        <p style="color: var(--accent-primary); font-weight: 600; margin: 0;">Q{i+1}: {q['question']}</p>
                        <p style="color: var(--text-primary); margin: 0.5rem 0;"><strong>Your Answer:</strong> {st.session_state.mentor_answers.get(i, '')}</p>
                        <p style="color: #22c55e; margin: 0;"><strong>Feedback:</strong> {st.session_state.mentor_feedback.get(i, '')}</p>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Plan", use_container_width=True, type="secondary"):
                st.session_state.current_step = 2
                st.rerun()
        with col2:
            if st.button("🛠️ Generate Prototype ➡️", type="primary", use_container_width=True):
                st.session_state.current_step = 4
                st.rerun()


def step4_prototype():
    """Step 4: Generate prototype."""
    # Hero section
    st.markdown(
        '''
        <div class="hero-section">
            <p class="step-header">🛠️ Step 4: Your Prototype</p>
            <p style="color: var(--text-secondary); margin-top: -0.5rem;">
                Here's your working prototype code - ready to run and customize!
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    if not st.session_state.prototype_generated:
        with st.spinner(f"🔨 Generating {st.session_state.idea_type} prototype..."):
            router = PrototypeRouter()
            result = router.generate(
                idea_type=st.session_state.idea_type,
                refined_idea=st.session_state.refined_idea,
                student_class=st.session_state.student_class,
                mentor_answers=st.session_state.mentor_answers
            )
            st.session_state.prototype_code = result
            st.session_state.prototype_generated = True
            save_prototype(result)
    
    prototype = st.session_state.prototype_code
    
    # Success message with type badge
    st.markdown(
        f'''
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)); 
                    border: 1px solid #22c55e; border-radius: 12px; padding: 1rem; display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <span style="font-size: 2rem;">✅</span>
            <div>
                <p style="color: #22c55e; font-weight: 700; margin: 0;">{st.session_state.idea_type} Prototype Generated!</p>
                <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0;">Files saved to /outputs folder</p>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    # Display based on type
    if st.session_state.idea_type == "App or Website":
        display_web_prototype(prototype)
    elif st.session_state.idea_type == "AI Tool":
        display_ai_tool_prototype(prototype)
    else:
        display_marketplace_prototype(prototype)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Back to Mentor", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()
    with col2:
        if st.button("📋 View Plan", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
    with col3:
        if st.button("🔄 Start New Idea", type="primary", use_container_width=True):
            reset_app()
            st.rerun()


def display_web_prototype(prototype):
    """Display web prototype."""
    st.markdown("### 🌐 Landing Page Preview")
    tab1, tab2 = st.tabs(["👁️ Live Preview", "💻 HTML Code"])
    with tab1:
        st.components.v1.html(prototype["html"], height=600, scrolling=True)
    with tab2:
        st.code(prototype["html"], language="html")
        st.download_button("📥 Download HTML", prototype["html"], "landing_page.html", "text/html")


def display_ai_tool_prototype(prototype):
    """Display AI tool prototype."""
    st.markdown("### 🤖 AI Tool Prototype")
    tab1, tab2 = st.tabs(["🧠 Prompt Logic", "📱 Streamlit Demo"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**System Prompt**")
            st.code(prototype["system_prompt"], language="text")
        with col2:
            st.markdown("**User Template**")
            st.code(prototype["user_prompt_template"], language="text")
    with tab2:
        st.code(prototype["streamlit_demo"], language="python")
        st.download_button("📥 Download Script", prototype["streamlit_demo"], "ai_tool_demo.py", "text/x-python")
        st.info("💡 Run with: `streamlit run ai_tool_demo.py`")


def display_marketplace_prototype(prototype):
    """Display marketplace prototype."""
    st.markdown("### 🏪 Marketplace Prototype")
    tab1, tab2, tab3 = st.tabs(["👥 Roles & Flow", "🗄️ Database", "🌐 HTML"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**User Roles**")
            for role in prototype["user_roles"]:
                if isinstance(role, dict):
                    st.info(f"**{role['name']}:** {role['description']}")
                else:
                    st.info(role)
        with col2:
            st.markdown("**User Flow**")
            for i, step in enumerate(prototype["user_flow"], 1):
                st.success(f"**{i}.** {step}")
    
    with tab2:
        st.code(prototype["database_schema"], language="sql")
        st.download_button("📥 Download Schema", prototype["database_schema"], "schema.sql", "text/plain")
    
    with tab3:
        preview, code = st.tabs(["Preview", "Code"])
        with preview:
            st.components.v1.html(prototype["html_scaffold"], height=400, scrolling=True)
        with code:
            st.code(prototype["html_scaffold"], language="html")
            st.download_button("📥 Download HTML", prototype["html_scaffold"], "marketplace.html", "text/html")


def save_prototype(prototype):
    """Save prototype files."""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    idea_type = st.session_state.idea_type
    
    if idea_type == "App or Website":
        (output_dir / "landing_page.html").write_text(prototype["html"], encoding="utf-8")
    elif idea_type == "AI Tool":
        (output_dir / "ai_tool_demo.py").write_text(prototype["streamlit_demo"], encoding="utf-8")
        (output_dir / "prompts.txt").write_text(
            f"System Prompt:\n{prototype['system_prompt']}\n\nUser Template:\n{prototype['user_prompt_template']}",
            encoding="utf-8"
        )
    else:
        (output_dir / "schema.sql").write_text(prototype["database_schema"], encoding="utf-8")
        (output_dir / "marketplace.html").write_text(prototype["html_scaffold"], encoding="utf-8")
    
    # Save session data
    session_data = {
        "idea_text": st.session_state.idea_text,
        "student_class": st.session_state.student_class,
        "idea_type": st.session_state.idea_type,
        "refined_idea": st.session_state.refined_idea,
        "scores": st.session_state.scores,
        "reality_check": st.session_state.reality_check,
        "pivots": st.session_state.pivots,
        "timeline": st.session_state.timeline,
        "mentor_answers": {str(k): v for k, v in st.session_state.mentor_answers.items()},
        "mentor_feedback": {str(k): v for k, v in st.session_state.mentor_feedback.items()}
    }
    (output_dir / "session_data.json").write_text(
        json.dumps(session_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    """Main application entry point."""
    # Initialize session state first
    init_session_state()
    
    # Apply theme CSS
    render_theme_toggle()
    
    # Header with enhanced styling
    is_dark = st.session_state.get("dark_mode", True)
    subtitle_color = "#8b949e" if is_dark else "#64748b"
    
    st.markdown('<p class="main-header">🚀 VenturePilot</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="main-subtitle">'
        f'AI-Powered Startup Builder with Age-Adaptive Intelligence</p>',
        unsafe_allow_html=True
    )
    
    # Feature badges
    st.markdown(
        f'''
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem;">
            <span class="stat-badge">🧠 Age-Adaptive AI</span>
            <span class="stat-badge">⚡ Reality Simplifier</span>
            <span class="stat-badge">🔄 Pivot Engine</span>
            <span class="stat-badge">📅 Timeline Visualizer</span>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    render_sidebar()
    
    step_handlers = {
        1: step1_idea_input,
        2: step2_idea_refinement,
        3: step3_mentor_session,
        4: step4_prototype
    }
    
    handler = step_handlers.get(st.session_state.current_step, step1_idea_input)
    handler()


if __name__ == "__main__":
    main()
