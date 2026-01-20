class MunicipalLeaseTypes:
    """أنواع التأجير البلدية المعربة بالكامل حسب اللوائح"""
    def __init__(self):
        self.lease_types = {
            'TEMPORARY_ACTIVITY': {
                'name': 'تأجير مؤقت (فعاليات/أنشطة)',
                'multiplier_key': 'mult_temporary',
                'description': 'عقود قصيرة الأجل تصل إلى 6 أشهر'
            },
            'LONG_TERM_INVESTMENT': {
                'name': 'تأجير استثماري طويل الأجل',
                'multiplier_key': 'mult_long_term',
                'description': 'عقود استثمارية تصل إلى 50 سنة'
            },
            'DIRECT_LEASE': {
                'name': 'تأجير مباشر',
                'multiplier_key': 'mult_direct',
                'description': 'تأجير بدون منافسة حسب حالات المادة 27'
            }
        }

    def get_all_types_arabic(self):
        return {k: v['name'] for k, v in self.lease_types.items()}
