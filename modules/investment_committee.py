import streamlit as st
from datetime import datetime
import uuid

class InvestmentCommitteeSystem:
    """نظام إدارة لجان الاستثمار البلدية وإصدار القرارات"""
    
    def __init__(self):
        if 'committee_decisions' not in st.session_state:
            st.session_state.committee_decisions = []

    def render_committee_module(self):
        """واجهة تكوين اللجنة وإدارة الأعضاء"""
        st.subheader("👥 تكوين لجنة الاستثمار (المادة 17)")
        
        with st.form("committee_form"):
            col1, col2 = st.columns(2)
            with col1:
                municipality = st.text_input("الأمانة / البلدية المعنية")
                chairman = st.text_input("رئيس اللجنة (مرتبة 12 فأعلى)")
            with col2:
                members_count = st.number_input("عدد الأعضاء يمثلون الوزارة والمالية", min_value=3, value=3)
                formation_date = st.date_input("تاريخ قرار التشكيل")
            
            if st.form_submit_button("✅ اعتماد تشكيل اللجنة"):
                st.session_state.committee_active = {
                    'id': f"COMM-{uuid.uuid4().hex[:4].upper()}",
                    'municipality': municipality,
                    'chairman': chairman,
                    'status': 'نشطة'
                }
                st.success(f"تم اعتماد تشكيل اللجنة برقم: {st.session_state.committee_active['id']}")

    def form_committee(self, municipality, site_data):
        """دالة برمجية لتشكيل لجنة لموقع محدد"""
        committee_id = f"COM-{datetime.now().strftime('%Y')}-{uuid.uuid4().hex[:4].upper()}"
        return {
            'id': committee_id,
            'municipality': municipality,
            'formation_date': datetime.now().strftime("%Y-%m-%d"),
            'site_code': site_data.get('site_code', 'غير محدد'),
            'members': [{'name': 'رئيس اللجنة', 'role': 'رئيس'}, {'name': 'أمين اللجنة', 'role': 'مقرر'}]
        }
