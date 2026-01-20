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
    """نسخة محسنة تدعم الخرائط واللوائح البلدية"""
    
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📍 تحديد الموقع", "💰 التقييم الإيجاري", "📄 العقد"])
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
            map_data = st_folium(m, height=400, width="100%")
            
            lat, lng = None, None
            if map_data and map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lng = map_data["last_clicked"]["lng"]
                st.success(f"الإحداثيات الملتقطة: {lat:.5f}, {lng:.5f}")

        with col_inputs:
            with st.form("site_info_form"):
                site_name = st.text_input("اسم الموقع")
                site_area = st.number_input("مساحة الموقع (م²)", min_value=1.0, value=1000.0)
                city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
                
                if st.form_submit_button("💾 حفظ البيانات"):
                    st.session_state.site_info = {
                        'name': site_name, 'area': site_area, 'city': city,
                        'lat': lat, 'lng': lng
                    }
                    st.success("✅ تم الحفظ")

    def render_valuation_tab(self):
        st.subheader("💰 التقييم الإيجاري")
        if 'site_info' not in st.session_state:
            st.warning("⚠️ حدد الموقع من الخريطة أولاً")
            return
            
        if st.session_state.site_info.get('lat'):
            mini_map = folium.Map(location=[st.session_state.site_info['lat'], st.session_state.site_info['lng']], zoom_start=15)
            folium.Marker([st.session_state.site_info['lat'], st.session_state.site_info['lng']]).add_to(mini_map)
            st_folium(mini_map, height=200, width="100%")
        
        rate = st.number_input("السعر للمتر", value=100.0)
        st.metric("الإجمالي التقديري", f"{rate * st.session_state.site_info['area']:,.0f} ريال")

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False

    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_sidebar_app()

def render_login_page():
    with st.container():
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

def render_sidebar_app():
    with st.sidebar:
        st.title(f"👤 {st.session_state.user_name}")
        page = st.radio("القائمة", ["📊 لوحة التحكم", "📈 التقييم", "📍 قيمة الموقع", "👥 اللجنة", "📑 التقارير", "⚙️ الإدارة"])
        if st.button("🚪 خروج"): logout(); st.rerun()

    if "لوحة التحكم" in page: render_dashboard(st.session_state.user_role)
    elif "التقييم" in page: render_evaluation_module(st.session_state.user_role)
    elif "قيمة الموقع" in page: 
        valuator = EnhancedSiteRentalValuation()
        valuator.render_enhanced_valuation()
    elif "التقارير" in page: render_report_module(st.session_state.user_role)
    elif "الإدارة" in page: render_admin_panel(st.session_state.user_role)

if __name__ == "__main__":
    init_db(); ensure_settings(); main()
