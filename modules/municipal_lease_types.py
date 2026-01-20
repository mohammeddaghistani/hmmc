import streamlit as st

class MunicipalLeaseTypes:
    """فئة متخصصة في أنواع التأجير البلدية حسب اللوائح"""
    
    def __init__(self):
        self.lease_types = {
            'TEMPORARY_ACTIVITY': {
                'code': 'TEMP',
                'name': 'تأجير مؤقت للأنشطة والفعاليات',
                'max_duration_months': 6,
                'max_extensions': 3,
                'total_max_months': 12,
                'source': 'المادة 3 من الضوابط، المادة 10/3 من اللائحة',
                'committee_required': True
            },
            'LONG_TERM_INVESTMENT': {
                'code': 'LONG',
                'name': 'تأجير طويل الأجل (استثماري)',
                'subtypes': {
                    'MAJOR_PROJECTS': {
                        'name': 'مشروعات استثمارية كبرى',
                        'max_years': 50,
                        'conditions': 'تنمية المدن'
                    },
                    'WITH_CONSTRUCTION': {
                        'name': 'أراضي مع إنشاءات',
                        'max_years': 25,
                        'conditions': 'إقامة مبانٍ ثابتة'
                    }
                },
                'source': 'المادة 21 من اللائحة',
                'committee_required': True
            },
            'DIRECT_LEASE': {
                'code': 'DIRECT',
                'name': 'تأجير مباشر',
                'source': 'المادة 27 من اللائحة',
                'committee_required': True
            }
        }
    
    def get_lease_type_details(self, lease_type, subtype=None):
        if lease_type not in self.lease_types:
            return None
        details = self.lease_types[lease_type].copy()
        if subtype and 'subtypes' in details:
            if subtype in details['subtypes']:
                details.update(details['subtypes'][subtype])
        return details

    def render_lease_type_selection(self):
        st.markdown("### 📋 اختيار نوع التأجير")
        selected_type = st.selectbox("نوع التأجير الرئيسي", list(self.lease_types.keys()))
        return selected_type, None
