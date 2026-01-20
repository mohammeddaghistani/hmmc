import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

# الوحدات المحلية
from modules.db import init_db, ensure_settings, get_setting, add_deal
from modules.style import apply_custom_style, get_custom_css
from modules.evaluation import render_evaluation_module
from modules.admin import render_admin_panel
from modules.dashboard import render_dashboard
from modules.report import render_report_module
from modules.investment_committee import InvestmentCommitteeSystem
from modules.municipal_lease_types import MunicipalLeaseTypes
from modules.site_rental_value import SiteRentalValuation

# التهيئة
apply_custom_style()
init_db()
ensure_settings()

class EnhancedApp:
    def __init__(self):
        self.lease_manager = MunicipalLeaseTypes()
        self.committee_manager = InvestmentCommitteeSystem()

    def render_dual_map(self):
        """خريطة مزدوجة: أساسية + ستلايت"""
        st.subheader("📍 تحديد الموقع الجغرافي")
        m_type = st.radio("نوع الخريطة", ["خريطة الشوارع", "أقمار صناعية (Satellite)"], horizontal=True)
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" if "أقمار" in m_type else "OpenStreetMap"
        attr = "Esri Satellite" if "أقمار" in m_type else "OSM"

        m = folium.Map(location=[24.7136, 46.6753], zoom_start=6, tiles=tiles, attr=attr)
        m.add_child(folium.LatLngPopup())
        output = st_folium(m, height=450, width="100%", key="main_map")
        
        if output.get("last_clicked"):
            st.session_state.lat = output["last_clicked"]["lat"]
            st.session_state.lng = output["last_clicked"]["lng"]
            st.success(f"📍 الإحداثيات: {st.session_state.lat:.5f}, {st.session_state.lng:.5f}")

    def run(self):
        st.markdown(get_custom_css(), unsafe_allow_html=True)
        
        with st.sidebar:
            st.title("🏛️ نظام التأجير البلدي")
            choice = st.radio("القائمة الرئيسية", ["📊 لوحة التحكم", "📈 التقييم الإيجاري", "👥 لجنة الاستثمار", "📉 التقييم العلمي", "📑 التقارير", "⚙️ الإدارة"])

        if choice == "📊 لوحة التحكم": render_dashboard('admin')
        elif choice == "📈 التقييم الإيجاري": self.render_rental_valuation()
        elif choice == "👥 لجنة الاستثمار": self.committee_manager.render_committee_module()
        elif choice == "📉 التقييم العلمي": render_evaluation_module('admin')
        elif choice == "📑 التقارير": render_report_module('admin')
        elif choice == "⚙️ الإدارة": render_admin_panel('admin')

    def render_rental_valuation(self):
        st.header("📍 تقييم القيمة الإيجارية")
        self.render_dual_map()
        
        st.divider()
        lt_options = self.lease_manager.get_lease_options()
        selected_key = st.selectbox("نوع التأجير المطلوب", options=list(lt_options.keys()), format_func=lambda x: lt_options[x])
        
        # جلب المعامل من الإدارة
        mult_key = self.lease_manager.lease_types[selected_key]['multiplier_key']
        multiplier = float(get_setting(mult_key, 1.0))
        
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input("المساحة الإجمالية (م²)", value=1000.0)
            base_p = st.number_input("السعر الاسترشادي للمتر", value=200.0)
        with col2:
            final_rent = area * base_p * multiplier
            st.metric("القيمة الإيجارية السنوية", f"{final_rent:,.2f} ريال")
            st.info(f"المعامل المطبق: {multiplier}")
        
        if st.button("📝 إرسال لقرار اللجنة"):
            self.committee_manager.render_decision_maker(area, base_p, multiplier)

if __name__ == "__main__":
    app = EnhancedApp()
    app.run()
