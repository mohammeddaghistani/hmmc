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

# تهيئة النظام الأساسي
apply_custom_style()
init_db()
ensure_settings()

class EnhancedApp:
    def __init__(self):
        self.lease_manager = MunicipalLeaseTypes()
        self.committee_manager = InvestmentCommitteeSystem()
        self.valuator = SiteRentalValuation()

    def render_dual_map(self):
        """تفعيل الخريطة المزدوجة (Satellite + Street)"""
        st.subheader("📍 تحديد الموقع الجغرافي (عرض الأقمار الصناعية)")
        
        map_type = st.radio("نوع العرض", ["أقمار صناعية (Satellite)", "خريطة الشوارع"], horizontal=True)
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" if "أقمار" in map_type else "OpenStreetMap"
        attr = "Esri Satellite Imagery" if "أقمار" in map_type else "OpenStreetMap"

        m = folium.Map(location=[24.7136, 46.6753], zoom_start=6, tiles=tiles, attr=attr)
        m.add_child(folium.LatLngPopup())
        
        output = st_folium(m, height=450, width="100%", key="main_map")
        
        if output.get("last_clicked"):
            st.session_state.lat = output["last_clicked"]["lat"]
            st.session_state.lng = output["last_clicked"]["lng"]
            st.success(f"📍 تم تحديد الموقع: {st.session_state.lat:.5f}, {st.session_state.lng:.5f}")

    def run(self):
        st.markdown(get_custom_css(), unsafe_allow_html=True)
        if 'authenticated' not in st.session_state: st.session_state.authenticated = False

        if not st.session_state.authenticated:
            self.render_login()
        else:
            self.render_main_interface()

    def render_login(self):
        st.markdown('<div class="main-header"><h1>🏛️ نظام تأجير العقارات البلدية</h1></div>', unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول"):
                st.session_state.authenticated = True
                st.rerun()

    def render_main_interface(self):
        with st.sidebar:
            st.title("القائمة الرئيسية")
            choice = st.radio("انتقل إلى:", ["📊 لوحة التحكم", "📈 التقييم الإيجاري", "👥 لجنة الاستثمار", "📑 التقارير", "⚙️ الإعدادات"])
        
        if choice == "📊 لوحة التحكم": render_dashboard('admin')
        elif choice == "📈 التقييم الإيجاري": self.render_valuation_page()
        elif choice == "👥 لجنة الاستثمار": self.committee_manager.render_committee_module()
        elif choice == "📑 التقارير": render_report_module('admin')
        elif choice == "⚙️ الإعدادات": render_admin_panel('admin')

    def render_valuation_page(self):
        st.header("📍 تقييم القيمة الإيجارية للموقع")
        self.render_dual_map()
        
        st.divider()
        selected_key = self.lease_manager.render_lease_type_selection()
        
        # جلب المعامل من الإعدادات العامة
        mult_key = self.lease_manager.lease_types[selected_key]['multiplier_key']
        multiplier = float(get_setting(mult_key, 1.0))
        
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input("المساحة الإجمالية م²", value=500.0)
            base_p = st.number_input("السعر الاسترشادي للمتر (ريال)", value=200.0)
        with col2:
            final_rent = area * base_p * multiplier
            st.metric("القيمة الإيجارية السنوية", f"{final_rent:,.2f} ريال")
            st.caption(f"تم تطبيق معامل ضرب: {multiplier}")

if __name__ == "__main__":
    app = EnhancedApp()
    app.run()
