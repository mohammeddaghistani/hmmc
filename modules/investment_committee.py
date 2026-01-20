import streamlit as st
from datetime import datetime
import uuid

class InvestmentCommitteeSystem:
    """نظام إدارة لجنة الاستثمار حسب اللوائح"""
    def __init__(self):
        if 'committee_decisions' not in st.session_state:
            st.session_state.committee_decisions = []

    def render_committee_module(self):
        st.subheader("👥 تكوين لجنة الاستثمار (المادة 17)")
        with st.form("comm_formation"):
            col1, col2 = st.columns(2)
            with col1:
                mun = st.text_input("الأمانة / البلدية", value="أمانة منطقة الرياض")
                chairman = st.text_input("رئيس اللجنة", value="وكيل الأمانة")
            with col2:
                members = st.number_input("عدد الأعضاء (يمثلون الوزارة والمالية)", min_value=3, value=3)
                date = st.date_input("تاريخ التكوين")
            
            if st.form_submit_button("✅ اعتماد اللجنة"):
                st.session_state.committee_active = {'id': f"COM-{uuid.uuid4().hex[:4].upper()}", 'mun': mun}
                st.success(f"تم اعتماد اللجنة برقم: {st.session_state.committee_active['id']}")

    def determine_rental_value(self, site_data, lease_type):
        # معادلات تحديد القيمة بناءً على نوع التأجير
        area = site_data.get('area', 1.0)
        multipliers = {'TEMPORARY_ACTIVITY': 0.85, 'LONG_TERM_INVESTMENT': 1.6, 'DIRECT_LEASE': 1.25}
        multiplier = multipliers.get(lease_type, 1.0)
        return area * 100 * multiplier
