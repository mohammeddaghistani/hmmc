class MunicipalLeaseTypes:
    """فئة متخصصة في أنواع التأجير البلدية حسب اللوائح"""
    
    def __init__(self):
        self.lease_types = {
            'TEMPORARY_ACTIVITY': {
                'code': 'TEMP',
                'name': 'تأجير مؤقت للأنشطة والفعاليات',
                'max_duration_months': 6,
                'max_extensions': 3,
                'total_max_months': 12,  # 6 + 6 تمديد
                'source': 'المادة 3 من الضوابط، المادة 10/3 من اللائحة',
                'activities': [
                    'الفعاليات والمهرجانات',
                    'المؤتمرات والمناسبات',
                    'الفعاليات الترويجية',
                    'الأنشطة الموسمية'
                ],
                'committee_required': True,  # تحتاج لجنة استثمار
                'contract_template': 'TEMPORARY_LEASE_TEMPLATE'
            },
            'LONG_TERM_INVESTMENT': {
                'code': 'LONG',
                'name': 'تأجير طويل الأجل (استثماري)',
                'subtypes': {
                    'ADVERTISING': {
                        'name': 'لوحات إعلانية وآلات بيع ذاتي',
                        'max_years': 10,
                        'conditions': 'بدون مبانٍ ثابتة'
                    },
                    'LAND_NO_BUILDING': {
                        'name': 'أراضي بدون مبانٍ ثابتة',
                        'max_years': 10,
                        'conditions': 'لا يتضمن إقامة مبانٍ'
                    },
                    'BUILDING_NO_ADDITION': {
                        'name': 'مبانٍ بدون إضافات',
                        'max_years': 10,
                        'conditions': 'بدون إضافة مبانٍ أو ترميم شامل'
                    },
                    'PUBLIC_GARDENS': {
                        'name': 'حدائق عامة منفذة',
                        'max_years': 10,
                        'conditions': 'حدائق مكتملة التنفيذ'
                    },
                    'ATM': {
                        'name': 'أجهزة الصرف الآلي',
                        'max_years': 15,
                        'conditions': 'مواقع مخصصة للصرف الآلي'
                    },
                    'WITH_CONSTRUCTION': {
                        'name': 'أراضي/مبانٍ مع إنشاءات',
                        'max_years': 25,
                        'conditions': 'يتضمن إقامة/إضافة مبانٍ ثابتة أو ترميم شامل'
                    },
                    'MAJOR_PROJECTS': {
                        'name': 'مشروعات استثمارية كبرى',
                        'max_years': 50,
                        'conditions': 'تساهم في تنمية المدن ولا تتحقق جدواها في أقل من 25 سنة'
                    }
                },
                'source': 'المادة 21 من اللائحة',
                'committee_required': True,
                'contract_template': 'LONG_TERM_INVESTMENT_TEMPLATE'
            },
            'DIRECT_LEASE': {
                'code': 'DIRECT',
                'name': 'تأجير مباشر',
                'conditions': [
                    'بعد إعلان واحد للحدائق العامة وعدم وجود مستثمرين',
                    'بعد إعلانين لأي عقار آخر وعدم وجود مستثمرين'
                ],
                'time_limit': 'سنة واحدة من تاريخ تسلم العروض',
                'source': 'المادة 27 من اللائحة',
                'committee_required': True,
                'minimum_price': 'لا يقل عن 75% من السعر الاسترشادي (المادة 46 من التعليمات)',
                'contract_template': 'DIRECT_LEASE_TEMPLATE'
            },
            'EXEMPTED_FROM_COMPETITION': {
                'code': 'EXEMPT',
                'name': 'عقارات مستثناة من المنافسة',
                'categories': [
                    'عقارات مع جهات حكومية',
                    'عقارات مع شركات امتياز عام',
                    'عقارات مع شركات تساهم فيها الدولة',
                    'عقارات لمنفذي المشروعات (≤3 سنوات)',
                    'عقارات لمعالجة أوضاع قائمة',
                    'حدائق في مخططات خاصة (≤سنتين)',
                    'أنشطة مؤقتة',
                    'مشروعات مبتكرة/رائدة/مميزة',
                    'عقارات للمنافسة العلنية المفتوحة'
                ],
                'source': 'المادة 10 من اللائحة، المادة 34 من التعليمات',
                'committee_required': True,
                'contract_template': 'EXEMPTED_LEASE_TEMPLATE'
            }
        }
    
    def get_lease_type_details(self, lease_type, subtype=None):
        """الحصول على تفاصيل نوع التأجير"""
        
        if lease_type not in self.lease_types:
            return None
        
        details = self.lease_types[lease_type].copy()
        
        if subtype and 'subtypes' in details:
            if subtype in details['subtypes']:
                details.update(details['subtypes'][subtype])
                del details['subtypes']
        
        return details
    
    def validate_lease_duration(self, lease_type, duration_months, extensions_count=0):
        """التحقق من مدة التأجير حسب النوع"""
        
        details = self.get_lease_type_details(lease_type)
        
        if not details:
            return False, "نوع التأجير غير معروف"
        
        if lease_type == 'TEMPORARY_ACTIVITY':
            # التحقق من المدة الأصلية
            if duration_months > details['max_duration_months']:
                return False, f"مدة التأجير المؤقت لا تزيد عن {details['max_duration_months']} أشهر"
            
            # التحقق من عدد التمديدات
            if extensions_count > details['max_extensions']:
                return False, f"لا تتجاوز طلبات التمديد {details['max_extensions']} طلبات"
            
            # التحقق من المدة الإجمالية
            total_months = duration_months + (extensions_count * details['max_duration_months'])
            if total_months > details['total_max_months']:
                return False, f"المدة الإجمالية لا تتجاوز {details['total_max_months']} أشهر"
        
        elif lease_type == 'LONG_TERM_INVESTMENT':
            duration_years = duration_months / 12
            max_years = details.get('max_years', 0)
            
            if duration_years > max_years:
                return False, f"المدة القصوى لهذا النوع هي {max_years} سنة"
        
        return True, "المدة مقبولة"
    
    def get_required_committee(self, lease_type):
        """التحقق مما إذا كان النوع يحتاج لجنة استثمار"""
        
        details = self.get_lease_type_details(lease_type)
        return details.get('committee_required', False) if details else False
    
    def generate_lease_code(self, lease_type, municipality_code, year, sequence):
        """توليد رمز فريد للتأجير"""
        
        if lease_type not in self.lease_types:
            return None
        
        type_code = self.lease_types[lease_type]['code']
        return f"ML-{municipality_code}-{type_code}-{year}-{sequence:04d}"
    
    def render_lease_type_selection(self):
        """عرض واجهة اختيار نوع التأجير"""
        
        import streamlit as st
        
        st.markdown("### 📋 اختيار نوع التأجير حسب اللوائح البلدية")
        
        # اختيار النوع الرئيسي
        lease_options = {
            'TEMPORARY_ACTIVITY': 'تأجير مؤقت للأنشطة والفعاليات (6 أشهر)',
            'LONG_TERM_INVESTMENT': 'تأجير طويل الأجل (استثماري)',
            'DIRECT_LEASE': 'تأجير مباشر',
            'EXEMPTED_FROM_COMPETITION': 'عقارات مستثناة من المنافسة'
        }
        
        selected_type = st.selectbox(
            "نوع التأجير",
            list(lease_options.keys()),
            format_func=lambda x: lease_options[x]
        )
        
        details = self.get_lease_type_details(selected_type)
        
        # عرض التفاصيل
        with st.expander("📄 تفاصيل النوع المختار", expanded=True):
            if details:
                st.write(f"**الاسم:** {details['name']}")
                st.write(f"**المصدر القانوني:** {details['source']}")
                
                if 'max_duration_months' in details:
                    st.write(f"**المدة القصوى:** {details['max_duration_months']} أشهر")
                
                if 'max_extensions' in details:
                    st.write(f"**أقصى عدد للتمديد:** {details['max_extensions']}")
                
                if 'activities' in details:
                    st.write("**الأنشطة المشمولة:**")
                    for activity in details['activities']:
                        st.write(f"- {activity}")
                
                if 'conditions' in details:
                    if isinstance(details['conditions'], list):
                        st.write("**الشروط:**")
                        for condition in details['conditions']:
                            st.write(f"- {condition}")
                    else:
                        st.write(f"**الشروط:** {details['conditions']}")
                
                st.write(f"**يتطلب لجنة استثمار:** {'نعم' if details['committee_required'] else 'لا'}")
        
        # إذا كان النوع طويل الأجل، اختيار النوع الفرعي
        if selected_type == 'LONG_TERM_INVESTMENT':
            subtype_options = list(details['subtypes'].keys())
            subtype_names = {k: v['name'] for k, v in details['subtypes'].items()}
            
            selected_subtype = st.selectbox(
                "النوع الفرعي للتأجير طويل الأجل",
                subtype_options,
                format_func=lambda x: subtype_names[x]
            )
            
            subtype_details = details['subtypes'][selected_subtype]
            
            with st.expander("📊 تفاصيل النوع الفرعي", expanded=True):
                st.write(f"**الاسم:** {subtype_details['name']}")
                st.write(f"**المدة القصوى:** {subtype_details['max_years']} سنة")
                st.write(f"**الشروط:** {subtype_details['conditions']}")
        
        return selected_type, selected_subtype if selected_type == 'LONG_TERM_INVESTMENT' else None
