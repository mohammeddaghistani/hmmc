import streamlit as st
from datetime import datetime
import uuid

class InvestmentCommitteeSystem:
    """نظام إدارة لجان الاستثمار البلدية وتحديد القيم الإيجارية"""
    
    def __init__(self):
        # قاعدة بيانات وهمية للقرارات في حال عدم وجود قاعدة بيانات حقيقية
        if 'committee_decisions' not in st.session_state:
            st.session_state.committee_decisions = []

    def form_committee(self, municipality, site_data):
        """تشكيل لجنة استثمار جديدة لموقع محدد"""
        committee_id = f"COM-{datetime.now().strftime('%Y')}-{uuid.uuid4().hex[:4].upper()}"
        
        committee = {
            'id': committee_id,
            'municipality': municipality,
            'formation_date': datetime.now().strftime("%Y-%m-%d"),
            'site_code': site_data.get('site_code', 'N/A'),
            'members': [
                {'name': 'رئيس اللجنة', 'role': 'رئيس'},
                {'name': 'عضو استثماري', 'role': 'عضو'},
                {'name': 'أمين اللجنة', 'role': 'عضو مقرر'}
            ]
        }
        return committee

    def determine_rental_value(self, committee_id, site_data, lease_type):
        """تحديد القيمة الإيجارية بناءً على معطيات الموقع ونوع التأجير"""
        area = site_data.get('area', 1)
        # حساب سعر استرشادي وهمي (يمكنك تعديل المعادلة حسب لوائحكم)
        base_rate = 100 # سعر أساسي
        
        # تعديل السعر حسب نوع التأجير
        multipliers = {
            'TEMPORARY_ACTIVITY': 0.8,
            'LONG_TERM_INVESTMENT': 1.5,
            'DIRECT_LEASE': 1.2,
            'EXEMPTED_FROM_COMPETITION': 1.0
        }
        
        multiplier = multipliers.get(lease_type, 1.0)
        guide_price = area * base_rate * multiplier
        
        decision = {
            'id': f"DEC-{uuid.uuid4().hex[:6].upper()}",
            'committee_id': committee_id,
            'lease_type': lease_type,
            'decision_date': datetime.now().isoformat(),
            'guide_price': guide_price,
            'proposed_rent': {
                'monthly_total': guide_price / 12,
                'monthly_per_m2': (guide_price / 12) / area
            },
            'requires_minister_approval': True if guide_price > 1000000 else False
        }
        
        st.session_state.committee_decisions.append(decision)
        return decision

    def get_all_decisions(self):
        """جلب جميع القرارات المسجلة"""
        return st.session_state.committee_decisions
