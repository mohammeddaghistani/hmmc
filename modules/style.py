import streamlit as st

def apply_custom_style():
    st.set_page_config(
        page_title="نظام التقييم الإيجاري",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown("""<style>#MainMenu, footer, header {visibility: hidden;} .stDeployButton {display:none;}</style>""", unsafe_allow_html=True)

def get_custom_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main-header {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* تحسينات العرض للجوال */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.4rem !important; }
        .stButton>button { height: 3.5em; font-size: 1rem !important; }
        [data-testid="stSidebar"] { width: 80% !important; }
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    </style>
    """
