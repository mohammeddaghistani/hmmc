import streamlit as st

def apply_custom_style():
    st.set_page_config(
        page_title="نظام التقييم الإيجاري",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # إخفاء عناصر Streamlit لتحسين المظهر
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        </style>
    """, unsafe_allow_html=True)

def get_custom_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* تحسينات الجوال والـ Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-left: 1px solid #e0e0e0;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        background-color: #1E3A8A;
        color: white;
    }

    .main-header {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }


    /* تنسيق الجوال */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.4rem !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.9rem !important; padding: 10px !important; }
    }
    </style>
    """
