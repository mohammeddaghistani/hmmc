import streamlit as st
from datetime import datetime
import uuid

class InvestmentCommitteeSystem:
    """نظام تكوين لجان الاستثمار وإصدار القرارات"""
    
    def render_committee_module(self):
        st.subheader("👥 تكوين لجنة الاستثمار (المادة 17)")
        
        with st.form("committee_formation"):
            col1, col2 = st.columns(2)
            with col1:
                municipality = st.text_input("الأمانة / البلدية", value="أمانة منطقة الرياض")
                members_count = st.number_input("عدد الأعضاء", min_value=3, value=3)
            with col2:
                chairman = st.text_input("رئيس اللجنة", value="وكيل الأمانة للاستثمار")
                formation_date = st.date_input("تاريخ التكوين")
            
            st.info("يتكون تشكيل اللجنة من ممثلي الوزارة وممثل وزارة المالية حسب النظام.")
            
            if st.form_submit_button("✅ اعتماد تشكيل اللجنة"):
                st.session_state.committee_active = {
                    'id': f"COMM-{datetime.now().year}-{uuid.uuid4().hex[:4].upper()}",
                    'municipality': municipality,
                    'chairman': chairman,
                    'status': 'نشطة'
                }
                st.success(f"تم اعتماد اللجنة برقم: {st.session_state.committee_active['id']}")

    def render_decision_maker(self, site_area, base_price, lease_multiplier):
        """إصدار قرار تحديد القيمة الإيجارية"""
        if 'committee_active' not in st.session_state:
            st.warning("⚠️ يجب تكوين اللجنة أولاً لإصدار القرار")
            return
            
        st.subheader("📝 قرار تحديد القيمة الإيجارية")
        guide_price = site_area * base_price * lease_multiplier
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("القيمة الاسترشادية (سنوياً)", f"{guide_price:,.2f} ريال")
        with col2:
            st.write(f"رقم اللجنة: {st.session_state.committee_active['id']}")
            st.write(f"رئيس اللجنة: {st.session_state.committee_active['chairman']}")
