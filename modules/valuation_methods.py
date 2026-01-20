import numpy as np

class ValuationMethods:
    """تطبيق منهجيات التقييم العقاري العلمية"""

    def sales_comparison_method(self, base_price, adjustments):
        """معادلة مقارنة المبيعات: السعر المعدل = السعر الأساسي * (1 + مجموع التعديلات)"""
        total_adj = sum(adjustments.values()) / 100
        adjusted_price = base_price * (1 + total_adj)
        return adjusted_price

    def residual_method(self, gdv, const_cost, profit_margin):
        """معادلة القيمة المتبقية: قيمة الأرض = القيمة الإجمالية للمشروع - (تكاليف البناء + ربح المطور)"""
        total_costs = const_cost + (const_cost * profit_margin)
        land_value = gdv - total_costs
        return max(0, land_value)

    def dcf_method(self, annual_income, discount_rate, years, growth_rate):
        """معادلة التدفقات النقدية: NPV = Σ (Income / (1 + r)^t)"""
        pv = 0
        for t in range(1, int(years) + 1):
            income_t = annual_income * ((1 + growth_rate) ** (t - 1))
            pv += income_t / ((1 + discount_rate) ** t)
        return pv

    def profits_method(self, revenue, operating_costs, rent_share):
        """معادلة الأرباح: الإيجار السوقي = (الإيرادات - المصاريف) * حصة الإيجار"""
        ebitda = revenue - operating_costs
        market_rent = ebitda * rent_share
        return max(0, market_rent)
