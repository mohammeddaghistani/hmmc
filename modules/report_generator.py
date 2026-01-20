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
        
        # قوالب أجزاء التقرير
        self.sections = {
            'title': "تقرير التقييم العقاري المهني",
            'executive_summary': "",
            'property_description': "",
            'valuation_basis': "",
            'valuation_analysis': "",
            'conclusions': "",
            'limitations': "",
            'certification': ""
        }
    
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
        
        return {
            'report_title': f"تقرير تقييم عقاري - {self.valuation_data.get('property_address', '')}",
            'valuation_number': f"VAL-{datetime.now().strftime('%Y%m%d')}-{self.valuation_data.get('id', '001')}",
            'valuation_date': self.valuation_date,
            'effective_date': self.valuation_data.get('effective_date', self.valuation_date),
            'purpose': self.valuation_data.get('purpose', 'تحديد القيمة السوقية'),
            'intended_users': self.valuation_data.get('intended_users', ['العميل', 'البنك التمويلي']),
            
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
    
    def _generate_facts_examination(self):
        """المجموعة الثانية: الحقائق والفحص"""
        
        property_data = self.valuation_data.get('property_data', {})
        
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
        
        analysis = {
            'methodology': {
                'selected_method': self._get_method_name(method),
                'justification': self._get_method_justification(method),
                'compliance': "متوافق مع المعيار الدولي للتقييم (IVS) 104 ومع دليل الهيئة"
            },
            
            'valuation_parameters': self._get_valuation_parameters(method),
            
            'detailed_calculations': self._format_calculations(method, results),
            
            'sensitivity_analysis': self._format_sensitivity_analysis(results),
            
            'final_valuation': {
                'market_value': f"{results.get('final_value', 0):,.0f} ريال سعودي",
                'value_per_m2': f"{results.get('value_per_m2', 0):,.0f} ريال/م²",
                'valuation_basis': results.get('valuation_basis', 'قيمة السوق العادلة'),
                'currency': "ريال سعودي (SAR)",
                'value_type': "القيمة السوقية (Market Value)",
                'special_assumptions': self.valuation_data.get('special_assumptions', [])
            }
        }
        
        return analysis
    
    def _generate_disclaimers_standards(self):
        """المجموعة الرابعة: إخلاء المسؤولية والمعايير"""
        
        return {
            'usage_restrictions': {
                'validity_period': "6 أشهر من تاريخ التقرير",
                'authorized_users': self.valuation_data.get('intended_users', ['العميل']),
                'prohibited_uses': "لا يجوز استخدام هذا التقرير لأغراض غير المذكورة دون موافقة كتابية"
            },
            
            'compliance_statements': {
                'ivs_compliance': "تم إعداد هذا التقرير وفقاً للمعايير الدولية للتقييم (IVS)",
                'saudi_standards': "متوافق مع دليل التقييم العقاري الصادر عن الهيئة السعودية للمقيمين المعتمدين",
                'ethics_code': "تم الالتزام بمدونة الأخلاقيات المهنية للمقيمين"
            },
            
            'disclaimers': {
                'liability': "المقيم غير مسؤول عن أي قرارات تتخذ بناءً على هذا التقرير",
                'market_uncertainty': self._generate_market_uncertainty_statement(),
                'data_reliance': "البيانات المعتمدة مقدمة من العميل وقد تكون قابلة للتحقق"
            },
            
            'signatures': {
                'valuer_signature': f"توقيع المقيم: {self.valuer_info.get('name', '')}",
                'date_issued': self.report_date,
                'stamp': "ختم الشركة المعتمدة"
            }
        }
    
    def _analyze_market_conditions(self, property_type):
        """تحليل ظروف السوق حسب نوع العقار"""
        
        market_analysis = {
            'residential': {
                'trend': "مستقر مع نمو طفيف",
                'demand': "مرتفع للوحدات السكنية الجيدة",
                'supply': "متوازن مع الطلب",
                'key_drivers': "النمو السكاني، توفر التمويل، مشاريع التنمية"
            },
            'commercial': {
                'trend': "متنامي في المناطق الرئيسية",
                'demand': "مرتفع للمكاتب الحديثة",
                'supply': "محدود للعقارات ذات المواصفات العالية",
                'key_drivers': "النمو الاقتصادي، استقرار الأعمال"
            },
            'industrial': {
                'trend': "مستقر مع زيادة الطلب على المستودعات",
                'demand': "متزايد للعقارات اللوجستية",
                'supply': "كافٍ في المناطق الصناعية",
                'key_drivers': "النمو التجاري، سلاسل التوريد"
            }
        }
        
        return market_analysis.get(property_type, market_analysis['residential'])
    
    def _get_method_name(self, method_key):
        """ترجمة مفتاح الطريقة إلى اسمها العربي"""
        method_names = {
            'sales_comparison': 'طريقة مقارنة المبيعات',
            'residual': 'طريقة القيمة المتبقية',
            'dcf': 'طريقة التدفقات النقدية المخصومة',
            'profits': 'طريقة الأرباح'
        }
        return method_names.get(method_key, 'طريقة مقارنة المبيعات')
    
    def _get_method_justification(self, method):
        """توفير تبرير لاختيار الطريقة"""
        justifications = {
            'sales_comparison': 'توفر بيانات كافية عن معاملات مشابهة حديثة',
            'residual': 'العقار مخصص للتطوير ولا توجد معاملات مشابهة',
            'dcf': 'العقار يدر دخلاً ويمكن التنبؤ بتدفقاته النقدية',
            'profits': 'قيمة العقار تعتمد على النشاط التجاري الذي يستضيفه'
        }
        return justifications.get(method, 'الطريقة الأنسب بناءً على توفر البيانات')
    
    def _get_valuation_parameters(self, method):
        """الحصول على معاملات التقييم حسب الطريقة"""
        
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
        
        return parameters.get(method, {})
    
    def _format_calculations(self, method, results):
        """تنسيق الحسابات التفصيلية حسب الطريقة"""
        
        if method == 'sales_comparison':
            return self._format_sales_comparison_calculations(results)
        elif method == 'residual':
            return self._format_residual_calculations(results)
        elif method == 'dcf':
            return self._format_dcf_calculations(results)
        elif method == 'profits':
            return self._format_profits_calculations(results)
        
        return {}
    
    def _format_sales_comparison_calculations(self, results):
        """تنسيق حسابات طريقة مقارنة المبيعات"""
        
        adjustments = results.get('adjustment_details', [])
        
        calculations = {
            'comparable_properties': [],
            'adjustment_summary': {},
            'final_calculation': {}
        }
        
        for adj in adjustments:
            calculations['comparable_properties'].append({
                'property': f"عقار مقارن #{adj.get('property_id', '')}",
                'base_price': f"{adj.get('base_price', 0):,.0f} ريال/م²",
                'adjustment_percentage': f"{adj.get('adjustment_percentage', 0)*100:+.1f}%",
                'adjusted_price': f"{adj.get('adjusted_price', 0):,.0f} ريال/م²",
                'adjustments': adj.get('adjustments', [])
            })
        
        if adjustments:
            prices = [adj.get('adjusted_price', 0) for adj in adjustments]
            calculations['adjustment_summary'] = {
                'average_price': f"{sum(prices)/len(prices):,.0f} ريال/م²",
                'standard_deviation': f"{np.std(prices) if len(prices) > 1 else 0:,.0f} ريال/م²",
                'confidence_level': f"{results.get('confidence_score', 0)*100:.0f}%"
            }
        
        return calculations
    
    def _format_residual_calculations(self, results):
        """تنسيق حسابات طريقة القيمة المتبقية"""
        
        return {
            'gross_development_value': {
                'label': 'القيمة الإجمالية للمشروع (GDV)',
                'value': f"{results.get('gross_development_value', 0):,.0f} ريال",
                'calculation': 'المساحة المبنية × الإيجار × نسبة الإشغال ÷ معدل العائد'
            },
            'development_costs': {
                'label': 'إجمالي تكاليف التطوير',
                'value': f"{results.get('total_development_cost', 0):,.0f} ريال",
                'breakdown': [
                    f"تكاليف البناء: {results.get('construction_cost', 0):,.0f} ريال",
                    f"الرسوم المهنية: {results.get('professional_fees', 0):,.0f} ريال",
                    f"التسويق: {results.get('marketing_cost', 0):,.0f} ريال"
                ]
            },
            'developer_profit': {
                'label': 'ربح المطور',
                'value': f"{results.get('developer_profit', 0):,.0f} ريال",
                'percentage': f"{self.valuation_data.get('developer_profit_percent', 0.20)*100:.0f}% من التكاليف"
            },
            'residual_land_value': {
                'label': 'القيمة المتبقية (قيمة الأرض)',
                'value': f"{results.get('land_value', 0):,.0f} ريال",
                'formula': 'GDV - (التكاليف + ربح المطور)'
            },
            'annual_ground_rent': {
                'label': 'الإيجار الأرضي السنوي',
                'value': f"{results.get('annual_ground_rent', 0):,.0f} ريال/سنوياً",
                'calculation': 'قيمة الأرض × معدل عائد الأرض'
            }
        }
    
    def _format_dcf_calculations(self, results):
        """تنسيق حسابات طريقة التدفقات النقدية المخصومة"""
        
        cashflows = results.get('cashflow_details', [])
        
        calculations = {
            'cashflow_forecast': [],
            'discounting_summary': {},
            'terminal_value': {},
            'investment_metrics': {}
        }
        
        for cf in cashflows[:5]:  # عرض أول 5 سنوات فقط
            calculations['cashflow_forecast'].append({
                'year': cf.get('year', 0),
                'occupancy': f"{cf.get('occupancy_rate', 0)*100:.0f}%",
                'rent': f"{cf.get('rent_per_m2', 0):,.0f} ريال/م²",
                'noi': f"{cf.get('noi', 0):,.0f} ريال",
                'discounted_cf': f"{cf.get('discounted_cashflow', 0):,.0f} ريال"
            })
        
        if cashflows:
            calculations['discounting_summary'] = {
                'total_present_value': f"{results.get('total_present_value', 0):,.0f} ريال",
                'discount_rate': f"{self.valuation_data.get('discount_rate', 0.09)*100:.1f}%",
                'present_value_of_cashflows': f"{sum(cf.get('discounted_cashflow', 0) for cf in cashflows):,.0f} ريال"
            }
        
        calculations['terminal_value'] = {
            'value': f"{results.get('discounted_terminal_value', 0):,.0f} ريال",
            'calculation': 'NOI السنة الأخيرة × (1+نمو) ÷ (معدل خصم - نمو)',
            'percentage_of_total': f"{(results.get('discounted_terminal_value', 0) / results.get('total_present_value', 1))*100:.0f}% من القيمة الإجمالية"
        }
        
        calculations['investment_metrics'] = {
            'npv': f"{results.get('net_present_value', 0):,.0f} ريال",
            'irr': f"{results.get('internal_rate_return', 0):.1f}%",
            'initial_investment': f"{self.valuation_data.get('initial_investment', 0):,.0f} ريال"
        }
        
        return calculations
    
    def _format_profits_calculations(self, results):
        """تنسيق حسابات طريقة الأرباح"""
        
        return {
            'revenue_analysis': {
                'total_revenue': f"{results.get('total_revenue', 0):,.0f} ريال",
                'revenue_sources': self.valuation_data.get('revenue_sources', {})
            },
            'profitability': {
                'ebitda': f"{results.get('ebitda', 0):,.0f} ريال",
                'ebitda_margin': f"{(results.get('ebitda', 0) / results.get('total_revenue', 1))*100:.1f}%",
                'divisible_balance': f"{results.get('divisible_balance', 0):,.0f} ريال"
            },
            'rent_calculation': {
                'market_rent': f"{results.get('market_rent', 0):,.0f} ريال/سنوياً",
                'rent_share': f"{self.valuation_data.get('rent_share_percent', 0.50)*100:.0f}% من الرصيد القابل للقسمة",
                'rent_to_revenue': f"{results.get('rent_to_revenue_ratio', 0):.1f}%"
            },
            'alternative_valuation': {
                'ebitda_multiple': f"{results.get('ebitda_multiple_valuation', 0):,.0f} ريال",
                'multiple_used': f"{self.valuation_data.get('ebitda_multiple', 8)}x EBITDA",
                'implied_rent': f"{results.get('ebitda_multiple_valuation', 0) * 0.08:,.0f} ريال/سنوياً"
            }
        }
    
    def _format_sensitivity_analysis(self, results):
        """تنسيق تحليل الحساسية"""
        
        sensitivity = results.get('sensitivity_analysis', [])
        
        if not sensitivity:
            return {"message": "لا يتوفر تحليل حساسية مفصل"}
        
        formatted = []
        for scenario in sensitivity[:5]:  # عرض 5 سيناريوهات فقط
            formatted.append({
                'scenario': f"تغير الإيرادات: {scenario.get('revenue_change', 0):+.0f}%",
                'rent_impact': f"{scenario.get('rent_change', 0):+.1f}%",
                'adjusted_rent': f"{scenario.get('adjusted_rent', 0):,.0f} ريال"
            })
        
        return formatted
    
    def _generate_market_uncertainty_statement(self):
        """بيان عدم اليقين المادي في ظروف السوق الاستثنائية"""
        
        market_condition = self.valuation_data.get('market_condition', 'stable')
        
        statements = {
            'volatile': "نظراً لظروف السوق المتقلبة حالياً، تنخفض درجة اليقين في هذا التقييم",
            'uncertain': "السوق يمر بفترة عدم يقين تؤثر على موثوقية التوقعات",
            'stable': "ظروف السوق مستقرة حالياً ولا توجد عوامل استثنائية",
            'crisis': "يتم التقييم خلال ظروف استثنائية قد تؤثر على دقة النتائج"
        }
        
        return statements.get(market_condition, statements['stable'])
    
    def generate_pdf_report(self):
        """توليد تقرير PDF احترافي"""
        
        pdf = FPDF()
        pdf.add_page()
        
        # إضافة محتوى التقرير
        report_content = self.generate_full_report()
        
        # هنا سيتم إضافة محتوى PDF مفصلاً
        # (مختصر لأغراض العرض)
        
        return pdf
    
    def generate_html_report(self):
        """توليد تقرير HTML تفاعلي"""
        
        template = """
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <title>تقرير التقييم العقاري</title>
            <style>
                body { font-family: 'Arial', sans-serif; margin: 40px; }
                .header { text-align: center; border-bottom: 3px solid #1E3A8A; padding: 20px; }
                .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; }
                .section-title { color: #1E3A8A; border-bottom: 2px solid #FBBF24; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; margin: 10px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
                th { background-color: #f2f2f2; }
                .value { color: #1E3A8A; font-weight: bold; }
                .disclaimer { background-color: #fff3cd; padding: 15px; border: 1px solid #ffc107; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>تقرير التقييم العقاري المهني</h1>
                <h3>رقم التقرير: {{valuation_number}}</h3>
                <p>تاريخ التقييم: {{valuation_date}}</p>
            </div>
            
            <div class="section">
                <h2 class="section-title">١. المعلومات الأساسية</h2>
                <p><strong>الغرض:</strong> {{purpose}}</p>
                <p><strong>المقيم:</strong> {{valuer_name}} - {{valuer_qualifications}}</p>
                <p><strong>العميل:</strong> {{client_name}}</p>
            </div>
            
            <div class="section">
                <h2 class="section-title">٢. وصف العقار والفحص</h2>
                <table>
                    <tr><th>المعيار</th><th>القيمة</th></tr>
                    <tr><td>العنوان</td><td>{{property_address}}</td></tr>
                    <tr><td>المساحة</td><td>{{property_area}} م²</td></tr>
                    <tr><td>نوع العقار</td><td>{{property_type}}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h2 class="section-title">٣. التحليل والتقييم</h2>
                <p><strong>الطريقة المستخدمة:</strong> {{valuation_method}}</p>
                <p><strong>القيمة السوقية:</strong> <span class="value">{{market_value}} ريال سعودي</span></p>
                <p><strong>القيمة للمتر المربع:</strong> {{value_per_m2}} ريال/م²</p>
            </div>
            
            <div class="section disclaimer">
                <h2 class="section-title">٤. إخلاء المسؤولية والمعايير</h2>
                <p>تم إعداد هذا التقرير وفقاً للمعايير الدولية للتقييم (IVS)</p>
                <p>فترة الصلاحية: 6 أشهر من تاريخ التقرير</p>
                <p>{{uncertainty_statement}}</p>
            </div>
        </body>
        </html>
        """
        
        # ملء القالب بالبيانات
        html_content = Template(template).render({
            'valuation_number': self.valuation_data.get('id', 'VAL-001'),
            'valuation_date': self.valuation_date,
            'purpose': self.valuation_data.get('purpose', 'تحديد القيمة السوقية'),
            'valuer_name': self.valuer_info.get('name', ''),
            'valuer_qualifications': ', '.join(self.valuer_info.get('qualifications', [])),
            'client_name': self.client_info.get('name', ''),
            'property_address': self.valuation_data.get('property_data', {}).get('address', ''),
            'property_area': self.valuation_data.get('property_data', {}).get('land_area_m2', 0),
            'property_type': self.valuation_data.get('property_data', {}).get('property_type', ''),
            'valuation_method': self._get_method_name(self.valuation_data.get('valuation_method', '')),
            'market_value': f"{self.valuation_data.get('valuation_results', {}).get('final_value', 0):,.0f}",
            'value_per_m2': f"{self.valuation_data.get('valuation_results', {}).get('value_per_m2', 0):,.0f}",
            'uncertainty_statement': self._generate_market_uncertainty_statement()
        })
        
        return html_content

# دالة مساعدة لإنشاء تقرير كامل
def create_professional_report(valuation_id, valuation_data, valuer_info, client_info):
    """دالة شاملة لإنشاء تقرير تقييم مهني"""
    
    report_generator = ProfessionalValuationReport(
        valuation_data=valuation_data,
        valuer_info=valuer_info,
        client_info=client_info
    )
    
    # تقرير مفصل (JSON)
    detailed_report = report_generator.generate_full_report()
    
    # تقرير HTML للعرض
    html_report = report_generator.generate_html_report()
    
    # تقرير PDF
    pdf_report = report_generator.generate_pdf_report()
    
    return {
        'detailed_report': detailed_report,
        'html_report': html_report,
        'pdf_report': pdf_report,
        'summary': {
            'valuation_id': valuation_id,
            'property_address': valuation_data.get('property_data', {}).get('address', ''),
            'market_value': valuation_data.get('valuation_results', {}).get('final_value', 0),
            'valuation_method': report_generator._get_method_name(valuation_data.get('valuation_method', '')),
            'report_date': report_generator.report_date
        }
    }
