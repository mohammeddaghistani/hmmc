"""
مولد تقارير التقييم المتوافقة مع المعايير الدولية (IVS) والملحق 4 
"""
from datetime import datetime
import json

class ProfessionalValuationReport:
    """فئة لتوليد بيانات التقارير المهنية المهيكلة """
    
    def __init__(self, valuation_data, valuer_info, client_info):
        self.valuation_data = valuation_data
        self.valuer_info = valuer_info
        self.client_info = client_info
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        self.valuation_date = valuation_data.get('valuation_date', self.report_date)
        
        # قائمة أغراض التقييم الشاملة 
        self.purposes = [
            "تحديد القيمة الإيجارية للموقع", "تحديد القيمة السوقية",
            "التمويل البنكي", "الشراكة", "التأمين", "الضرائب",
            "التخطيط المالي", "التسعير للإيجار", "تحديد رسوم التملك",
            "التثمين للاستحواذ", "التقييم للغرامات"
        ]
    
    def generate_full_report(self):
        """توليد البيانات الكاملة للتقرير """
        return {
            'basic_information': self._generate_basic_information(),
            'facts_examination': self._generate_facts_examination(),
            'analysis_valuation': self._generate_analysis_valuation(),
            'disclaimers_standards': self._generate_disclaimers_standards()
        }

    def _generate_basic_information(self):
        """المعلومات الأساسية وتحديد نوع الغرض """
        purpose = self.valuation_data.get('purpose', 'تحديد القيمة الإيجارية للموقع')
        return {
            'report_title': f"تقرير تقييم عقاري - {self.valuation_data.get('property_address', '')}",
            'valuation_number': f"VAL-{datetime.now().strftime('%Y%m%d')}-{self.valuation_data.get('id', '001')}",
            'purpose': purpose,
            'purpose_type': self._get_purpose_type(purpose),
            'valuer_info': self.valuer_info,
            'client_info': self.client_info
        }

    def _get_purpose_type(self, purpose):
        """تصنيف الغرض (إيجاري، سوقي، مالي، قانوني) """
        if purpose in ["تحديد القيمة الإيجارية للموقع", "التسعير للإيجار"]:
            return "تقييم إيجاري"
        elif purpose in ["تحديد القيمة السوقية", "التثمين للاستحواذ"]:
            return "تقييم سوقي"
        return "تقييم عام"

    def _generate_facts_examination(self):
        """الحقائق والفحص ومعلومات الإيجار """
        property_data = self.valuation_data.get('property_data', {})
        purpose = self.valuation_data.get('purpose', '')
        
        # إضافة معلومات الإيجار إذا كان الغرض إيجاري 
        rental_info = {}
        if purpose == "تحديد القيمة الإيجارية للموقع":
            rental_info = {
                'current_rent': property_data.get('current_rent', 'غير محدد'),
                'lease_term': property_data.get('lease_term', 'غير محدد'),
                'rental_history': property_data.get('rental_history', 'لا توجد سجلات سابقة')
            }
        
        return {
            'description': property_data,
            'rental_information': rental_info,
            'inspection_details': "فحص ميداني شامل مطابق للمعايير"
        }

    def _generate_analysis_valuation(self):
        """التحليل المالي وتحديد القيمة الإيجارية أو السوقية """
        results = self.valuation_data.get('valuation_results', {})
        purpose = self.valuation_data.get('purpose', '')
        
        # تحديد التسميات حسب الغرض 
        value_label = "القيمة الإيجارية المقترحة" if "إيجار" in purpose else "القيمة السوقية المقدرة"
        
        return {
            'methodology': self.valuation_data.get('valuation_method', 'sales_comparison'),
            'final_valuation': {
                'value': results.get('final_value', 0),
                'value_label': value_label,
                'currency': "ريال سعودي"
            }
        }

    def _generate_disclaimers_standards(self):
        """إخلاء المسؤولية والالتزام بالمعايير الدولية """
        return {
            'compliance': "هذا التقرير متوافق مع معايير IVS 2024",
            'disclaimer': "تم إعداد هذا التقرير بناءً على المعلومات المتوفرة وتاريخ الفحص الميداني."
        }
