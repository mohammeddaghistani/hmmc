import streamlit as st
from datetime import datetime
from modules.db import init_db, ensure_settings
from modules.auth import login_required, logout
from modules.dashboard import render_dashboard
from modules.style import apply_custom_style, get_custom_css
from modules.evaluation import render_evaluation_module
from modules.report import render_report_module
from modules.admin import render_admin_panel
from modules.municipal_lease_types import MunicipalLeaseTypes

# 1. تهيئة النظام والستايل (تحسين السرعة)
st.set_page_config(page_title="نظام التقييم الإيجاري", layout="wide")
apply_custom_style()

def main():
    # تطبيق CSS المخصص للجوال
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # تهيئة حالة الجلسة
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_sidebar_navigation()

def render_sidebar_navigation():
    """قائمة جانبية متوافقة مع جميع الشاشات"""
    with st.sidebar:
        st.image("assets/logo.png", width=150)
        st.title(f"مرحباً {st.session_state.get('user_name', '')}")
        st.markdown("---")
        
        # قائمة التنقل (أسرع وأفضل للجوال)
        page = st.radio("القائمة الرئيسية", [
            "📊 لوحة التحكم", 
            "📈 التقييم العلمي", 
            "🏛️ أنواع التأجير", 
            "👥 لجان الاستثمار",
            "📑 التقارير", 
            "⚙️ الإدارة"
        ])
        
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            logout()
            st.rerun()

    # توجيه الصفحات
    if "لوحة التحكم" in page: render_dashboard(st.session_state.user_role)
    elif "التقييم" in page: render_evaluation_module(st.session_state.user_role)
    elif "أنواع" in page: render_lease_types_page()
    elif "التقارير" in page: render_report_module(st.session_state.user_role)
    elif "الإدارة" in page: render_admin_panel(st.session_state.user_role)

# استكمال الدوال الأخرى (login_page, etc) بنفس المنطق الأصلي
