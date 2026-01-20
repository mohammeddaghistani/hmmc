import streamlit as st
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# استيراد الوحدات (تأكد من وجودها في مجلد modules)
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

# تهيئة التصميم
apply_custom_style()

# تهيئة حالة الجلسة الأصلية
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'current_page' not in st.session_state: st.session_state.current_page = "dashboard"

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """النسخة الكاملة المستعادة مع الخرائط والتقارير والعقود"""
    
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📍 معلومات الموقع والخريطة", "💰 التقييم الإيجاري", "📄 العقد والموافقات"])
        with tab1: self.render_site_info_tab()
        with tab2: self.render_valuation_tab()
        with tab3: self.render_contract_tab()

    def render_site_info_tab(self):
        st.subheader("📍 تحديد الموقع الجغرافي")
        col_map, col_inputs = st.columns([2, 1])
        
        with col_map:
            st.info("انقر على الخريطة لتحديد موقع العقار بدقة")
            m = folium.Map(location=[24.7136, 46.6753], zoom_start=6)
            m.add_child(folium.LatLngPopup())
            map_data = st_folium(m, height=400, width="100%", key="site_map")
            
            lat, lng = None, None
            if map_data and map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lng = map_data["last_clicked"]["lng"]
                st.success(f"📍 الإحداثيات الملتقطة: {lat:.5f}, {lng:.5f}")

        with col_inputs:
            with st.form("site_info_full_form"):
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
        st.subheader("💰 التقييم الإيجاري")
        if 'site_info' not in st.session_state:
            st.warning("⚠️ يرجى تحديد الموقع أولاً")
            return
            
        site_data = st.session_state.site_info
        if site_data.get('lat'):
            m_mini = folium.Map(location=[site_data['lat'], site_data['lng']], zoom_start=15)
            folium.Marker([site_data['lat'], site_data['lng']]).add_to(m_mini)
            st_folium(m_mini, height=200, width="100%", key="mini_map")

        col1, col2 = st.columns(2)
        with col1:
            base_rate = st.number_input("السعر للمتر (ريال)", value=100.0)
        with col2:
            st.metric("المساحة", f"{site_data['area']} م²")
        
        total = base_rate * site_data['area']
        st.session_state.calculated_rent = total
        st.metric("الإجمالي السنوي", f"{total:,.2f} ريال")

    def render_contract_tab(self):
        st.subheader("📄 مراجعة العقد")
        if 'calculated_rent' not in st.session_state:
            st.warning("⚠️ أكمل التقييم أولاً")
            return
        
        st.info("تم توليد مسودة العقد بناءً على لوائح التصرف بالعقارات البلدية.")
        if st.button("📝 عرض مسودة الاتفاقية"):
            self.show_agreement_preview(st.session_state.calculated_rent, st.session_state.site_info['zoning'])

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_sidebar_navigation()

def render_login_page():
    st.markdown('<div class="main-header"><h1>🏛️ نظام تأجير العقارات البلدية</h1></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            u = st.text_input("👤 اسم المستخدم")
            p = st.text_input("🔒 كلمة المرور", type="password")
            if st.form_submit_button("دخول"):
                user = login_required(u, p)
                if user:
                    st.session_state.update({"authenticated": True, "user_role": user['role'], "user_name": user['name']})
                    st.rerun()

def render_sidebar_navigation():
    with st.sidebar:
        st.title(f"👤 {st.session_state.user_name}")
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
        if st.button("🚪 خروج", type="secondary"):
            logout(); st.rerun()

    cp = st.session_state.current_page
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
        InvestmentCommitteeSystem().form_committee("الأمانة", st.session_state.get('site_info', {}))
        st.write("إدارة قرارات اللجنة وفقاً للمادة 17.")
    elif cp == 'reports': render_report_module(st.session_state.user_role)
    elif cp == 'admin': render_admin_panel(st.session_state.user_role)

if __name__ == "__main__":
    init_db(); ensure_settings(); main()
