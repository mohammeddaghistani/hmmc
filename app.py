import streamlit as st
import folium
from streamlit_folium import st_folium
from modules.db import init_db, ensure_settings, get_setting
from modules.municipal_lease_types import MunicipalLeaseTypes
from modules.investment_committee import InvestmentCommitteeSystem
from modules.style import apply_custom_style, get_custom_css
from modules.valuation_methods import ValuationMethods
from modules.evaluation import render_evaluation_module
from modules.admin import render_admin_panel
from modules.dashboard import render_dashboard
from modules.report import render_report_module

# تهيئة النظام
apply_custom_style()
init_db()
ensure_settings()

class EnhancedApp:
    def __init__(self):
        self.lease_manager = MunicipalLeaseTypes()
        self.committee_manager = InvestmentCommitteeSystem()
        self.valuation_engine = ValuationMethods()

    def render_dual_map(self):
        """خريطة مزدوجة: أساسية + ستلايت"""
        st.subheader("📍 تحديد الموقع (عرض ستلايت متاح)")
        
        # اختيار الطبقة من قبل المستخدم
        map_type = st.radio("نوع الخريطة", ["ستلايت (أقمار صناعية)", "خريطة الشوارع"], horizontal=True)
        
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" if "ستلايت" in map_type else "OpenStreetMap"
        attr = "Esri World Imagery" if "ستلايت" in map_type else "OSM"

        m = folium.Map(location=[24.7136, 46.6753], zoom_start=6, tiles=tiles, attr=attr)
        m.add_child(folium.LatLngPopup())
        
        output = st_folium(m, height=450, width="100%", key="main_map")
        
        if output.get("last_clicked"):
            st.session_state.lat = output["last_clicked"]["lat"]
            st.session_state.lng = output["last_clicked"]["lng"]
            st.success(f"📍 تم تحديد الإحداثيات: {st.session_state.lat:.5f}, {st.session_state.lng:.5f}")

    def run(self):
        st.markdown(get_custom_css(), unsafe_allow_html=True)
        
        if 'authenticated' not in st.session_state: st.session_state.authenticated = False
        
        if not st.session_state.authenticated:
            self.render_login()
        else:
            self.render_main()

    def render_login(self):
        with st.form("login"):
            u = st.text_input("المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول"):
                st.session_state.authenticated = True
                st.session_state.user_role = 'admin'
                st.rerun()

    def render_main(self):
        with st.sidebar:
            st.title("🏛️ نظام التأجير البلدي")
            choice = st.radio("القائمة", ["📊 لوحة التحكم", "📈 التقييم الإيجاري", "👥 لجنة الاستثمار", "📑 التقارير", "⚙️ الإعدادات"])
        
        if choice == "📊 لوحة التحكم": render_dashboard('admin')
        elif choice == "📈 التقييم الإيجاري": self.render_valuation_page()
        elif choice == "👥 لجنة الاستثمار": self.committee_manager.render_committee_module()
        elif choice == "📑 التقارير": render_report_module('admin')
        elif choice == "⚙️ الإعدادات": render_admin_panel('admin')

    def render_valuation_page(self):
        st.header("📍 تقييم القيمة الإيجارية للموقع")
        
        # 1. الخريطة المزدوجة
        self.render_dual_map()
        
        # 2. اختيار نوع التأجير (معرب)
        st.divider()
        st.subheader("📋 تفاصيل التأجير")
        lease_options = self.lease_manager.get_all_types_arabic()
        selected_key = st.selectbox("نوع التأجير المطلوب", options=list(lease_options.keys()), format_func=lambda x: lease_options[x])
        
        # جلب المعامل من قاعدة البيانات (الإعدادات العامة)
        multiplier_key = self.lease_manager.lease_types[selected_key]['multiplier_key']
        multiplier = float(get_setting(multiplier_key, 1.0))
        
        st.info(f"المعامل المطبق لهذا النوع: {multiplier} (يمكن تعديله من الإعدادات العامة)")
        
        # 3. الحساب باستخدام المعادلات العلمية
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input("المساحة (م²)", value=500.0)
            base_p = st.number_input("السعر الاسترشادي للمتر", value=200.0)
        
        with col2:
            final_rent = area * base_p * multiplier
            st.metric("القيمة الإيجارية السنوية المقدرة", f"{final_rent:,.2f} ريال")
            
        # 4. إصدار قرار اللجنة
        if st.button("📝 إرسال للجنة الاستثمار"):
            self.committee_manager.render_decision_maker(area, base_p, multiplier)

if __name__ == "__main__":
    app = EnhancedApp()
    app.run()
