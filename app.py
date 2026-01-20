import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime
from modules.db import init_db, ensure_settings, add_deal
from modules.auth import login_required, logout
from modules.dashboard import render_dashboard
from modules.style import apply_custom_style, get_custom_css
from modules.evaluation import render_evaluation_module
from modules.report import render_report_module
from modules.admin import render_admin_panel
from modules.municipal_lease_types import MunicipalLeaseTypes
from modules.site_rental_value import SiteRentalValuation

# تطبيق التصميم المطور
apply_custom_style()

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """نظام التقييم مع الخريطة التفاعلية وحفظ البيانات"""
    
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📍 تحديد الموقع", "💰 التقييم الإيجاري", "📄 التقارير"])
        with tab1: self.render_map_selection_tab()
        with tab2: self.render_valuation_tab()
        with tab3: self.render_contract_tab()

    def render_map_selection_tab(self):
        st.subheader("📍 تحديد الموقع الجغرافي للعقار")
        
        col_map, col_inputs = st.columns([2, 1])
        
        with col_map:
            st.info("انقر على الخريطة لتحديد الموقع بدقة")
            # إحداثيات افتراضية (الرياض)
            m = folium.Map(location=[24.7136, 46.6753], zoom_start=12)
            m.add_child(folium.LatLngPopup())
            
            map_data = st_folium(m, height=400, width="100%")
            
            lat, lng = None, None
            if map_data and map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lng = map_data["last_clicked"]["lng"]
                st.success(f"تم التقاط الإحداثيات: {lat:.5f}, {lng:.5f}")

        with col_inputs:
            with st.form("site_info_full_form"):
                site_name = st.text_input("اسم الموقع")
                site_area = st.number_input("المساحة (م²)", min_value=1.0)
                property_type = st.selectbox("نوع العقار", ["تجاري", "سكني", "صناعي"])
                
                if st.form_submit_button("💾 حفظ الموقع في قاعدة البيانات"):
                    if lat and lng:
                        deal_data = {
                            'property_type': property_type,
                            'location': site_name,
                            'area': site_area,
                            'price': 0.0, # يتم تحديثه في تبويب التقييم
                            'deal_date': datetime.now().date(),
                            'latitude': lat,
                            'longitude': lng,
                            'activity_type': 'تأجير بلدي',
                            'notes': f"تم التحديد عبر الخريطة التفاعلية"
                        }
                        deal_id = add_deal(deal_data)
                        st.session_state.current_deal_id = deal_id
                        st.session_state.site_info = deal_data
                        st.success(f"✅ تم حفظ الموقع بنجاح (رقم الصفقة: {deal_id})")
                    else:
                        st.error("⚠️ يرجى النقر على الخريطة أولاً لتحديد الإحداثيات")

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    if not st.session_state.get('authenticated'):
        render_login_page()
    else:
        render_sidebar_navigation()

def render_login_page():
    # كود تسجيل الدخول الأصلي
    pass

def render_sidebar_navigation():
    with st.sidebar:
        st.title("القائمة الرئيسية")
        page = st.radio("انتقل إلى:", ["📊 لوحة التحكم", "📈 التقييم الإيجاري", "👥 الإدارة"])
        if st.button("🚪 خروج"): logout(); st.rerun()

    if "لوحة التحكم" in page: render_dashboard(st.session_state.user_role)
    elif "التقييم" in page: 
        st.header("📍 نظام تحديد القيمة الإيجارية")
        valuator = EnhancedSiteRentalValuation()
        valuator.render_enhanced_valuation()
    elif "الإدارة" in page: render_admin_panel(st.session_state.user_role)

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
