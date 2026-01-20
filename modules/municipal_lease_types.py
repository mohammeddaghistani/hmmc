class MunicipalLeaseTypes:
    """تعريب أنواع التأجير البلدية بالكامل"""
    def __init__(self):
        self.lease_types = {
            'TEMPORARY_ACTIVITY': {'name': 'تأجير مؤقت للأنشطة والفعاليات', 'multiplier': 'mult_temp'},
            'LONG_TERM_INVESTMENT': {'name': 'تأجير طويل الأجل (استثماري)', 'multiplier': 'mult_long'},
            'DIRECT_LEASE': {'name': 'تأجير مباشر (المادة 27)', 'multiplier': 'mult_direct'}
        }
    def get_lease_options(self):
        return {k: v['name'] for k, v in self.lease_types.items()}
