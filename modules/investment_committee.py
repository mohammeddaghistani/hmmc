import streamlit as st
from datetime import datetime
import uuid

class InvestmentCommitteeSystem:
    """نظام إدارة لجان الاستثمار حسب اللوائح"""
    
    def __init__(self):
        if 'committee_decisions' not in st.session_state:
            st.session_state.committee_decisions = []

    def render_committee_module(self):
        st.subheader("👥 تكوين لجنة الاستثمار (المادة 17)")
        with st.form("comm_form"):
            col1, col2 = st.columns(2)
            with col1:
                mun = st.text_input("الأمانة / البلدية", value="أمانة منطقة الرياض")
                chairman = st.text_input("رئيس اللجنة", value="وكيل الأمانة")
            with col2:
                members = st.number_input("عدد الأعضاء (يمثلون الوزارة والمالية)", min_value=3, value=3)
                date = st.date_input("تاريخ التكوين")
            
            if st.form_submit_button("✅ اعتماد تشكيل اللجنة"):
                st.session_state.committee_active = {'id': f"COM-{uuid.uuid4().hex[:4].upper()}", 'mun': mun, 'chairman': chairman}
                st.success(f"تم اعتماد اللجنة برقم: {st.session_state.committee_active['id']}")

    def render_decision_maker(self, area, base_price, multiplier):
        """إصدار قرار تحديد القيمة الإيجارية"""
        if 'committee_active' not in st.session_state:
            st.warning("⚠️ يجب تكوين اللجنة أولاً لإصدار القرار")
            return
            
        guide_price = area * base_price * multiplier
        st.subheader("📝 قرار تحديد القيمة الإيجارية")
        st.metric("القيمة الاسترشادية المقترحة", f"{guide_price:,.2f} ريال سنوياً")
        if st.button("💾 حفظ القرار"):
            st.session_state.committee_decisions.append({'date': datetime.now(), 'value': guide_price})
            st.success("تم حفظ القرار بنجاح")
