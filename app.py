import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# الوحدات النمطية
from modules.db import init_db, ensure_settings
from modules.auth import login_required, logout
from modules.dashboard import render_dashboard
from modules.style import apply_custom_style, get_custom_css
from modules.evaluation import render_evaluation_module
from modules.report import render_report_module
from modules.admin import render_admin_panel
from modules.site_rental_value import SiteRentalValuation
from modules.municipal_lease_types import MunicipalLeaseTypes
from modules.investment_committee import InvestmentCommitteeSystem

# تطبيق التصميم المخصص
apply_custom_style()

# تهيئة حالة الجلسة
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"
if 'selected_lease_type' not in st.session_state:
    st.session_state.selected_lease_type = None
if 'selected_subtype' not in st.session_state:
    st.session_state.selected_subtype = None

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """نسخة محسنة من نظام التقييم تتوافق مع اللوائح"""
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📋 معلومات الموقع", "💰 التقييم الإيجاري", "📄 العقد والموافقات"])
        with tab1: self.render_site_info_tab()
        with tab2: self.render_valuation_tab()
        with tab3: self.render_contract_tab()

    def render_site_info_tab(self):
        st.subheader("📍 معلومات الموقع الأساسية")
        with st.form("site_info_form"):
            col1, col2 = st.columns(2)
            with col1:
                site_name = st.text_input("اسم الموقع الرسمي")
                site_code = st.text_input("رقم الموقع")
                site_area = st.number_input("مساحة الموقع (م²)", min_value=1.0, value=1000.0)
                frontage = st.number_input("طول الواجهة (م)", min_value=0.0, value=20.0)
            with col2:
                city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
                district = st.text_input("الحي")
                zoning = st.selectbox("التصنيف", ["سكني", "تجاري", "صناعي"])
                allowed_uses = st.text_area("الاستخدامات المسموحة")
            if st.form_submit_button("💾 حفظ"):
                st.session_state.site_info = {'name': site_name, 'area': site_area, 'city': city}
                st.success("✅ تم الحفظ")

    def render_valuation_tab(self):
        st.subheader("💰 التقييم الإيجاري")
        if 'site_info' not in st.session_state:
            st.warning("⚠️ أدخل معلومات الموقع أولاً")
            return
        # كود التقييم المختصر هنا
        st.metric("المساحة", f"{st.session_state.site_info['area']} م²")
        rate = st.number_input("السعر للمتر", value=50.0)
        st.metric("الإجمالي", f"{rate * st.session_state.site_info['area']:,.0f} ريال")

    def render_contract_tab(self):
        st.subheader("📄 العقد")
        st.info("سيتم توليد العقد بناءً على البيانات أعلاه.")

def main():
    custom_css = get_custom_css() + """
    <style>
    .rtl-text { direction: rtl; text-align: right; }
    .lease-type-card { border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; background: white; text-align: right; }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="main-header">
        <h1 class="app-title">🏛️ نظام تأجير العقارات البلدية</h1>
        <p>التاريخ: {datetime.now().strftime("%Y-%m-%d")}</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_main_application()

def render_login_page():
    with st.form("login_form"):
        username = st.text_input("👤 اسم المستخدم")
        password = st.text_input("🔒 كلمة المرور", type="password")
        if st.form_submit_button("🚀 دخول"):
            user = login_required(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_role = user.get('role', 'guest')
                st.session_state.user_name = user.get('name', 'مستخدم')
                st.rerun()

def render_main_application():
    render_enhanced_navigation_bar()
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard': render_dashboard(st.session_state.user_role)
    elif page == 'evaluation': render_evaluation_module(st.session_state.user_role)
    elif page == 'site_rental': render_enhanced_site_rental_page()
    elif page == 'lease_types': render_lease_types_page()
    elif page == 'committee': render_committee_page()
    elif page == 'reports': render_report_module(st.session_state.user_role)
    elif page == 'admin': render_admin_panel(st.session_state.user_role)

def render_enhanced_navigation_bar():
    cols = st.columns([2, 1, 1, 1, 1, 1, 1])
    with cols[1]: 
        if st.button("📊 لوحة التحكم"): st.session_state.current_page = 'dashboard'; st.rerun()
    with cols[2]: 
        if st.button("📈 التقييم"): st.session_state.current_page = 'evaluation'; st.rerun()
    with cols[3]: 
        if st.button("🏛️ الأنواع"): st.session_state.current_page = 'lease_types'; st.rerun()
    with cols[4]: 
        if st.button("👥 اللجنة"): st.session_state.current_page = 'committee'; st.rerun()
    with cols[6]:
        if st.button("🚪 خروج"): 
            logout(); st.session_state.authenticated = False; st.rerun()

def render_enhanced_site_rental_page():
    st.header("📍 نظام تحديد القيمة الإيجارية")
    if not st.session_state.selected_lease_type:
        st.warning("⚠️ اختر نوع التأجير أولاً")
        if st.button("🏛️ الذهاب للأنواع"): 
            st.session_state.current_page = 'lease_types'; st.rerun()
        return
    
    lease_types = MunicipalLeaseTypes()
    details = lease_types.get_lease_type_details(st.session_state.selected_lease_type, st.session_state.selected_subtype)
    if details:
        st.info(f"النوع المحدد: {details.get('name')}")
    
    valuator = EnhancedSiteRentalValuation()
    valuator.render_enhanced_valuation()

def render_lease_types_page():
    st.header("🏛️ أنواع التأجير البلدية")
    lease_types = MunicipalLeaseTypes()
    tab1, tab2, tab3 = st.tabs(["📋 مؤقت", "🏗️ طويل الأجل", "🎯 مباشر"])
    
    with tab1:
        st.write("تأجير لمدة 6 أشهر قابلة للتمديد.")
        if st.button("✅ اختيار مؤقت"):
            st.session_state.selected_lease_type = 'TEMPORARY_ACTIVITY'
            st.success("تم الاختيار"); st.rerun()
    
    with tab2:
        st.write("تأجير استثماري يصل لـ 25-50 سنة.")
        if st.button("✅ اختيار طويل الأجل"):
            st.session_state.selected_lease_type = 'LONG_TERM_INVESTMENT'
            st.success("تم الاختيار"); st.rerun()

def render_committee_page():
    st.header("👥 لجنة الاستثمار")
    st.write("إدارة قرارات اللجنة وتشكيل الأعضاء.")

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
