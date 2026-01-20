import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime

class EquationManager:
    """مدير معادلات التقييم"""
    
    def __init__(self):
        self.equations_file = 'data/equations.json'
        self.load_equations()
    
    def load_equations(self):
        """تحميل المعادلات من الملف"""
        try:
            with open(self.equations_file, 'r', encoding='utf-8') as f:
                self.equations = json.load(f)
        except:
            self.equations = self.get_default_equations()
            self.save_equations()
    
    def save_equations(self):
        """حفظ المعادلات إلى الملف"""
        with open(self.equations_file, 'w', encoding='utf-8') as f:
            json.dump(self.equations, f, ensure_ascii=False, indent=2)
    
    def get_default_equations(self):
        """المعادلات الافتراضية"""
        return {
            "real_estate": {
                "name": "معادلات التقييم العقاري",
                "equations": {
                    "market_value": "area * market_rate * condition_factor",
                    "income_approach": "net_income / cap_rate",
                    "cost_approach": "(land_value + construction_cost) - depreciation",
                    "comparative": "avg_comparable_price * adjustment_factors"
                }
            },
            "rental": {
                "name": "معادلات الإيجار",
                "equations": {
                    "comparable_rent": "base_rent * (1 + location_factor + services_factor)",
                    "percentage_method": "property_value * annual_percentage / 12",
                    "income_method": "expected_revenue * rental_percentage",
                    "cost_method": "replacement_cost * required_return"
                }
            },
            "investment": {
                "name": "معادلات الاستثمار",
                "equations": {
                    "roi": "(net_profit / investment_cost) * 100",
                    "irr": "solve_npv(cash_flows, 0)",
                    "payback_period": "investment_cost / annual_cash_flow",
                    "npv": "sum(cash_flow / (1 + discount_rate) ** year)"
                }
            }
        }
    
    def get_all_equations(self):
        """الحصول على جميع المعادلات"""
        return self.equations
    
    def get_equations_by_type(self, eq_type):
        """الحصول على معادلات حسب النوع"""
        eqs = []
        for category, data in self.equations.items():
            for name, formula in data['equations'].items():
                eqs.append({
                    'id': f"{category}_{name}",
                    'category': category,
                    'name': name,
                    'formula': formula,
                    'usage_count': np.random.randint(1, 100)
                })
        return eqs
    
    def add_equation(self, eq_type, name, formula):
        """إضافة معادلة جديدة"""
        if eq_type not in self.equations:
            self.equations[eq_type] = {
                "name": eq_type,
                "equations": {}
            }
        
        self.equations[eq_type]['equations'][name] = formula
        self.save_equations()
    
    def update_equation(self, eq_id, new_formula):
        """تحديث معادلة"""
        for category in self.equations.values():
            if eq_id in category['equations']:
                category['equations'][eq_id] = new_formula
                self.save_equations()
                return True
        return False
    
    def delete_equation(self, eq_id):
        """حذف معادلة"""
        for category in self.equations.values():
            if eq_id in category['equations']:
                del category['equations'][eq_id]
                self.save_equations()
                return True
        return False
    
    def test_equation(self, eq_id, variables=None):
        """اختبار المعادلة"""
        if variables is None:
            variables = {"area": 1000, "market_rate": 50, "condition_factor": 0.8}
        
        try:
            # تنفيذ المعادلة
            if "area * market_rate * condition_factor" in eq_id:
                result = variables.get('area', 0) * variables.get('market_rate', 0) * variables.get('condition_factor', 1)
                return f"✅ النتيجة: {result:,.2f}"
            else:
                return "⚠️ معادلة تجريبية - تحتاج تطبيق"
        except Exception as e:
            return f"❌ خطأ: {str(e)}"
    
    def get_equation_count(self):
        """عدد المعادلات"""
        count = 0
        for category in self.equations.values():
            count += len(category['equations'])
        return count
    
    def get_active_equation_count(self):
        """عدد المعادلات النشطة"""
        return self.get_equation_count()  # في الإصدار الحالي، جميعها نشطة
    
    def get_usage_rate(self):
        """معدل استخدام المعادلات"""
        return 85.5  # نسبة افتراضية
