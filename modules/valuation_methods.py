"""
وحدة طرق التقييم العقاري العلمية
تطبق منهجيات التقييم وفقاً للدليل والمعايير الدولية
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class ValuationMethods:
    """فئة تجمع جميع طرق التقييم العقاري العلمية"""
    
    def __init__(self):
        self.methods = {
            'sales_comparison': 'مقارنة المبيعات',
            'residual': 'القيمة المتبقية',
            'dcf': 'التدفقات النقدية المخصومة',
            'profits': 'الأرباح'
        }
    
    def sales_comparison_method(self, subject_property, comparable_properties, adjustments_matrix=None):
        """
        طريقة مقارنة المبيعات (Sales Comparison Method)
        تُستخدم عندما تتوفر بيانات لعقارات مشابهة تم بيعها أو تأجيرها حديثاً
        
        المعادلة: القيمة = متوسط الأسعار بعد التعديلات
        """
        
        try:
            # تحليل العقارات المقارنة
            adjusted_prices = []
            adjustment_details = []
            
            for i, comp in enumerate(comparable_properties):
                # السعر الأساسي
                base_price = comp.get('price_per_m2', 0)
                
                # تطبيق التعديلات
                adjustment_percentage = 0
                adjustments = []
                
                # 1. تعديل المساحة (المساحات الأصغر عادة أغلى)
                subject_area = subject_property.get('area_m2', 1000)
                comp_area = comp.get('area_m2', 1000)
                
                if comp_area > subject_area:
                    # إذا كانت المقارنة أكبر مساحة، نزيد سعر المتر
                    area_ratio = (comp_area - subject_area) / comp_area
                    area_adjustment = min(area_ratio * 0.3, 0.15)  # حتى 15% زيادة
                    adjustment_percentage += area_adjustment
                    adjustments.append(f"المساحة: +{area_adjustment*100:.1f}%")
                
                # 2. تعديل الموقع (استخدام مصفوفة الترجيح)
                if adjustments_matrix:
                    for factor, weight in adjustments_matrix.items():
                        if factor in comp:
                            diff = comp[factor] - subject_property.get(factor, 0)
                            adjustment = diff * weight
                            adjustment_percentage += adjustment
                            adjustments.append(f"{factor}: {adjustment*100:+.1f}%")
                
                # 3. تعديل العمر
                subject_age = subject_property.get('age_years', 0)
                comp_age = comp.get('age_years', 0)
                
                if comp_age > subject_age:
                    age_adjustment = (comp_age - subject_age) * 0.01
                    adjustment_percentage -= age_adjustment  # العقار الأقدم أقل قيمة
                    adjustments.append(f"العمر: -{age_adjustment*100:.1f}%")
                elif comp_age < subject_age:
                    age_adjustment = (subject_age - comp_age) * 0.01
                    adjustment_percentage += age_adjustment  # العقار الأحدث أعلى قيمة
                    adjustments.append(f"العمر: +{age_adjustment*100:.1f}%")
                
                # 4. تعديل حالة العقار
                subject_condition = subject_property.get('condition_score', 3)
                comp_condition = comp.get('condition_score', 3)
                condition_diff = subject_condition - comp_condition
                condition_adjustment = condition_diff * 0.02
                adjustment_percentage += condition_adjustment
                adjustments.append(f"الحالة: {condition_adjustment*100:+.1f}%")
                
                # حساب السعر المعدل
                adjusted_price = base_price * (1 + adjustment_percentage)
                adjusted_prices.append(adjusted_price)
                
                # تفاصيل التعديل
                adjustment_details.append({
                    'property_id': comp.get('id', i+1),
                    'base_price': base_price,
                    'adjustment_percentage': adjustment_percentage,
                    'adjusted_price': adjusted_price,
                    'adjustments': adjustments
                })
            
            # حساب القيمة النهائية
            if adjusted_prices:
                final_price_per_m2 = np.mean(adjusted_prices)
                confidence_level = self._calculate_confidence(adjusted_prices)
                
                return {
                    'method': 'sales_comparison',
                    'value_per_m2': round(final_price_per_m2, 2),
                    'total_value': round(final_price_per_m2 * subject_property.get('area_m2', 0), 2),
                    'confidence_score': confidence_level,
                    'comparable_count': len(comparable_properties),
                    'adjustment_details': adjustment_details,
                    'formula_used': 'القيمة = متوسط (أسعار المقارنة × (1 + نسبة التعديل))'
                }
            
            return None
            
        except Exception as e:
            print(f"خطأ في طريقة مقارنة المبيعات: {e}")
            return None
    
    def residual_method(self, development_data):
        """
        طريقة القيمة المتبقية (Residual Method)
        تُستخدم لتقييم الأراضي المعدة للتطوير
        
        المعادلة: قيمة الأرض = القيمة الإجمالية للمشروع - (التكاليف + ربح المطور)
        """
        
        try:
            # المدخلات الأساسية
            total_buildable_area = development_data.get('total_area_m2', 0)  # إجمالي المساحة القابلة للبناء
            construction_area = development_data.get('construction_area_m2', 0)  # المساحة المبنية
            expected_rent_per_m2 = development_data.get('expected_rent_per_m2', 0)
            occupancy_rate = development_data.get('occupancy_rate', 0.85)  # نسبة الإشغال
            yield_rate = development_data.get('yield_rate', 0.08)  # معدل العائد
            
            # تكاليف التطوير
            construction_cost_per_m2 = development_data.get('construction_cost_per_m2', 3000)
            professional_fees_percent = development_data.get('professional_fees_percent', 0.12)
            marketing_cost_percent = development_data.get('marketing_cost_percent', 0.05)
            finance_cost_percent = development_data.get('finance_cost_percent', 0.08)
            contingency_percent = development_data.get('contingency_percent', 0.10)
            
            # ربح المطور
            developer_profit_percent = development_data.get('developer_profit_percent', 0.20)
            
            # === حساب القيمة الإجمالية للمشروع المكتمل (GDV) ===
            # الإيراد السنوي
            annual_rental_income = construction_area * expected_rent_per_m2 * occupancy_rate
            
            # القيمة الرأسمالية
            gdv = annual_rental_income / yield_rate
            
            # === حساب التكاليف ===
            # تكلفة البناء
            construction_cost = construction_area * construction_cost_per_m2
            
            # الرسوم المهنية
            professional_fees = construction_cost * professional_fees_percent
            
            # تكاليف التسويق
            marketing_cost = gdv * marketing_cost_percent
            
            # تكاليف التمويل
            finance_cost = (construction_cost + professional_fees) * finance_cost_percent
            
            # مخصص الطوارئ
            contingency = construction_cost * contingency_percent
            
            # إجمالي التكاليف
            total_development_cost = (
                construction_cost +
                professional_fees +
                marketing_cost +
                finance_cost +
                contingency
            )
            
            # === حساب ربح المطور ===
            developer_profit = total_development_cost * developer_profit_percent
            
            # === حساب القيمة المتبقية (قيمة الأرض) ===
            land_value = gdv - (total_development_cost + developer_profit)
            
            # === تحويل إلى إيجار سنوي ===
            land_yield_rate = development_data.get('land_yield_rate', 0.05)
            annual_ground_rent = land_value * land_yield_rate
            
            # === تحليل الحساسية ===
            sensitivity_analysis = self._perform_sensitivity_analysis(
                gdv, total_development_cost, developer_profit
            )
            
            return {
                'method': 'residual',
                'gross_development_value': round(gdv, 2),
                'total_development_cost': round(total_development_cost, 2),
                'developer_profit': round(developer_profit, 2),
                'land_value': round(land_value, 2),
                'annual_ground_rent': round(annual_ground_rent, 2),
                'rent_per_m2': round(annual_ground_rent / total_buildable_area, 2) if total_buildable_area > 0 else 0,
                'sensitivity_analysis': sensitivity_analysis,
                'formula_used': 'قيمة الأرض = GDV - (التكاليف + ربح المطور)'
            }
            
        except Exception as e:
            print(f"خطأ في طريقة القيمة المتبقية: {e}")
            return None
    
    def discounted_cash_flow_method(self, cashflow_data):
        """
        طريقة التدفقات النقدية المخصومة (DCF)
        تُستخدم للعقارات ذات الدخل المتغير عبر الزمن
        
        المعادلة: القيمة = Σ (التدفق النقدي للسنة / (1 + معدل الخصم)^السنة)
        """
        
        try:
            # المدخلات الأساسية
            forecast_period = cashflow_data.get('forecast_period', 10)  # سنوات
            discount_rate = cashflow_data.get('discount_rate', 0.09)  # 9%
            terminal_growth_rate = cashflow_data.get('terminal_growth_rate', 0.02)  # 2%
            
            # بيانات الإيرادات
            initial_rent_per_m2 = cashflow_data.get('initial_rent_per_m2', 0)
            total_area = cashflow_data.get('total_area_m2', 0)
            occupancy_schedule = cashflow_data.get('occupancy_schedule', [0.4, 0.6, 0.75, 0.85, 0.9])
            
            # بيانات المصاريف
            operating_expenses_percent = cashflow_data.get('operating_expenses_percent', 0.35)
            management_fees_percent = cashflow_data.get('management_fees_percent', 0.03)
            maintenance_reserve_percent = cashflow_data.get('maintenance_reserve_percent', 0.02)
            
            # === حساب التدفقات النقدية السنوية ===
            cashflows = []
            detailed_cashflows = []
            
            for year in range(1, forecast_period + 1):
                # نسبة الإشغال لهذه السنة
                if year <= len(occupancy_schedule):
                    occupancy_rate = occupancy_schedule[year - 1]
                else:
                    occupancy_rate = occupancy_schedule[-1]  # آخر نسبة
                
                # معدل نمو الإيجار (افتراضي 3% سنوياً)
                rental_growth_rate = cashflow_data.get('rental_growth_rate', 0.03)
                current_rent = initial_rent_per_m2 * ((1 + rental_growth_rate) ** (year - 1))
                
                # الإيرادات
                gross_income = total_area * current_rent * occupancy_rate
                
                # المصاريف التشغيلية
                operating_expenses = gross_income * operating_expenses_percent
                management_fees = gross_income * management_fees_percent
                maintenance_reserve = gross_income * maintenance_reserve_percent
                
                # صافي الدخل التشغيلي (NOI)
                noi = gross_income - (operating_expenses + management_fees + maintenance_reserve)
                
                # التدفق النقدي بعد الضريبة (بافتراض 20% ضريبة)
                tax_rate = cashflow_data.get('tax_rate', 0.20)
                tax_payment = noi * tax_rate
                net_cashflow = noi - tax_payment
                
                # خصم التدفق النقدي
                discounted_cashflow = net_cashflow / ((1 + discount_rate) ** year)
                
                cashflows.append(discounted_cashflow)
                
                detailed_cashflows.append({
                    'year': year,
                    'occupancy_rate': occupancy_rate,
                    'rent_per_m2': current_rent,
                    'gross_income': gross_income,
                    'noi': noi,
                    'net_cashflow': net_cashflow,
                    'discounted_cashflow': discounted_cashflow
                })
            
            # === حساب القيمة النهائية (Terminal Value) ===
            # استخدام نموذج النمو الدائم (Perpetuity Growth Model)
            final_year_noi = detailed_cashflows[-1]['noi']
            terminal_value = (final_year_noi * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
            discounted_terminal_value = terminal_value / ((1 + discount_rate) ** forecast_period)
            
            # === حساب القيمة الإجمالية ===
            total_present_value = sum(cashflows) + discounted_terminal_value
            
            # === مقاييس العائد ===
            initial_investment = cashflow_data.get('initial_investment', total_present_value * 0.7)
            npv = total_present_value - initial_investment
            irr = self._calculate_irr(cashflows, initial_investment)
            
            return {
                'method': 'dcf',
                'total_present_value': round(total_present_value, 2),
                'net_present_value': round(npv, 2),
                'internal_rate_return': round(irr * 100, 2) if irr else None,
                'discounted_terminal_value': round(discounted_terminal_value, 2),
                'cashflow_details': detailed_cashflows,
                'key_assumptions': {
                    'discount_rate': discount_rate,
                    'rental_growth_rate': rental_growth_rate,
                    'terminal_growth_rate': terminal_growth_rate,
                    'forecast_period': forecast_period
                },
                'formula_used': 'القيمة = Σ (NOI / (1+r)^t) + (TV / (1+r)^n)'
            }
            
        except Exception as e:
            print(f"خطأ في طريقة التدفقات النقدية المخصومة: {e}")
            return None
    
    def profits_method(self, business_data):
        """
        طريقة الأرباح (Profits Method)
        تُستخدم للعقارات المتخصصة (فنادق، مستشفيات، محطات وقود)
        
        المعادلة: الإيجار = (EBITDA - استحقاقات المشغل) × نسبة الإيجار
        """
        
        try:
            # بيانات الإيرادات
            revenue_sources = business_data.get('revenue_sources', {})
            
            # حساب إجمالي الإيرادات
            total_revenue = sum(revenue_sources.values())
            
            # بيانات المصاريف التشغيلية
            operating_expenses_percent = business_data.get('operating_expenses_percent', 0.60)  # 60% من الإيرادات
            total_operating_expenses = total_revenue * operating_expenses_percent
            
            # حساب EBITDA (الربح قبل الفوائد والضرائب والإهلاك)
            ebitda = total_revenue - total_operating_expenses
            
            # خصم الإهلاك (Depreciation)
            depreciation_percent = business_data.get('depreciation_percent', 0.05)
            depreciation = total_revenue * depreciation_percent
            
            # خصم الضرائب
            tax_rate = business_data.get('tax_rate', 0.20)
            tax_payment = (ebitda - depreciation) * tax_rate
            
            # خصم مكافأة المشغل
            operator_remuneration_percent = business_data.get('operator_remuneration_percent', 0.10)
            operator_remuneration = total_revenue * operator_remuneration_percent
            
            # حساب الرصيد القابل للقسمة (Divisible Balance)
            divisible_balance = ebitda - depreciation - tax_payment - operator_remuneration
            
            # تحديد حصة الإيجار (عادة 50% من الرصيد القابل للقسمة)
            rent_share_percent = business_data.get('rent_share_percent', 0.50)
            market_rent = divisible_balance * rent_share_percent
            
            # تحليل الحساسية لتغيرات الإيرادات
            sensitivity = []
            for change in [-0.10, -0.05, 0, 0.05, 0.10]:  # ±10%, ±5%
                adjusted_revenue = total_revenue * (1 + change)
                adjusted_ebitda = adjusted_revenue * (1 - operating_expenses_percent)
                adjusted_balance = adjusted_ebitda * (1 - depreciation_percent - tax_rate - operator_remuneration_percent)
                adjusted_rent = adjusted_balance * rent_share_percent
                
                sensitivity.append({
                    'revenue_change': change * 100,
                    'adjusted_rent': adjusted_rent,
                    'rent_change': ((adjusted_rent - market_rent) / market_rent) * 100 if market_rent > 0 else 0
                })
            
            # مقارنة مع نسبة الإيجار إلى الإيرادات (Rent to Revenue Ratio)
            rent_to_revenue_ratio = (market_rent / total_revenue) * 100 if total_revenue > 0 else 0
            
            # مقارنة مع مضاعف EBITDA
            ebitda_multiple = business_data.get('ebitda_multiple', 8)  # 8x EBITDA شائع للفنادق
            implied_property_value = ebitda * ebitda_multiple
            implied_rent = implied_property_value * 0.08  # افتراض عائد 8%
            
            return {
                'method': 'profits',
                'total_revenue': round(total_revenue, 2),
                'ebitda': round(ebitda, 2),
                'divisible_balance': round(divisible_balance, 2),
                'market_rent': round(market_rent, 2),
                'rent_per_m2': round(market_rent / business_data.get('total_area_m2', 1), 2),
                'rent_to_revenue_ratio': round(rent_to_revenue_ratio, 2),
                'ebitda_multiple_valuation': round(implied_property_value, 2),
                'sensitivity_analysis': sensitivity,
                'key_assumptions': {
                    'operating_expenses_percent': operating_expenses_percent,
                    'rent_share_percent': rent_share_percent,
                    'ebitda_multiple': ebitda_multiple
                },
                'formula_used': 'الإيجار = (EBITDA - استحقاقات) × نسبة الإيجار'
            }
            
        except Exception as e:
            print(f"خطأ في طريقة الأرباح: {e}")
            return None
    
    def select_appropriate_method(self, property_type, data_availability):
        """
        اختيار طريقة التقييم المناسبة حسب نوع العقار وتوفر البيانات
        """
        
        method_selection = {
            'residential': {
                'high': 'sales_comparison',
                'medium': 'sales_comparison',
                'low': 'residual'
            },
            'commercial': {
                'high': 'dcf',
                'medium': 'sales_comparison',
                'low': 'residual'
            },
            'industrial': {
                'high': 'sales_comparison',
                'medium': 'dcf',
                'low': 'residual'
            },
            'hotel': {
                'high': 'profits',
                'medium': 'dcf',
                'low': 'sales_comparison'
            },
            'hospital': {
                'high': 'profits',
                'medium': 'dcf',
                'low': 'residual'
            },
            'gas_station': {
                'high': 'profits',
                'medium': 'sales_comparison',
                'low': 'residual'
            },
            'land': {
                'high': 'sales_comparison',
                'medium': 'residual',
                'low': 'residual'
            }
        }
        
        # تقييم توفر البيانات
        data_level = 'low'
        if data_availability.get('comparable_sales', 0) >= 3:
            data_level = 'high'
        elif data_availability.get('comparable_sales', 0) >= 1:
            data_level = 'medium'
        
        # اختيار الطريقة
        property_category = method_selection.get(property_type, 'residential')
        selected_method = property_category.get(data_level, 'sales_comparison')
        
        return {
            'selected_method': selected_method,
            'method_name': self.methods.get(selected_method, 'مقارنة المبيعات'),
            'data_level': data_level,
            'justification': self._get_method_justification(selected_method, property_type)
        }
    
    def _calculate_confidence(self, prices):
        """حساب درجة الثقة بناءً على تباين الأسعار"""
        if len(prices) <= 1:
            return 0.5
        
        std_dev = np.std(prices)
        mean_price = np.mean(prices)
        coefficient_variation = std_dev / mean_price if mean_price > 0 else 1
        
        # كلما قل التباين، زادت الثقة
        confidence = max(0.1, 1 - coefficient_variation)
        return round(confidence, 2)
    
    def _perform_sensitivity_analysis(self, gdv, costs, profit):
        """تحليل الحساسية لطريقة القيمة المتبقية"""
        scenarios = []
        
        for gdv_change in [-0.10, -0.05, 0, 0.05, 0.10]:
            for cost_change in [-0.05, 0, 0.05, 0.10]:
                adjusted_gdv = gdv * (1 + gdv_change)
                adjusted_costs = costs * (1 + cost_change)
                adjusted_land_value = adjusted_gdv - (adjusted_costs + profit)
                
                scenarios.append({
                    'gdv_change': gdv_change * 100,
                    'cost_change': cost_change * 100,
                    'land_value': adjusted_land_value,
                    'value_change': ((adjusted_land_value - (gdv - costs - profit)) / (gdv - costs - profit)) * 100
                })
        
        return scenarios
    
    def _calculate_irr(self, cashflows, initial_investment):
        """حساب معدل العائد الداخلي (IRR)"""
        try:
            # إضافة الاستثمار الأولي كتدفق نقدي سالب
            all_cashflows = [-initial_investment] + cashflows
            
            # حساب IRR باستخدام طريقة نيوتن-رافسون المبسطة
            def npv(rate):
                return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(all_cashflows))
            
            rate = 0.1  # معدل بداية
            for _ in range(100):
                npv_value = npv(rate)
                if abs(npv_value) < 0.0001:
                    return rate
                
                # المشتق العددي
                rate_plus = rate + 0.0001
                derivative = (npv(rate_plus) - npv_value) / 0.0001
                
                if abs(derivative) < 0.0001:
                    break
                    
                rate = rate - npv_value / derivative
            
            return rate
        except:
            return None
    
    def _get_method_justification(self, method, property_type):
        """توفير تبرير لاختيار الطريقة"""
        justifications = {
            'sales_comparison': f'توفر بيانات مبيعات/إيجارات حديثة لعقارات {property_type} مشابهة',
            'residual': f'الأرض مخصصة للتطوير ولا توجد عقارات {property_type} مشابهة للمقارنة',
            'dcf': f'عقار {property_type} ذو دخل متوقع عبر الزمن مع إمكانية التنبؤ بالتدفقات',
            'profits': f'عقار {property_type} متخصص تعتمد قيمته على النشاط التجاري'
        }
        return justifications.get(method, 'الطريقة الأنسب بناءً على توفر البيانات وطبيعة العقار')

# دالة مساعدة للاستخدام
def apply_valuation_method(method_name, property_data, additional_data=None):
    """دالة شاملة لتطبيق أي طريقة تقييم"""
    valuator = ValuationMethods()
    
    if method_name == 'sales_comparison':
        comparable_properties = additional_data.get('comparable_properties', [])
        adjustments_matrix = additional_data.get('adjustments_matrix', {
            'location': 0.30,
            'specifications': 0.25,
            'age': 0.20,
            'condition': 0.15,
            'facilities': 0.10
        })
        return valuator.sales_comparison_method(property_data, comparable_properties, adjustments_matrix)
    
    elif method_name == 'residual':
        return valuator.residual_method(property_data)
    
    elif method_name == 'dcf':
        return valuator.discounted_cash_flow_method(property_data)
    
    elif method_name == 'profits':
        return valuator.profits_method(property_data)
    
    else:
        # الاختيار التلقائي للطريقة
        data_availability = additional_data.get('data_availability', {'comparable_sales': 0})
        selection = valuator.select_appropriate_method(
            property_data.get('property_type', 'residential'),
            data_availability
        )
        
        # تطبيق الطريقة المختارة
        return apply_valuation_method(selection['selected_method'], property_data, additional_data)
