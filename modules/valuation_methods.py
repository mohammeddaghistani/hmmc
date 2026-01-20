import pandas as pd
import numpy as np

class ValuationMethods:
    """منهجيات التقييم العقاري العلمية وفق المعايير الدولية IVS"""
    
    def __init__(self):
        self.methods = {
            'sales_comparison': 'مقارنة المبيعات',
            'residual': 'القيمة المتبقية',
            'dcf': 'التدفقات النقدية المخصومة',
            'profits': 'الأرباح'
        }

    def sales_comparison_method(self, subject_property, comparable_properties, adjustments_matrix):
        """معادلة مقارنة المبيعات المعدلة"""
        adjusted_prices = []
        for comp in comparable_properties:
            base_price = comp.get('price_per_m2', 0)
            # القيمة المعدلة = السعر الأساسي * (1 + مجموع نسب التعديلات)
            total_adj = sum(adjustments_matrix.values()) / 100
            adjusted_prices.append(base_price * (1 + total_adj))
        
        final_val = np.mean(adjusted_prices) if adjusted_prices else 0
        return {
            'total_value': final_val * subject_property.get('land_area', 1),
            'value_per_m2': final_val,
            'method': 'sales_comparison'
        }

    def residual_method(self, property_data):
        """معادلة القيمة المتبقية (قيمة الأرض = GDV - تكاليف البناء والربح)"""
        gdv = property_data.get('gdv', 0)
        costs = property_data.get('construction_cost', 0)
        profit = property_data.get('developer_profit', 0.20)
        land_value = gdv - (costs * (1 + profit))
        return {'total_value': max(0, land_value), 'method': 'residual'}

    def discounted_cash_flow_method(self, property_data):
        """معادلة التدفقات النقدية المخصومة DCF"""
        income = property_data.get('annual_income', 0)
        rate = property_data.get('discount_rate', 0.10)
        years = property_data.get('forecast_years', 10)
        pv = sum([income / ((1 + rate) ** t) for t in range(1, int(years) + 1)])
        return {'total_value': pv, 'method': 'dcf'}

    def profits_method(self, property_data):
        """معادلة الأرباح للعقارات التشغيلية"""
        revenue = property_data.get('revenue', 0)
        costs = property_data.get('operating_costs', 0)
        share = property_data.get('rent_share', 0.5)
        rent = (revenue - costs) * share
        return {'total_value': max(0, rent), 'method': 'profits'}

def apply_valuation_method(method_name, property_data, additional_data=None):
    """دالة الربط الأساسية لحل أخطاء الاستيراد"""
    valuator = ValuationMethods()
    additional_data = additional_data or {}
    if method_name == 'sales_comparison':
        return valuator.sales_comparison_method(property_data, additional_data.get('comparable_properties', []), additional_data.get('adjustments_matrix', {}))
    elif method_name == 'residual': return valuator.residual_method(property_data)
    elif method_name == 'dcf': return valuator.discounted_cash_flow_method(property_data)
    elif method_name == 'profits': return valuator.profits_method(property_data)
    return None
