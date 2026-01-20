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
from modules.investment_committee import InvestmentCommitteeSystem

# تطبيق الإعدادات الأولية
apply_custom_style()

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # تهيئة حالة الجلسة [cite: 3]
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"

    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_main_navigation()

def render_login_page():
    st.markdown('<div class="main-header"><h1>🏛️ نظام تأجير العقارات البلدية</h1></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.subheader("🔐 تسجيل الدخول")
                username = st.text_input("👤 اسم المستخدم")
                password = st.text_input("🔒 كلمة المرور", type="password")
                if st.form_submit_button("دخول"):
                    user = login_required(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_role = user['role']
                        st.session_state.user_name = user['name']
                        st.rerun()
                    else:
                        st.error("خطأ في البيانات")

def render_main_navigation():
    """نظام التنقل الجانبي المتوافق مع الجوال"""
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.info(f"الدور: {st.session_state.user_role}")
        st.markdown("---")
        
        # خيارات القائمة
        menu = {
            "📊 لوحة التحكم": "dashboard",
            "📈 التقييم العلمي": "evaluation",
            "🏛️ أنواع التأجير": "lease_types",
            "👥 لجان الاستثمار": "committee",
            "📑 التقارير": "reports",
            "⚙️ الإدارة": "admin"
        }
        
        for label, page_id in menu.items():
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 خروج", type="secondary", use_container_width=True):
            logout()
            st.rerun()

    # عرض الصفحة المختارة [cite: 3]
    page = st.session_state.current_page
    if page == 'dashboard': render_dashboard(st.session_state.user_role)
    elif page == 'evaluation': render_evaluation_module(st.session_state.user_role)
    elif page == 'lease_types': render_lease_types_page()
    elif page == 'committee': render_committee_page()
    elif page == 'reports': render_report_module(st.session_state.user_role)
    elif page == 'admin': render_admin_panel(st.session_state.user_role)

# الدوال الفرعية (Lease Types & Committee) يتم استدعاؤها من ملفاتها الأصلية
def render_lease_types_page():
    st.header("🏛️ أنواع التأجير البلدية")
    # الكود الأصلي الخاص بـ MunicipalLeaseTypes [cite: 12]

def render_committee_page():
    st.header("👥 لجنة الاستثمار")
    # الكود الأصلي الخاص بـ InvestmentCommitteeSystem [cite: 11, 15]

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
