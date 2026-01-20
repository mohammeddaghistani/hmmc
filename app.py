import streamlit as st
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# استيراد كافة الوحدات مع التأكد من وجودها في مجلد modules
from modules.db import init_db, ensure_settings, add_deal
from modules.auth import login_required, logout
from modules.dashboard import render_dashboard
from modules.style import apply_custom_style, get_custom_css
from modules.evaluation import render_evaluation_module
from modules.report import render_report_module
from modules.admin import render_admin_panel
from modules.site_rental_value import SiteRentalValuation
from modules.municipal_lease_types import MunicipalLeaseTypes
from modules.investment_committee import InvestmentCommitteeSystem

# تهيئة النظام [cite: 1, 10]
apply_custom_style()

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """النسخة الشاملة: تدمج الخريطة مع منطق التقييم والعقود الأصلي"""
    
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📍 معلومات الموقع والخريطة", "💰 الحسابات التقديرية", "📄 مسودة العقد"])
        with tab1: self.render_site_info_tab()
        with tab2: self.render_valuation_tab()
        with tab3: self.render_contract_tab()

    def render_site_info_tab(self):
        st.subheader("📍 تحديد الموقع الجغرافي")
        col_map, col_inputs = st.columns([2, 1])
        
        with col_map:
            st.info("انقر على الخريطة لتحديد موقع العقار")
            m = folium.Map(location=[24.7136, 46.6753], zoom_start=6)
            m.add_child(folium.LatLngPopup())
            map_data = st_folium(m, height=400, width="100%", key="map_input")
            
            lat, lng = None, None
            if map_data and map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lng = map_data["last_clicked"]["lng"]
                st.success(f"📍 الإحداثيات: {lat:.5f}, {lng:.5f}")

        with col_inputs:
            with st.form("site_info_form"):
                site_name = st.text_input("اسم الموقع الرسمي")
                site_area = st.number_input("مساحة الموقع (م²)", min_value=1.0, value=1000.0)
                city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
                zoning = st.selectbox("التصنيف", ["سكني", "تجاري", "صناعي"])
                
                if st.form_submit_button("💾 حفظ البيانات"):
                    st.session_state.site_info = {
                        'name': site_name, 'area': site_area, 'city': city,
                        'lat': lat, 'lng': lng, 'zoning': zoning
                    }
                    st.success("✅ تم حفظ معلومات الموقع")

    def render_valuation_tab(self):
        st.subheader("💰 حساب القيمة الإيجارية")
        if 'site_info' not in st.session_state:
            st.warning("⚠️ يرجى تحديد الموقع أولاً")
            return
            
        # دمج عوامل التقييم الأصلية [cite: 14]
        site_data = st.session_state.site_info
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                base_price = st.number_input("السعر الأساسي للمتر (ريال)", min_value=0.0, value=100.0)
                duration = st.number_input("مدة العقد (سنوات)", min_value=1, value=10)
            with col2:
                # عرض الموقع الصغير للتأكيد
                if site_data.get('lat'):
                    m_mini = folium.Map(location=[site_data['lat'], site_data['lng']], zoom_start=15)
                    folium.Marker([site_data['lat'], site_data['lng']]).add_to(m_mini)
                    st_folium(m_mini, height=150, width="100%", key="mini_map")

            # الحساب بناءً على معادلتك الأصلية [cite: 14]
            total_value = base_price * site_data['area'] * duration
            st.session_state.calculated_total = total_value
            st.metric("إجمالي القيمة التقديرية", f"{total_value:,.2f} ريال")

    def render_contract_tab(self):
        st.subheader("📄 مسودة الاتفاقية")
        if 'calculated_total' not in st.session_state:
            st.warning("⚠️ أكمل التقييم أولاً")
            return
            
        # استدعاء عرض المسودة الأصلي من ملف site_rental_value.py [cite: 14]
        if st.button("📝 توليد وعرض مسودة الاتفاقية"):
            self.show_agreement_preview(
                st.session_state.calculated_total, 
                st.session_state.site_info['zoning']
            )

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_main_navigation()

def render_login_page():
    # كود تسجيل الدخول الأصلي [cite: 1, 7]
    st.markdown('<div class="main-header"><h1>🏛️ نظام تأجير العقارات البلدية</h1></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم")
            password = st.text_input("🔒 كلمة المرور", type="password")
            if st.form_submit_button("دخول"):
                user = login_required(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_role = user['role']
                    st.session_state.user_name = user['name']
                    st.rerun()

def render_main_navigation():
    """القائمة الجانبية التي تضمن الوصول لكافة الأقسام الأصلية"""
    with st.sidebar:
        st.title(f"👤 {st.session_state.user_name}")
        st.markdown("---")
        
        menu = {
            "📊 لوحة التحكم": "dashboard",
            "📈 التقييم العلمي (IVS)": "evaluation",
            "🏛️ أنواع التأجير البلدية": "lease_types",
            "📍 القيمة الإيجارية للموقع": "site_rental",
            "👥 لجنة الاستثمار": "committee",
            "📑 التقارير والإحصائيات": "reports",
            "⚙️ لوحة الإدارة": "admin"
        }
        
        for label, page in menu.items():
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", type="secondary"):
            logout(); st.rerun()

    # التوجيه مع الحفاظ على كافة الخصائص [cite: 1, 10, 11]
    cp = st.session_state.get('current_page', 'dashboard')
    
    if cp == 'dashboard': render_dashboard(st.session_state.user_role)
    elif cp == 'evaluation': render_evaluation_module(st.session_state.user_role)
    elif cp == 'lease_types': 
        st.header("🏛️ أنواع التأجير البلدية")
        MunicipalLeaseTypes().render_lease_type_selection()
    elif cp == 'site_rental':
        valuator = EnhancedSiteRentalValuation()
        valuator.render_enhanced_valuation()
    elif cp == 'committee':
        st.header("👥 لجنة الاستثمار")
        # استدعاء نظام اللجنة الأصلي [cite: 12]
        comm = InvestmentCommitteeSystem()
        st.write("إدارة قرارات اللجنة وتشكيل الأعضاء وفقاً للمادة 17.")
    elif cp == 'reports': render_report_module(st.session_state.user_role)
    elif cp == 'admin': render_admin_panel(st.session_state.user_role)

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
