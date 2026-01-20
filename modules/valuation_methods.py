import numpy as np

class ValuationMethods:
    """منهجيات التقييم العقاري العلمية IVS"""
    
    def sales_comparison_method(self, base_price, adjustments):
        """معادلة مقارنة المبيعات"""
        total_adj = sum(adjustments.values()) / 100
        return base_price * (1 + total_adj)

    def residual_method(self, gdv, const_cost, profit_margin):
        """معادلة القيمة المتبقية"""
        return max(0, gdv - (const_cost * (1 + profit_margin)))

    def dcf_method(self, annual_income, discount_rate, years, growth_rate=0.02):
        """معادلة التدفقات النقدية المخصومة"""
        pv = sum([ (annual_income * (1 + growth_rate)**t) / (1 + discount_rate)**(t+1) for t in range(years)])
        return pv

    def profits_method(self, revenue, operating_costs, rent_share):
        """معادلة الأرباح"""
        return max(0, (revenue - operating_costs) * rent_share)

def apply_valuation_method(method_name, property_data, additional_data=None):
    vm = ValuationMethods()
    adj = additional_data.get('adjustments_matrix', {}) if additional_data else {}
    
    if method_name == 'sales_comparison':
        val = vm.sales_comparison_method(property_data.get('base_price', 0), adj)
        return {'total_value': val * property_data.get('land_area', 1), 'method': 'مقارنة المبيعات'}
    elif method_name == 'residual':
        val = vm.residual_method(property_data.get('gdv', 0), property_data.get('construction_cost', 0), property_data.get('developer_profit', 0.2))
        return {'total_value': val, 'method': 'القيمة المتبقية'}
    elif method_name == 'dcf':
        val = vm.dcf_method(property_data.get('annual_income', 0), property_data.get('discount_rate', 0.1), property_data.get('forecast_years', 10))
        return {'total_value': val, 'method': 'التدفقات النقدية'}
    return None
