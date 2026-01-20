class MunicipalLeaseTypes:
    """إدارة أنواع التأجير البلدية باللغة العربية"""
    def __init__(self):
        self.lease_types = {
            'TEMPORARY_ACTIVITY': {
                'name': 'تأجير مؤقت للأنشطة والفعاليات',
                'multiplier_key': 'mult_temporary',
                'max_period': '6 أشهر'
            },
            'LONG_TERM_INVESTMENT': {
                'name': 'تأجير طويل الأجل (استثماري)',
                'multiplier_key': 'mult_long_term',
                'max_period': '50 سنة'
            },
            'DIRECT_LEASE': {
                'name': 'تأجير مباشر (المادة 27)',
                'multiplier_key': 'mult_direct',
                'max_period': 'حسب الحالة'
            }
        }
    def get_lease_options(self):
        return {k: v['name'] for k, v in self.lease_types.items()}
