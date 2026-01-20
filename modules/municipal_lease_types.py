import streamlit as st

class MunicipalLeaseTypes:
    """إدارة أنواع التأجير البلدية المعربة بالكامل"""
    
    def __init__(self):
        self.lease_types = {
            'TEMPORARY_ACTIVITY': {
                'name': 'تأجير مؤقت للأنشطة والفعاليات',
                'multiplier_key': 'mult_temp',
                'duration': '6 أشهر قابلة للتمديد'
            },
            'LONG_TERM_INVESTMENT': {
                'name': 'تأجير استثماري طويل الأجل',
                'multiplier_key': 'mult_long',
                'duration': 'حتى 50 سنة'
            },
            'DIRECT_LEASE': {
                'name': 'تأجير مباشر (المادة 27)',
                'multiplier_key': 'mult_direct',
                'duration': 'حسب شروط الحالة'
            }
        }

    def render_lease_type_selection(self):
        st.subheader("🏛️ اختيار نوع التأجير البلدي")
        options = {k: v['name'] for k, v in self.lease_types.items()}
        selected_key = st.selectbox("نوع التأجير المطلوب", options=list(options.keys()), format_func=lambda x: options[x])
        st.info(f"الوصف: {self.lease_types[selected_key]['duration']}")
        return selected_key
