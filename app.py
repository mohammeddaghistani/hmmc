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
from modules.site_rental_value import SiteRentalValuation

# تطبيق التصميم والتهيئة
apply_custom_style()

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """نسخة محسنة من نظام التقييم تتوافق مع اللوائح"""
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📍 معلومات الموقع", "💰 التقييم الإيجاري", "📄 العقد والموافقات"])
        with tab1: self.render_site_info_tab()
        with tab2: self.render_valuation_tab()
        with tab3: self.render_contract_tab()

    def render_site_info_tab(self):
        st.subheader("📍 معلومات الموقع الأساسية")
        with st.form("site_info_form"):
            col1, col2 = st.columns([1, 1])
            with col1:
                site_name = st.text_input("اسم الموقع الرسمي")
                site_area = st.number_input("مساحة الموقع (م²)", min_value=1.0, value=1000.0)
            with col2:
                city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
                zoning = st.selectbox("التصنيف", ["سكني", "تجاري", "صناعي"])
            if st.form_submit_button("💾 حفظ"):
                st.session_state.site_info = {'name': site_name, 'area': site_area, 'city': city}
                st.success("✅ تم حفظ البيانات")

    def render_valuation_tab(self):
        st.subheader("💰 التقييم الإيجاري")
        if 'site_info' not in st.session_state:
            st.warning("⚠️ أدخل معلومات الموقع أولاً")
            return
        st.metric("المساحة الإجمالية", f"{st.session_state.site_info['area']} م²")
        rate = st.number_input("السعر المقترح للمتر", value=50.0)
        st.metric("إجمالي القيمة الإيجارية", f"{rate * st.session_state.site_info['area']:,.0f} ريال")

    def render_contract_tab(self):
        st.subheader("📄 العقد")
        st.info("سيتم توليد العقد بناءً على البيانات المدخلة.")

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_sidebar_app()

def render_login_page():
    st.markdown('<div class="main-header"><h1>🏛️ نظام تأجير العقارات البلدية</h1></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.subheader("🔐 تسجيل الدخول")
                username = st.text_input("👤 اسم المستخدم")
                password = st.text_input("🔒 كلمة المرور", type="password")
                if st.form_submit_button("دخول للنظام"):
                    user = login_required(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_role = user.get('role', 'guest')
                        st.session_state.user_name = user.get('name', 'مستخدم')
                        st.rerun()
                    else:
                        st.error("⚠️ خطأ في اسم المستخدم أو كلمة المرور")

def render_sidebar_app():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.caption(f"الدور: {st.session_state.user_role}")
        st.markdown("---")
        
        menu = {
            "📊 لوحة التحكم": "dashboard",
            "📈 التقييم العلمي": "evaluation",
            "🏛️ أنواع التأجير": "lease_types",
            "📍 قيمة الموقع": "site_rental",
            "👥 لجنة الاستثمار": "committee",
            "📑 التقارير": "reports",
            "⚙️ الإدارة": "admin"
        }
        
        for label, page in menu.items():
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 خروج", type="secondary", use_container_width=True):
            logout()
            st.session_state.authenticated = False
            st.rerun()

    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard': render_dashboard(st.session_state.user_role)
    elif current_page == 'evaluation': render_evaluation_module(st.session_state.user_role)
    elif current_page == 'lease_types': render_lease_types_page()
    elif current_page == 'site_rental': render_enhanced_site_rental_page()
    elif current_page == 'committee': render_committee_page()
    elif current_page == 'reports': render_report_module(st.session_state.user_role)
    elif current_page == 'admin': render_admin_panel(st.session_state.user_role)

def render_lease_types_page():
    st.header("🏛️ أنواع التأجير البلدية")
    lease_types = MunicipalLeaseTypes()
    tab1, tab2, tab3 = st.tabs(["📋 مؤقت", "🏗️ طويل الأجل", "🎯 مباشر"])
    with tab1:
        st.write("تأجير لمدة 6 أشهر قابلة للتمديد.")
        if st.button("✅ اختيار مؤقت"):
            st.session_state.selected_lease_type = 'TEMPORARY_ACTIVITY'
            st.success("تم الاختيار")
    with tab2:
        st.write("تأجير استثمار استراتيجي.")
        if st.button("✅ اختيار طويل الأجل"):
            st.session_state.selected_lease_type = 'LONG_TERM_INVESTMENT'
            st.success("تم الاختيار")

def render_enhanced_site_rental_page():
    st.header("📍 نظام تحديد القيمة الإيجارية")
    valuator = EnhancedSiteRentalValuation()
    valuator.render_enhanced_valuation()

def render_committee_page():
    st.header("👥 لجنة الاستثمار")
    system = InvestmentCommitteeSystem()
    st.write("إدارة قرارات اللجنة وفقاً للمادة 17 من اللائحة.")

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
