import streamlit as st
import folium
from streamlit_folium import st_folium
from modules.db import init_db, ensure_settings, get_setting
from modules.style import apply_custom_style, get_custom_css
from modules.evaluation import render_evaluation_module
from modules.admin import render_admin_panel
from modules.dashboard import render_dashboard
from modules.report import render_report_module
from modules.investment_committee import InvestmentCommitteeSystem
from modules.municipal_lease_types import MunicipalLeaseTypes
from modules.site_rental_value import SiteRentalValuation

apply_custom_style()
init_db()
ensure_settings()

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """تطوير واجهة تحديد القيمة الإيجارية للمواقع"""
    def render_enhanced_valuation(self):
        tab1, tab2, tab3 = st.tabs(["📍 الموقع والخريطة المزدوجة", "💰 حساب القيمة", "📄 المسودة"])
        with tab1: self.render_dual_map_tab()
        with tab2: self.render_calculations_tab()
        with tab3: self.render_contract_tab()

    def render_dual_map_tab(self):
        st.subheader("📍 تحديد الموقع (عرض الأقمار الصناعية متاح)")
        map_type = st.radio("نوع الخريطة", ["خريطة الشوارع", "أقمار صناعية (Satellite)"], horizontal=True)
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" if "أقمار" in map_type else "OpenStreetMap"
        attr = "Esri Satellite" if "أقمار" in map_type else "OSM"
        
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=6, tiles=tiles, attr=attr)
        m.add_child(folium.LatLngPopup())
        output = st_folium(m, height=400, width="100%", key="site_map")
        if output.get("last_clicked"):
            st.session_state.lat = output["last_clicked"]["lat"]
            st.session_state.lng = output["last_clicked"]["lng"]
            st.success(f"تم تحديد الإحداثيات: {st.session_state.lat:.5f}, {st.session_state.lng:.5f}")

    def render_calculations_tab(self):
        # استرجاع منطق الحسابات الأصلي وربطه بالمعدلات من الإدارة
        area = st.number_input("المساحة م²", value=1000.0)
        base_p = st.number_input("السعر الاسترشادي", value=200.0)
        # جلب المعامل المحدث من قاعدة البيانات
        mult = float(get_setting('mult_temp', 0.85))
        st.metric("القيمة الإيجارية السنوية", f"{area * base_p * mult:,.2f} ريال")

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    with st.sidebar:
        st.title("🏛️ نظام التأجير البلدي")
        choice = st.radio("القائمة", ["📊 لوحة التحكم", "📈 التقييم العلمي", "📍 القيمة الإيجارية", "👥 اللجنة", "⚙️ الإعدادات"])

    if choice == "📊 لوحة التحكم": render_dashboard('admin')
    elif choice == "📈 التقييم العلمي": render_evaluation_module('admin')
    elif choice == "📍 القيمة الإيجارية": EnhancedSiteRentalValuation().render_enhanced_valuation()
    elif choice == "👥 اللجنة": InvestmentCommitteeSystem().render_committee_module()
    elif choice == "⚙️ الإعدادات": render_admin_panel('admin')

if __name__ == "__main__":
    main()
