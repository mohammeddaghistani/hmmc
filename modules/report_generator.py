"""
مولد تقارير التقييم المتوافقة مع المعايير الدولية (IVS) والملحق 4
"""

from datetime import datetime
from fpdf import FPDF
import json
from jinja2 import Template
import base64
from io import BytesIO

class ProfessionalValuationReport:
    """فئة لتوليد تقارير التقييم المهنية"""
    
    def __init__(self, valuation_data, valuer_info, client_info):
        self.valuation_data = valuation_data
        self.valuer_info = valuer_info
        self.client_info = client_info
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        self.valuation_date = valuation_data.get('valuation_date', self.report_date)
        
        # ⬅️ تحديث: قائمة أغراض التقييم
        self.purposes = [
            "تحديد القيمة الإيجارية للموقع",
            "تحديد القيمة السوقية",
            "التمويل البنكي",
            "الشراكة",
            "التأمين",
            "الضرائب",
            "التخطيط المالي",
            "التسعير للإيجار",
            "تحديد رسوم التملك",
            "التثمين للاستحواذ",
            "التقييم للغرامات"
        ]
    
    def generate_full_report(self):
        """توليد التقرير الكامل حسب هيكل الملحق 4"""
        
        report = {
            # === المجموعة الأولى: المعلومات الأساسية ===
            'basic_information': self._generate_basic_information(),
            
            # === المجموعة الثانية: الحقائق والفحص ===
            'facts_examination': self._generate_facts_examination(),
            
            # === المجموعة الثالثة: التحليل والقيمة ===
            'analysis_valuation': self._generate_analysis_valuation(),
            
            # === المجموعة الرابعة: إخلاء المسؤولية والمعايير ===
            'disclaimers_standards': self._generate_disclaimers_standards()
        }
        
        return report
    
    def _generate_basic_information(self):
        """المجموعة الأولى: المعلومات الأساسية"""
        
        # ⬅️ تحديث: إضافة خيار "تحديد القيمة الإيجارية للموقع"
        purpose = self.valuation_data.get('purpose', 'تحديد القيمة الإيجارية للموقع')
        if purpose not in self.purposes:
            purpose = self.purposes[0]
        
        return {
            'report_title': f"تقرير تقييم عقاري - {self.valuation_data.get('property_address', '')}",
            'valuation_number': f"VAL-{datetime.now().strftime('%Y%m%d')}-{self.valuation_data.get('id', '001')}",
            'valuation_date': self.valuation_date,
            'effective_date': self.valuation_data.get('effective_date', self.valuation_date),
            'purpose': purpose,  # ⬅️ تحديث
            'purpose_type': self._get_purpose_type(purpose),  # ⬅️ جديد
            'intended_users': self.valuation_data.get('intended_users', ['العميل', 'البنك التمويلي']),
            'available_purposes': self.purposes,  # ⬅️ جديد
            
            'valuer_information': {
                'name': self.valuer_info.get('name', 'المقيم المعتمد'),
                'qualifications': self.valuer_info.get('qualifications', ['مقيم عقاري معتمد', 'عضوية الهيئة السعودية للمقيمين']),
                'company': self.valuer_info.get('company', 'شركة التقييم العقاري'),
                'license_number': self.valuer_info.get('license_number', 'VAL-2024-001'),
                'independence_statement': "أؤكد استقلاليتي وعدم وجود أي تضارب مصالح في هذا التقييم."
            },
            
            'client_information': {
                'name': self.client_info.get('name', 'العميل'),
                'type': self.client_info.get('type', 'شركة'),
                'contact': self.client_info.get('contact', 'معلومات الاتصال')
            }
        }
    
    def _get_purpose_type(self, purpose):
        """تصنيف الغرض حسب النوع"""
        rental_purposes = [
            "تحديد القيمة الإيجارية للموقع",
            "التسعير للإيجار"
        ]
        
        valuation_purposes = [
            "تحديد القيمة السوقية",
            "التثمين للاستحواذ"
        ]
        
        financial_purposes = [
            "التمويل البنكي",
            "التخطيط المالي"
        ]
        
        legal_purposes = [
            "الضرائب",
            "التقييم للغرامات",
            "تحديد رسوم التملك"
        ]
        
        if purpose in rental_purposes:
            return "تقييم إيجاري"
        elif purpose in valuation_purposes:
            return "تقييم سوقي"
        elif purpose in financial_purposes:
            return "تقييم مالي"
        elif purpose in legal_purposes:
            return "تقييم قانوني"
        else:
            return "تقييم عام"
    
    def _generate_facts_examination(self):
        """المجموعة الثانية: الحقائق والفحص"""
        
        property_data = self.valuation_data.get('property_data', {})
        
        # ⬅️ تحديث: إضافة معلومات الإيجار إذا كان الغرض إيجاري
        purpose = self.valuation_data.get('purpose', '')
        rental_info = {}
        
        if purpose == "تحديد القيمة الإيجارية للموقع":
            rental_info = {
                'current_rent': property_data.get('current_rent', 'غير محدد'),
                'lease_term': property_data.get('lease_term', 'غير محدد'),
                'rental_history': property_data.get('rental_history', 'لا توجد سجلات سابقة')
            }
        
        return {
            'property_description': {
                'address': property_data.get('address', 'غير محدد'),
                'location_coordinates': {
                    'latitude': property_data.get('latitude'),
                    'longitude': property_data.get('longitude')
                },
                'property_type': property_data.get('property_type', 'سكني'),
                'land_area': f"{property_data.get('land_area_m2', 0):,.0f} م²",
                'built_up_area': f"{property_data.get('built_up_area_m2', 0):,.0f} م²",
                'year_built': property_data.get('year_built', 'غير معروف'),
                'condition': property_data.get('condition', 'جيد'),
                'zoning': property_data.get('zoning', 'سكني'),
                'permitted_use': property_data.get('permitted_use', 'سكن عائلي')
            },
            
            'legal_information': {
                'title_deed': property_data.get('title_deed_number', 'غير متوفر'),
                'ownership': property_data.get('ownership_type', 'ملكية كاملة'),
                'encumbrances': property_data.get('encumbrances', 'لا توجد قيود مسجلة'),
                'lease_details': property_data.get('lease_details', 'لا توجد عقود إيجار حالية')
            },
            
            'rental_information': rental_info,  # ⬅️ جديد
            
            'inspection_details': {
                'inspection_date': property_data.get('inspection_date', self.valuation_date),
                'inspected_by': self.valuer_info.get('name', 'المقيم المعتمد'),
                'scope_of_inspection': "فحص خارجي وداخلي شامل للعقار",
                'limitations_of_inspection': "الفحص بصري ولم يشمل فحص الهيكل الإنشائي المخفي"
            },
            
            'market_analysis': {
                'market_conditions': self._analyze_market_conditions(property_data.get('property_type')),
                'supply_demand': "تحليل العرض والطلب في المنطقة",
                'recent_transactions': "ملخص للمعاملات الحديثة المشابهة"
            }
        }
    
    def _generate_analysis_valuation(self):
        """المجموعة الثالثة: التحليل والقيمة (تختلف حسب الطريقة)"""
        
        method = self.valuation_data.get('valuation_method', 'sales_comparison')
        results = self.valuation_data.get('valuation_results', {})
        purpose = self.valuation_data.get('purpose', '')
        
        # ⬅️ تحديث: تحديد التركيز حسب الغرض
        if purpose == "تحديد القيمة الإيجارية للموقع":
            focus = "تحليل الإيجار والجدوى الإيجارية"
            value_label = "القيمة الإيجارية المقترحة"
        else:
            focus = "تحليل القيمة السوقية"
            value_label = "القيمة السوقية المقدرة"
        
        analysis = {
            'methodology': {
                'selected_method': self._get_method_name(method),
                'justification': self._get_method_justification(method, purpose),
                'compliance': "متوافق مع المعيار الدولي للتقييم (IVS) 104 ومع دليل الهيئة",
                'focus': focus  # ⬅️ جديد
            },
            
            'valuation_parameters': self._get_valuation_parameters(method, purpose),
            
            'detailed_calculations': self._format_calculations(method, results, purpose),
            
            'sensitivity_analysis': self._format_sensitivity_analysis(results),
            
            'final_valuation': {
                'market_value': f"{results.get('final_value', 0):,.0f} ريال سعودي",
                'value_per_m2': f"{results.get('value_per_m2', 0):,.0f} ريال/م²",
                'valuation_basis': results.get('valuation_basis', 'قيمة السوق العادلة'),
                'value_label': value_label,  # ⬅️ جديد
                'currency': "ريال سعودي (SAR)",
                'value_type': self._get_value_type(purpose),  # ⬅️ جديد
                'special_assumptions': self.valuation_data.get('special_assumptions', [])
            }
        }
        
        return analysis
    
    def _get_method_justification(self, method, purpose):
        """توفير تبرير لاختيار الطريقة حسب الغرض"""
        
        if purpose == "تحديد القيمة الإيجارية للموقع":
            justifications = {
                'sales_comparison': 'توفر بيانات إيجارات حديثة لمواقع مشابهة في المنطقة',
                'residual': 'الموقع مخصص للتطوير ولا توجد إيجارات مشابهة للمقارنة',
                'dcf': 'الموقع يدر دخلاً إيجارياً ويمكن التنبؤ بتدفقاته النقدية',
                'profits': 'قيمة الإيجار تعتمد على النشاط التجاري في الموقع'
            }
        else:
            justifications = {
                'sales_comparison': 'توفر بيانات كافية عن معاملات مشابهة حديثة',
                'residual': 'العقار مخصص للتطوير ولا توجد معاملات مشابهة',
                'dcf': 'العقار يدر دخلاً ويمكن التنبؤ بتدفقاته النقدية',
                'profits': 'قيمة العقار تعتمد على النشاط التجاري الذي يستضيفه'
            }
        
        return justifications.get(method, 'الطريقة الأنسب بناءً على توفر البيانات وطبيعة العقار')
    
    def _get_valuation_parameters(self, method, purpose):
        """الحصول على معاملات التقييم حسب الطريقة والغرض"""
        
        parameters = {
            'sales_comparison': {
                'comparables_count': self.valuation_data.get('comparables_count', 0),
                'adjustment_factors': ['الموقع', 'المساحة', 'العمر', 'الحالة', 'المواصفات'],
                'weight_matrix': self.valuation_data.get('weight_matrix', {})
            },
            'residual': {
                'yield_rate': f"{self.valuation_data.get('yield_rate', 0.08)*100:.1f}%",
                'construction_cost': self.valuation_data.get('construction_cost_per_m2', 0),
                'developer_profit': f"{self.valuation_data.get('developer_profit_percent', 0.20)*100:.0f}%"
            },
            'dcf': {
                'discount_rate': f"{self.valuation_data.get('discount_rate', 0.09)*100:.1f}%",
                'terminal_growth': f"{self.valuation_data.get('terminal_growth_rate', 0.02)*100:.1f}%",
                'forecast_period': f"{self.valuation_data.get('forecast_period', 10)} سنوات"
            },
            'profits': {
                'ebitda_multiple': self.valuation_data.get('ebitda_multiple', 8),
                'rent_share': f"{self.valuation_data.get('rent_share_percent', 0.50)*100:.0f}%",
                'operator_remuneration': f"{self.valuation_data.get('operator_remuneration_percent', 0.10)*100:.0f}%"
            }
        }
        
        base_params = parameters.get(method, {})
        
        # ⬅️ تحديث: إضافة معاملات خاصة بالتقيم الإيجاري
        if purpose == "تحديد القيمة الإيجارية للموقع":
            base_params['rental_factors'] = [
                'طول فترة الإيجار',
                'شروط تجديد العقد',
                'مسؤولية الصيانة',
                'زيادات الإيجار السنوية'
            ]
        
        return base_params
    
    def _get_value_type(self, purpose):
        """تحديد نوع القيمة حسب الغرض"""
        
        value_types = {
            "تحديد القيمة الإيجارية للموقع": "القيمة الإيجارية العادلة (Fair Rental Value)",
            "تحديد القيمة السوقية": "القيمة السوقية (Market Value)",
            "التمويل البنكي": "قيمة التمليك (Mortgage Lending Value)",
            "الشراكة": "قيمة الاستثمار (Investment Value)",
            "التأمين": "قيمة التعويض (Insurable Value)",
            "الضرائب": "قيمة الضريبة (Taxable Value)",
            "التخطيط المالي": "القيمة العادلة (Fair Value)"
        }
        
        return value_types.get(purpose, "القيمة السوقية (Market Value)")
    
    def _format_calculations(self, method, results, purpose):
        """تنسيق الحسابات التفصيلية حسب الطريقة والغرض"""
        
        if purpose == "تحديد القيمة الإيجارية للموقع":
            # ⬅️ تحديث: تنسيق خاص للحسابات الإيجارية
            return self._format_rental_calculations(method, results)
        else:
            # التنسيق العام
            if method == 'sales_comparison':
                return self._format_sales_comparison_calculations(results)
            elif method == 'residual':
                return self._format_residual_calculations(results)
            elif method == 'dcf':
                return self._format_dcf_calculations(results)
            elif method == 'profits':
                return self._format_profits_calculations(results)
        
        return {}
    
    def _format_rental_calculations(self, method, results):
        """تنسيق حسابات التقييم الإيجاري"""
        
        calculations = {
            'rental_analysis': {
                'focus': 'تحليل القيمة الإيجارية للموقع',
                'method_used': self._get_method_name(method),
                'rental_period': 'سنوي وشهري'
            },
            'rental_breakdown': {},
            'comparison_data': {}
        }
        
        # إضافة بيانات حسب الطريقة
        if method == 'sales_comparison':
            calculations['rental_breakdown'] = {
                'base_rent_per_m2': f"{results.get('base_rent_per_m2', 0):,.1f} ريال/م²",
                'adjusted_rent_per_m2': f"{results.get('adjusted_rent_per_m2', 0):,.1f} ريال/م²",
                'annual_rent': f"{results.get('annual_rent', 0):,.0f} ريال",
                'monthly_rent': f"{results.get('monthly_rent', 0):,.0f} ريال"
            }
            
            if results.get('adjustments'):
                calculations['adjustments_applied'] = results.get('adjustments', [])
        
        elif method == 'residual':
            calculations['rental_breakdown'] = {
                'land_value': f"{results.get('land_value', 0):,.0f} ريال",
                'yield_rate': f"{results.get('yield_rate', 0):.1f}%",
                'annual_rent': f"{results.get('annual_rent', 0):,.0f} ريال",
                'monthly_rent': f"{results.get('monthly_rent', 0):,.0f} ريال",
                'rent_per_m2': f"{results.get('rent_per_m2', 0):,.1f} ريال/م²"
            }
        
        elif method == 'dcf':
            calculations['rental_breakdown'] = {
                'total_present_value': f"{results.get('total_present_value', 0):,.0f} ريال",
                'annual_rent_equivalent': f"{results.get('annual_rent', 0):,.0f} ريال",
                'monthly_rent': f"{results.get('monthly_rent', 0):,.0f} ريال"
            }
        
        elif method == 'profits':
            calculations['rental_breakdown'] = {
                'market_rent': f"{results.get('market_rent', 0):,.0f} ريال",
                'monthly_rent': f"{results.get('monthly_rent', 0):,.0f} ريال",
                'rent_per_m2': f"{results.get('rent_per_m2', 0):,.1f} ريال/م²"
            }
        
        # إضافة توصيات إيجارية
        calculations['rental_recommendations'] = [
            "تحديد فترة عقد إيجار مناسبة (3-5 سنوات)",
            "تضمين بند زيادات سنوية (3-5%)",
            "تحديد مسؤوليات الصيانة والإصلاح",
            "وضع شروط تجديد العقد"
        ]
        
        return calculations
    
    # ... باقي الدوال كما هي مع تحديثات بسيطة ...
    
    def generate_rental_report(self):
        """توليد تقرير إيجاري متخصص"""
        
        purpose = self.valuation_data.get('purpose', '')
        
        if purpose != "تحديد القيمة الإيجارية للموقع":
            return self.generate_full_report()
        
        # ⬅️ جديد: تقرير إيجاري متخصص
        report = {
            'report_type': 'rental_valuation',
            'title': f"تقرير تحديد القيمة الإيجارية - {self.valuation_data.get('property_data', {}).get('address', '')}",
            'basic_info': self._generate_basic_information(),
            'rental_analysis': self._generate_rental_analysis(),
            'lease_terms_recommendations': self._generate_lease_recommendations(),
            'market_comparison': self._generate_rental_market_comparison()
        }
        
        return report
    
    def _generate_rental_analysis(self):
        """تحليل القيمة الإيجارية"""
        
        results = self.valuation_data.get('valuation_results', {})
        
        return {
            'rental_value': {
                'annual_rent': results.get('annual_rent', 0),
                'monthly_rent': results.get('monthly_rent', 0),
                'rent_per_m2': results.get('rent_per_m2', 0),
                'rent_per_square_foot': results.get('rent_per_square_foot', 0)
            },
            'financial_metrics': {
                'rental_yield': f"{results.get('rental_yield', 0)*100:.1f}%",
                'price_to_rent_ratio': results.get('price_to_rent_ratio', 0),
                'gross_rent_multiplier': results.get('gross_rent_multiplier', 0)
            },
            'market_positioning': {
                'position': self._determine_rental_position(results),
                'competitiveness': self._assess_rental_competitiveness(results),
                'growth_potential': self._assess_rental_growth(results)
            }
        }
    
    def _generate_lease_recommendations(self):
        """توصيات شروط عقد الإيجار"""
        
        return {
            'recommended_terms': [
                {'term': 'فترة العقد', 'recommendation': '3-5 سنوات', 'rationale': 'توازن بين استقرار المالك ومرونة المستأجر'},
                {'term': 'زيادة الإيجار', 'recommendation': '3-5% سنوياً', 'rationale': 'مواكبة التضخم وأسعار السوق'},
                {'term': 'كفالة', 'recommendation': 'إيجار شهرين', 'rationale': 'حماية حقوق المالك'},
                {'term': 'فترة السماح', 'recommendation': '15 يوم', 'rationale': 'مرونة في السداد'}
            ],
            'maintenance_responsibilities': [
                'المالك: الهيكل الإنشائي، الأنظمة الرئيسية',
                'المستأجر: الصيانة الدورية، الإصلاحات البسيطة',
                'مشترك: التلفيات الناتجة عن الإهمال'
            ],
            'renewal_terms': [
                'إخطار مسبق 90 يوم قبل انتهاء العقد',
                'الأولوية للمستأجر الحالي',
                'مراجعة السوق عند التجديد'
            ]
        }
    
    def _generate_rental_market_comparison(self):
        """مقارنة بالسوق الإيجاري"""
        
        return {
            'market_average': {
                'similar_properties': '110-150 ريال/م²/سنة',
                'area_average': '130 ريال/م²/سنة',
                'city_average': '125 ريال/م²/سنة'
            },
            'competitive_position': {
                'position': 'قريب من متوسط السوق',
                'advantages': ['موقع ممتاز', 'خدمات كاملة', 'مواقف كافية'],
                'disadvantages': ['عمر المبنى', 'نقص بعض المرافق']
            },
            'rental_trends': {
                'quarterly_growth': '+2.5%',
                'annual_growth': '+8.3%',
                'vacancy_rate': '7.2%'
            }
        }
    
    def _determine_rental_position(self, results):
        """تحديد موقع الإيجار في السوق"""
        
        rent_per_m2 = results.get('rent_per_m2', 0)
        
        if rent_per_m2 < 100:
            return 'تحت متوسط السوق'
        elif rent_per_m2 < 130:
            return 'قريب من متوسط السوق'
        elif rent_per_m2 < 160:
            return 'أعلى من متوسط السوق'
        else:
            return 'مرتفع مقارنة بالسوق'
    
    def _assess_rental_competitiveness(self, results):
        """تقييم القدرة التنافسية للإيجار"""
        
        factors = []
        rent_per_m2 = results.get('rent_per_m2', 0)
        
        if rent_per_m2 < 120:
            factors.append('سعر تنافسي')
        if results.get('adjustments'):
            adjustments = sum([abs(a) for a in results.get('adjustment_percentage', [])])
            if adjustments < 0.10:
                factors.append('مواصفات مقبولة')
        
        return factors or ['سعر معقول']
    
    def _assess_rental_growth(self, results):
        """تقييم إمكانات نمو الإيجار"""
        
        return {
            'short_term': '+2-3% سنوياً',
            'medium_term': '+15-20% خلال 5 سنوات',
            'long_term': '+30-40% خلال 10 سنوات',
            'drivers': ['نمو المنطقة', 'تحسين البنية التحتية', 'زيادة الطلب']
        }

# دالة مساعدة لإنشاء تقرير كامل
def create_professional_report(valuation_id, valuation_data, valuer_info, client_info):
    """دالة شاملة لإنشاء تقرير تقييم مهني"""
    
    report_generator = ProfessionalValuationReport(
        valuation_data=valuation_data,
        valuer_info=valuer_info,
        client_info=client_info
    )
    
    purpose = valuation_data.get('purpose', '')
    
    # ⬅️ تحديث: اختيار نوع التقرير حسب الغرض
    if purpose == "تحديد القيمة الإيجارية للموقع":
        detailed_report = report_generator.generate_rental_report()
        report_type = 'rental'
    else:
        detailed_report = report_generator.generate_full_report()
        report_type = 'valuation'
    
    # تقرير HTML للعرض
    html_report = report_generator.generate_html_report()
    
    return {
        'detailed_report': detailed_report,
        'html_report': html_report,
        'summary': {
            'valuation_id': valuation_id,
            'property_address': valuation_data.get('property_data', {}).get('address', ''),
            'purpose': purpose,
            'report_type': report_type,
            'report_date': report_generator.report_date
        }
    }
