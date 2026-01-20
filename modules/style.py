import streamlit as st

def apply_custom_style():
    """تطبيق الإعدادات الأساسية وتحسين واجهة المستخدم"""
    st.set_page_config(
        page_title="نظام التقييم الإيجاري",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # إخفاء عناصر Streamlit الافتراضية لتحسين المظهر الاحترافي
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        </style>
    """, unsafe_allow_html=True)

def get_custom_css():
    """CSS مخصص متوافق مع الجوال (iPhone/Android)"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* تحسينات الجوال */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.5rem !important; }
        .stMetric { padding: 5px !important; }
        .dashboard-card { margin-bottom: 10px !important; }
    }

    /* تصميم البطاقات الإحصائية */
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-right: 5px solid #1E3A8A;
        margin-bottom: 1rem;
    }

    .main-header {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* أزرار كبيرة للمس السهل في الجوال */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """
