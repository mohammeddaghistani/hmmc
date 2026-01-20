import streamlit as st
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# استيراد الوحدات المحلية
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

# تطبيق التصميم والتهيئة
apply_custom_style()

def get_coordinates_from_address(address):
    """تحويل العنوان النصي إلى إحداثيات جغرافية"""
    try:
        geolocator = Nominatim(user_agent="rental_app")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except:
        return None
    return None

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """النسخة الاحترافية الكاملة لنظام التقييم"""
    
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📍 تحديد الموقع الجغرافي", "💰 التقييم الإيجاري", "📄 مراجعة العقد"])
        with tab1: self.render_site_info_tab()
        with tab2: self.render_valuation_tab()
        with tab3: self.render_contract_tab()

    def render_site_info_tab(self):
        st.subheader("📍 تحديد الموقع على الخريطة")
        col_map, col_inputs = st.columns([2, 1])
        
        with col_map:
            st.info("قم بالنقر على الخريطة لتحديد موقع العقار بدقة")
            m = folium.Map(location=[24.7136, 46.6753], zoom_start=6)
            m.add_child(folium.LatLngPopup())
            map_data = st_folium(m, height=400, width="100%", key="main_map")
            
            lat, lng = None, None
            if map_data and map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lng = map_data["last_clicked"]["lng"]
                st.success(f"تم التقاط الإحداثيات: {lat:.5f}, {lng:.5f}")

        with col_inputs:
            with st.form("site_info_main_form"):
                site_name = st.text_input("اسم الموقع أو المشروع")
                site_area = st.number_input("المساحة الإجمالية (م²)", min_value=1.0, value=1000.0)
                city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
                prop_type = st.selectbox("نوع العقار", ["تجاري", "سكني", "صناعي"])
                
                if st.form_submit_button("💾 حفظ البيانات والموقع"):
                    if lat and lng:
                        st.session_state.site_info = {
                            'name': site_name, 'area': site_area, 'city': city,
                            'lat': lat, 'lng': lng, 'type': prop_type
                        }
                        st.success("✅ تم حفظ بيانات الموقع")
                    else:
                        st.error("⚠️ يرجى تحديد الموقع على الخريطة أولاً")

    def render_valuation_tab(self):
        st.subheader("💰 حساب القيمة الإيجارية")
        if 'site_info' not in st.session_state:
            st.warning("⚠️ يرجى إكمال بيانات الموقع أولاً")
            return
            
        if st.session_state.site_info.get('lat'):
            mini_map = folium.Map(location=[st.session_state.site_info['lat'], st.session_state.site_info['lng']], zoom_start=15)
            folium.Marker([st.session_state.site_info['lat'], st.session_state.site_info['lng']]).add_to(mini_map)
            st_folium(mini_map, height=200, width="100%", key="mini_map")
        
        base_rate = st.number_input("السعر المقترح للمتر (ريال)", value=100.0)
        total = base_rate * st.session_state.site_info['area']
        st.session_state.calculated_rent = total
        st.metric("إجمالي القيمة الإيجارية السنوية", f"{total:,.2f} ريال")

    def render_contract_tab(self):
        """هذه هي الدالة التي كانت مفقودة وتسببت في الخطأ"""
        st.subheader("📄 مراجعة العقد والموافقات")
        if 'site_info' not in st.session_state or 'calculated_rent' not in st.session_state:
            st.warning("⚠️ يرجى إكمال بيانات الموقع والتقييم أولاً")
            return
        
        st.info("بناءً على البيانات المدخلة، تم تجهيز مسودة العقد الأولية.")
        if st.button("📋 عرض مسودة الاتفاقية"):
            self.show_agreement_preview(st.session_state.calculated_rent, st.session_state.site_info['type'])

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False

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
            if st.form_submit_button("دخول للنظام"):
                user = login_required(u, p)
                if user:
                    st.session_state.update({"authenticated": True, "user_role": user['role'], "user_name": user['name'], "current_page": "dashboard"})
                    st.rerun()
                else:
                    st.error("⚠️ بيانات الدخول غير صحيحة")

def render_sidebar_navigation():
    with st.sidebar:
        st.title(f"مرحباً {st.session_state.user_name}")
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
            logout(); st.rerun()

    cp = st.session_state.get('current_page', 'dashboard')
    if cp == 'dashboard': render_dashboard(st.session_state.user_role)
    elif cp == 'evaluation': render_evaluation_module(st.session_state.user_role)
    elif cp == 'site_rental':
        valuator = EnhancedSiteRentalValuation()
        valuator.render_enhanced_valuation()
    elif cp == 'reports': render_report_module(st.session_state.user_role)
    elif cp == 'admin': render_admin_panel(st.session_state.user_role)
    elif cp == 'lease_types': 
        st.header("🏛️ أنواع التأجير البلدية")
        MunicipalLeaseTypes().render_lease_type_selection()

if __name__ == "__main__":
    init_db(); ensure_settings(); main()
