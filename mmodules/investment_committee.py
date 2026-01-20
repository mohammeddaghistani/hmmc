class InvestmentCommitteeSystem:
    """نظام إدارة لجنة الاستثمار حسب اللوائح"""
    
    def __init__(self):
        self.committee_requirements = {
            'members_count': 3,
            'ministry_members': 2,  # يمثلون الوزارة
            'finance_member': 1,    # يمثل وزارة المالية
            'min_rank': 12,         # مرتبة لا تقل عن الثانية عشرة
            'alternates': {
                'ministry': 1,      # عضو احتياطي للوزارة
                'finance': 1        # عضو احتياطي للمالية
            }
        }
    
    def form_committee(self, municipality_name, site_data):
        """تكوين لجنة استثمار حسب المادة 17"""
        
        committee = {
            'id': f"COMM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'formation_date': datetime.now().isoformat(),
            'municipality': municipality_name,
            'site_reference': site_data.get('site_code', 'غير محدد'),
            'members': [],
            'alternates': [],
            'status': 'active',
            'decisions': []
        }
        
        # إضافة الأعضاء (في الواقع ستكون من قاعدة بيانات)
        committee['members'] = [
            {
                'id': 'MEM001',
                'name': 'رئيس البلدية أو ممثله',
                'role': 'رئيس اللجنة',
                'organization': municipality_name,
                'min_rank': 12,
                'qualification': 'حامل شهادة جامعية'
            },
            {
                'id': 'MEM002',
                'name': 'ممثل وزارة الشؤون البلدية',
                'role': 'عضو',
                'organization': 'الوزارة',
                'qualification': 'حامل شهادة جامعية'
            },
            {
                'id': 'MEM003',
                'name': 'ممثل وزارة المالية',
                'role': 'عضو',
                'organization': 'وزارة المالية',
                'qualification': 'حامل شهادة جامعية'
            }
        ]
        
        # الأعضاء الاحتياطيون
        committee['alternates'] = [
            {
                'id': 'ALT001',
                'name': 'احتياطي الوزارة',
                'role': 'عضو احتياطي',
                'organization': 'الوزارة'
            },
            {
                'id': 'ALT002',
                'name': 'احتياطي المالية',
                'role': 'عضو احتياطي',
                'organization': 'وزارة المالية'
            }
        ]
        
        return committee
    
    def determine_rental_value(self, committee_id, site_data, lease_type, market_data=None):
        """تحديد القيمة الإيجارية بقرار لجنة"""
        
        # تحليل البيانات
        analysis = self._analyze_site_for_valuation(site_data, lease_type, market_data)
        
        # اتخاذ القرار
        decision = {
            'id': f"DEC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'committee_id': committee_id,
            'decision_date': datetime.now().isoformat(),
            'lease_type': lease_type,
            'site_data': site_data,
            'market_analysis': analysis,
            'proposed_rent': None,
            'guide_price': None,
            'final_decision': None,
            'votes': {'yes': 0, 'no': 0, 'abstain': 0},
            'members_voted': [],
            'requires_minister_approval': False
        }
        
        # حساب القيمة المقترحة
        if lease_type == 'TEMPORARY_ACTIVITY':
            decision['proposed_rent'] = self._calculate_temporary_rent(site_data, analysis)
        elif lease_type == 'LONG_TERM_INVESTMENT':
            decision['proposed_rent'] = self._calculate_long_term_rent(site_data, analysis)
        else:
            decision['proposed_rent'] = self._calculate_general_rent(site_data, analysis)
        
        # تحديد السعر الاسترشادي
        decision['guide_price'] = decision['proposed_rent'] * 1.33  # +33% تقريباً
        
        # التحقق من الحاجة لموافقة الوزير
        if lease_type == 'DIRECT_LEASE':
            min_price = decision['guide_price'] * 0.75
            if decision['proposed_rent'] < min_price:
                decision['requires_minister_approval'] = True
        
        return decision
    
    def _analyze_site_for_valuation(self, site_data, lease_type, market_data):
        """تحليل الموقع لتحديد القيمة"""
        
        analysis = {
            'site_score': 0,
            'market_comparables': [],
            'adjustment_factors': {},
            'risk_assessment': {},
            'recommendations': []
        }
        
        # حساب نقاط الموقع (1-100)
        score = 50  # نقطة أساسية
        
        # إضافة نقاط حسب الخدمات
        services = site_data.get('services', {})
        score += sum(services.values()) * 5
        
        # إضافة نقاط حسب الموقع
        city_tier = self._get_city_tier(site_data.get('city', ''))
        score += city_tier * 10
        
        # إضافة نقاط حسب الاستخدام
        zoning_value = self._get_zoning_value(site_data.get('zoning', ''))
        score += zoning_value
        
        analysis['site_score'] = min(100, max(20, score))
        
        # عوامل التعديل
        analysis['adjustment_factors'] = {
            'location': {'weight': 0.3, 'value': city_tier/10},
            'services': {'weight': 0.25, 'value': len([s for s in services.values() if s])/8},
            'frontage': {'weight': 0.15, 'value': min(site_data.get('frontage', 0)/50, 1)},
            'area': {'weight': 0.1, 'value': min(site_data.get('area', 0)/5000, 1)},
            'zoning': {'weight': 0.2, 'value': zoning_value/20}
        }
        
        return analysis
    
    def _calculate_temporary_rent(self, site_data, analysis):
        """حساب إيجار الأنشطة المؤقتة"""
        
        base_rate = 100  # ريال/م²/شهر (قيمة افتراضية)
        
        # تطبيق عوامل التعديل
        adjustment = sum(factor['weight'] * factor['value'] 
                        for factor in analysis['adjustment_factors'].values())
        
        adjusted_rate = base_rate * (0.5 + adjustment)
        
        # حساب الإيجار الشهري
        monthly_rent = adjusted_rate * site_data.get('area', 0)
        
        # للأنشطة المؤقتة، عادة ما تكون القيمة إجمالية وليست للمتر
        return {
            'monthly_per_m2': adjusted_rate,
            'monthly_total': monthly_rent,
            'for_6_months': monthly_rent * 6,
            'calculation_method': 'تعديل على أساس قيم السوق والعوامل المؤثرة'
        }
    
    def _get_city_tier(self, city):
        """تصنيف المدينة"""
        
        tiers = {
            'الرياض': 3, 'جدة': 3, 'الدمام': 3,
            'مكة': 2, 'المدينة': 2, 'الشرقية': 2,
            'أبها': 1, 'تبوك': 1, 'حائل': 1
        }
        
        return tiers.get(city, 1)
    
    def _get_zoning_value(self, zoning):
        """قيمة التصنيف البلدي"""
        
        values = {
            'تجاري': 20, 'سكني': 15, 'صناعي': 12,
            'سياحي': 18, 'زراعي': 8, 'تعليمي': 10,
            'صحي': 12, 'مختلط': 16
        }
        
        return values.get(zoning, 10)
