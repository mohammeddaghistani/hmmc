"""
وحدة متخصصة لتحديد القيمة الإيجارية للموقع
لأغراض تحديد الإيجارات الأرضية والتأجير طويل الأجل
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
from modules.valuation_methods import ValuationMethods

class SiteRentalValuation:
    """فئة متخصصة في تحديد القيمة الإيجارية للمواقع"""
    
    def __init__(self):
        self.methods = ValuationMethods()
        self.site_types = {
            'land': 'أرض خام',
            'developed_land': 'أرض مخدمة',
            'industrial': 'موقع صناعي',
            'commercial': 'موقع تجاري',
            'agricultural': 'موقع زراعي',
            'tourism': 'موقع سياحي',
            'residential': 'موقع سكني',
            'mixed_use': 'استخدام مختلط'
        }
        
        self.services_list = {
            'electricity': 'كهرباء',
            'water': 'مياه',
            'sewage': 'صرف صحي',
            'roads': 'طرق معبدة',
            'fencing': 'سور',
            'lighting': 'إنارة',
            'internet': 'إنترنت',
            'security': 'حراسة'
        }
    
    def render_site_rental_module(self):
        """عرض واجهة تحديد القيمة الإيجارية للموقع"""
        
        st.markdown("""
        <div class="section-header">
            <h2>📍 نظام تحديد القيمة الإيجارية للموقع</h2>
            <p>تقييم متخصص للإيجارات الأرضية والمواقع طويلة الأجل</p>
        </div>
        """, unsafe_allow_html=True)
        
        # تبويبات الوحدة
        tab1, tab2, tab3, tab4 = st.tabs([
            "🆕 تقييم موقع جديد", 
            "🗺️ خريطة الإيجارات", 
            "📊 تحليل المنطقة",
            "📑 تقارير الإيجار"
        ])
        
        with tab1:
            self.render_new_site_valuation()
        
        with tab2:
            self.render_rental_map()
        
        with tab3:
            self.render_area_analysis()
        
        with tab4:
            self.render_rental_reports()
    
    def render_new_site_valuation(self):
        """نموذج تقييم موقع جديد"""
        
        st.subheader("📍 معلومات الموقع الأساسية")
        
        with st.form("site_rental_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # معلومات الموقع
                site_name = st.text_input("اسم الموقع", placeholder="مثل: قطعة أرض في حي النخيل")
                site_type = st.selectbox(
                    "نوع الموقع",
                    list(self.site_types.values())
                )
                
                # المساحة والإحداثيات
                site_area = st.number_input("مساحة الموقع (م²)", min_value=1.0, value=1000.0)
                frontage_length = st.number_input("طول الواجهة (م)", min_value=0.0, value=20.0)
                
                # الموقع الجغرافي
                city = st.selectbox(
                    "المدينة",
                    ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الشرقية", "أخرى"]
                )
                district = st.text_input("الحي / المنطقة", placeholder="اسم الحي أو المنطقة")
            
            with col2:
                # الخدمات المتوفرة
                st.subheader("⚡ الخدمات المتوفرة")
                services_selected = {}
                for key, service in self.services_list.items():
                    services_selected[key] = st.checkbox(service, value=(key in ['electricity', 'water', 'roads']))
                
                # التراخيص
                st.subheader("📜 التراخيص والاستخدام")
                zoning_type = st.selectbox(
                    "التصنيف البلدي",
                    ["سكني", "تجاري", "صناعي", "زراعي", "سياحي", "مختلط", "تعليمي", "صحي"]
                )
                allowed_uses = st.text_area(
                    "الاستخدامات المسموحة",
                    placeholder="مثال: سكني عائلي، عمارة سكنية حتى 4 أدوار، مركز تجاري"
                )
                
                # فترة التأجير المطلوبة
                lease_term = st.slider("فترة التأجير المطلوبة (سنوات)", 1, 50, 10)
            
            st.markdown("---")
            
            # منهجية التقييم
            st.subheader("📊 منهجية تحديد القيمة الإيجارية")
            
            method = st.radio(
                "اختر طريقة التقييم المناسبة:",
                [
                    "مقارنة إيجارات مواقع مشابهة",
                    "القيمة المتبقية للتطوير",
                    "نسبة من قيمة الأرض",
                    "طريقة الدخل (للمواقع التجارية)",
                    "طريقة التكلفة (للمواقع المبنية)"
                ]
            )
            
            if method == "مقارنة إيجارات مواقع مشابهة":
                self.render_comparable_rentals_input()
            elif method == "القيمة المتبقية للتطوير":
                self.render_residual_for_rent()
            elif method == "نسبة من قيمة الأرض":
                self.render_percentage_of_value()
            elif method == "طريقة الدخل (للمواقع التجارية)":
                self.render_income_method()
            elif method == "طريقة التكلفة (للمواقع المبنية)":
                self.render_cost_method()
            
            st.markdown("---")
            
            # أزرار التحكم
            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
            
            with col_btn1:
                if st.form_submit_button("🚀 تحديد القيمة الإيجارية", use_container_width=True):
                    self.calculate_site_rental_value(
                        site_data={
                            'name': site_name,
                            'type': site_type,
                            'area': site_area,
                            'frontage': frontage_length,
                            'city': city,
                            'district': district,
                            'services': services_selected,
                            'zoning': zoning_type,
                            'allowed_uses': allowed_uses,
                            'lease_term': lease_term
                        },
                        method=method
                    )
            
            with col_btn2:
                st.form_submit_button("💾 حفظ كمسودة", use_container_width=True, type="secondary")
            
            with col_btn3:
                st.form_submit_button("🧹 إعادة تعيين", use_container_width=True, type="secondary")
    
    def render_comparable_rentals_input(self):
        """إدخال بيانات الإيجارات المقارنة"""
        
        st.info("📋 أدخل بيانات مواقع مشابهة تم تأجيرها حديثاً")
        
        # عدد العقارات المقارنة
        num_comparables = st.number_input("عدد المواقع المقارنة", min_value=1, max_value=10, value=3)
        
        # جدول للإدخال
        comparables = []
        for i in range(num_comparables):
            with st.expander(f"الموقع المقارن #{i+1}", expanded=(i == 0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    address = st.text_input(f"📍 موقع #{i+1}", placeholder="الموقع", key=f"addr_{i}")
                    rent_per_m2 = st.number_input(f"💰 الإيجار/م²/سنة", value=100.0, key=f"rent_{i}")
                    area = st.number_input(f"📏 المساحة (م²)", value=1000.0, key=f"area_{i}")
                
                with col2:
                    frontage = st.number_input(f"📐 طول الواجهة (م)", value=20.0, key=f"front_{i}")
                    services_count = st.slider(f"⚡ عدد الخدمات", 0, 8, 3, key=f"serv_{i}")
                    location_score = st.slider(f"⭐ جودة الموقع (1-5)", 1, 5, 3, key=f"loc_{i}")
                
                # إدخال إضافي
                col3, col4 = st.columns(2)
                with col3:
                    year_rented = st.number_input(f"📅 سنة التأجير", min_value=2010, max_value=2024, value=2023, key=f"year_{i}")
                with col4:
                    lease_term = st.number_input(f"⏱️ فترة الإيجار (سنوات)", min_value=1, max_value=50, value=5, key=f"term_{i}")
                
                comparables.append({
                    'address': address,
                    'rent_per_m2': rent_per_m2,
                    'area': area,
                    'frontage': frontage,
                    'services_count': services_count,
                    'location_score': location_score,
                    'year_rented': year_rented,
                    'lease_term': lease_term
                })
        
        st.session_state.site_comparables = comparables
    
    def render_residual_for_rent(self):
        """طريقة القيمة المتبقية للإيجار"""
        
        st.info("🏗️ حساب الإيجار من خلال قيمة تطوير الموقع")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 معلومات الأرض")
            land_value = st.number_input("القيمة السوقية للأرض (ريال)", value=1000000.0)
            land_area = st.number_input("مساحة الأرض (م²)", value=1000.0)
            
            st.subheader("🏗️ معلومات التطوير")
            construction_cost_per_m2 = st.number_input("تكلفة البناء للمتر (ريال)", value=3000.0)
            built_area = st.number_input("المساحة المبنية (م²)", value=800.0)
        
        with col2:
            st.subheader("📈 عوامل التكلفة")
            professional_fees = st.slider("الرسوم المهنية %", 5, 20, 12)
            marketing_cost = st.slider("تكاليف التسويق %", 2, 10, 5)
            finance_cost = st.slider("تكاليف التمويل %", 3, 15, 8)
            contingency = st.slider("مخصص الطوارئ %", 5, 15, 10)
            
            st.subheader("🎯 ربحية المشروع")
            developer_profit = st.slider("ربح المطور %", 10, 40, 20)
            land_yield_rate = st.slider("معدل عائد الأرض %", 3, 15, 8)
        
        # الحساب التلقائي
        construction_cost = built_area * construction_cost_per_m2
        total_development_cost = construction_cost * (1 + professional_fees/100 + marketing_cost/100 + finance_cost/100 + contingency/100)
        developer_profit_amount = total_development_cost * (developer_profit / 100)
        
        # حساب GDV (افتراضي)
        estimated_gdv = total_development_cost + developer_profit_amount + land_value
        
        # حساب الإيجار
        annual_ground_rent = land_value * (land_yield_rate / 100)
        monthly_rent = annual_ground_rent / 12
        rent_per_m2 = annual_ground_rent / land_area
        
        st.markdown("### 💰 الحساب التقديري")
        st.write(f"""
        **ملخص التكاليف:**
        - تكلفة البناء: {construction_cost:,.0f} ريال
        - إجمالي تكاليف التطوير: {total_development_cost:,.0f} ريال
        - ربح المطور: {developer_profit_amount:,.0f} ريال
        - القيمة الإجمالية للمشروع: {estimated_gdv:,.0f} ريال
        
        **الإيجار المقترح:**
        - القيمة الإيجارية السنوية: {annual_ground_rent:,.0f} ريال
        - الإيجار الشهري: {monthly_rent:,.0f} ريال
        - ريال/م²/سنة: {rent_per_m2:,.1f}
        """)
    
    def render_percentage_of_value(self):
        """طريقة نسبة من قيمة الأرض"""
        
        st.info("💎 حساب الإيجار كنسبة مئوية من قيمة الأرض")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("💰 قيمة الأرض")
            land_value = st.number_input("القيمة السوقية للأرض (ريال)", value=1000000.0)
            value_source = st.selectbox(
                "مصدر القيمة",
                ["تقييم حديث", "سجل العقاري", "مقارنة سوقية", "تقدير المقيم"]
            )
        
        with col2:
            st.subheader("📊 النسبة المئوية")
            percentage = st.slider("النسبة المئوية السنوية %", 1.0, 20.0, 8.0)
            
            st.info(f"""
            **نطاق النسب المقترحة:**
            - أراضي سكنية: 5-7%
            - مواقع تجارية: 7-10%
            - مواقع صناعية: 6-9%
            - أراضي زراعية: 3-5%
            """)
        
        with col3:
            st.subheader("📐 المساحة")
            area = st.number_input("مساحة الأرض (م²)", value=1000.0)
            usable_area = st.slider("النسبة القابلة للاستخدام %", 50, 100, 85)
        
        # حساب الإيجار
        annual_rent = land_value * (percentage / 100)
        monthly_rent = annual_rent / 12
        rent_per_m2 = annual_rent / area
        effective_rent_per_m2 = annual_rent / (area * usable_area/100)
        
        st.markdown("### 📊 نتائج الحساب")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.metric("الإيجار السنوي", f"{annual_rent:,.0f} ريال")
            st.caption(f"نسبة {percentage}% من القيمة")
        
        with col_res2:
            st.metric("الإيجار الشهري", f"{monthly_rent:,.0f} ريال")
            st.caption("شهرياً")
        
        with col_res3:
            st.metric("ريال/م²/سنة", f"{rent_per_m2:,.1f}")
            st.caption(f"فعلي: {effective_rent_per_m2:,.1f} مع نسبة استخدام {usable_area}%")
        
        st.info(f"""
        **تفسير النسبة {percentage}%:**
        - هذه النسبة تعكس العائد المتوقع من استثمار الأرض
        - تأخذ في الاعتبار المخاطر وفرص النمو في المنطقة
        - تتوافق مع أسعار الفائدة السائدة في السوق
        """)
    
    def render_income_method(self):
        """طريقة الدخل للمواقع التجارية"""
        
        st.info("🏪 حساب الإيجار بناءً على الدخل المتوقع للمشروع")
        
        tab1, tab2, tab3 = st.tabs(["الإيرادات", "المصاريف", "التوقعات"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 مصادر الإيرادات")
                expected_revenue = st.number_input("الدخل السنوي المتوقع (ريال)", value=500000.0)
                revenue_growth = st.slider("نمو الإيرادات السنوي %", 0, 20, 5)
                seasonal_factor = st.slider("تذبذب موسمي %", 0, 50, 15)
            
            with col2:
                st.subheader("📈 جودة الدخل")
                revenue_stability = st.slider("استقرار الدخل (1-5)", 1, 5, 3,
                    help="1: متقلب جداً, 5: مستقر تماماً")
                payment_history = st.selectbox("سجل السداد",
                    ["ممتاز", "جيد", "متوسط", "ضعيف", "غير معروف"])
        
        with tab2:
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("💸 المصاريف التشغيلية")
                operating_expenses = st.slider("نسبة المصاريف التشغيلية %", 20, 80, 40)
                fixed_costs = st.number_input("التكاليف الثابتة السنوية (ريال)", value=100000.0)
                variable_costs_percent = st.slider("التكاليف المتغيرة % من الإيرادات", 10, 50, 25)
            
            with col4:
                st.subheader("📊 الربحية")
                target_profit_margin = st.slider("هامش الربح المستهدف %", 10, 50, 25)
                industry_average = st.number_input("متوسط هامش القطاع %", value=30.0)
                competitive_position = st.select_slider("الموقع التنافسي",
                    options=["ضعيف", "متوسط", "جيد", "ممتاز"], value="جيد")
        
        with tab3:
            col5, col6 = st.columns(2)
            
            with col5:
                st.subheader("📅 شروط الإيجار")
                rental_to_revenue = st.slider("نسبة الإيجار من الدخل %", 5, 30, 15)
                lease_term = st.slider("فترة الإيجار (سنوات)", 1, 20, 5)
                rent_escalation = st.slider("زيادة إيجار سنوية %", 0, 10, 3)
            
            with col6:
                st.subheader("📊 عوامل المخاطرة")
                business_risk = st.slider("مخاطر النشاط (1-5)", 1, 5, 3)
                market_risk = st.slider("مخاطر السوق (1-5)", 1, 5, 3)
                location_risk = st.slider("مخاطر الموقع (1-5)", 1, 5, 2)
        
        # الحسابات
        net_income = expected_revenue * (1 - operating_expenses/100)
        variable_costs = expected_revenue * (variable_costs_percent / 100)
        total_costs = fixed_costs + variable_costs
        gross_profit = expected_revenue - total_costs
        target_profit = expected_revenue * (target_profit_margin / 100)
        available_for_rent = gross_profit - target_profit
        suggested_rent = available_for_rent * (rental_to_revenue / 100)
        
        # حساب عامل المخاطرة
        total_risk = (business_risk + market_risk + location_risk) / 15  # طبيعي بين 0-1
        risk_adjustment = 1 - (total_risk * 0.2)  # تخفيض يصل إلى 20%
        adjusted_rent = suggested_rent * risk_adjustment
        
        st.markdown("### 💼 تحليل الدخل")
        
        col_sum1, col_sum2 = st.columns(2)
        
        with col_sum1:
            st.write(f"""
            **الإيرادات والمصاريف:**
            - الدخل المتوقع: {expected_revenue:,.0f} ريال
            - المصاريف التشغيلية ({operating_expenses}%): {expected_revenue * operating_expenses/100:,.0f} ريال
            - التكاليف الثابتة: {fixed_costs:,.0f} ريال
            - التكاليف المتغيرة: {variable_costs:,.0f} ريال
            - إجمالي التكاليف: {total_costs:,.0f} ريال
            """)
        
        with col_sum2:
            st.write(f"""
            **الربحية:**
            - الربح الإجمالي: {gross_profit:,.0f} ريال
            - الربح المستهدف ({target_profit_margin}%): {target_profit:,.0f} ريال
            - المبلغ المتاح للإيجار: {available_for_rent:,.0f} ريال
            - عامل المخاطرة: {total_risk:.2f} (تخفيض {((1-risk_adjustment)*100):.1f}%)
            """)
        
        st.metric("الإيجار المقترح", f"{adjusted_rent:,.0f} ريال/سنة")
        st.caption(f"الأصل: {suggested_rent:,.0f} ريال | بعد تعديل المخاطرة: {adjusted_rent:,.0f} ريال")
        
        # جدول الزيادات السنوية
        if rent_escalation > 0:
            st.markdown("### 📈 جدول الزيادات السنوية")
            
            data = []
            for year in range(1, lease_term + 1):
                annual_rent = adjusted_rent * ((1 + rent_escalation/100) ** (year-1))
                cumulative_increase = ((1 + rent_escalation/100) ** (year-1) - 1) * 100
                data.append({
                    'السنة': year,
                    'الإيجار السنوي': f"{annual_rent:,.0f}",
                    'الإيجار الشهري': f"{annual_rent/12:,.0f}",
                    'الزيادة السنوية': f"{rent_escalation if year > 1 else 0}%",
                    'الزيادة التراكمية': f"{cumulative_increase:.1f}%"
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
    
    def render_cost_method(self):
        """طريقة التكلفة للمواقع المبنية"""
        
        st.info("🏗️ حساب الإيجار بناءً على تكلفة الإنشاء والاستبدال")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏗️ تكاليف الإنشاء")
            construction_cost_per_m2 = st.number_input("تكلفة البناء للمتر (ريال)", value=3000.0)
            total_area = st.number_input("المساحة الإجمالية (م²)", value=1000.0)
            construction_year = st.number_input("سنة البناء", min_value=1900, max_value=2024, value=2020)
            
            st.subheader("📉 الإهلاك")
            useful_life = st.slider("العمر الإفتراضي (سنوات)", 10, 100, 50)
            depreciation_method = st.selectbox("طريقة الإهلاك", ["خطي", "متناقص"])
            salvage_value_percent = st.slider("قيمة الخردة %", 0, 50, 10)
        
        with col2:
            st.subheader("🎯 العائد المطلوب")
            required_return = st.slider("العائد المطلوب على الاستثمار %", 5, 20, 10)
            operating_expenses_percent = st.slider("نسبة المصاريف التشغيلية %", 15, 40, 25)
            vacancy_rate = st.slider("معدل الشغور %", 0, 30, 10)
            
            st.subheader("📊 عوامل الجودة")
            construction_quality = st.slider("جودة البناء (1-5)", 1, 5, 3)
            maintenance_level = st.slider("مستوى الصيانة (1-5)", 1, 5, 3)
            functional_obsolescence = st.slider("تقادم وظيفي (1-5)", 1, 5, 2,
                help="1: حديث تماماً, 5: قديم وغير عملي")
        
        # الحسابات
        replacement_cost = construction_cost_per_m2 * total_area
        
        # حساب الإهلاك
        age = 2024 - construction_year
        if depreciation_method == "خطي":
            annual_depreciation = replacement_cost / useful_life
            accumulated_depreciation = annual_depreciation * age
        else:  # متناقص
            depreciation_rate = 2 / useful_life  # ضعف المعدل الخطي
            accumulated_depreciation = replacement_cost * (1 - (1 - depreciation_rate) ** age)
        
        depreciated_value = max(replacement_cost - accumulated_depreciation, 
                               replacement_cost * salvage_value_percent/100)
        
        # عوامل الجودة
        quality_factor = (construction_quality + maintenance_level) / 10  # 0.2-1.0
        obsolescence_factor = 1 - (functional_obsolescence / 10)  # 0.9-0.5
        adjusted_value = depreciated_value * quality_factor * obsolescence_factor
        
        # حساب الإيجار
        required_income = adjusted_value * (required_return / 100)
        gross_required = required_income / (1 - operating_expenses_percent/100)
        gross_required_adjusted = gross_required / (1 - vacancy_rate/100)
        
        annual_rent = gross_required_adjusted
        monthly_rent = annual_rent / 12
        rent_per_m2 = annual_rent / total_area
        
        st.markdown("### 🏗️ تحليل التكلفة")
        
        col_calc1, col_calc2 = st.columns(2)
        
        with col_calc1:
            st.write(f"""
            **تكاليف الإنشاء:**
            - تكلفة الاستبدال: {replacement_cost:,.0f} ريال
            - العمر: {age} سنة من {useful_life} سنة
            - إهلاك متراكم: {accumulated_depreciation:,.0f} ريال
            - القيمة بعد الإهلاك: {depreciated_value:,.0f} ريال
            """)
        
        with col_calc2:
            st.write(f"""
            **تعديلات الجودة:**
            - عامل الجودة: {quality_factor:.2f}
            - عامل التقادم: {obsolescence_factor:.2f}
            - القيمة المعدلة: {adjusted_value:,.0f} ريال
            - العائد المطلوب ({required_return}%): {required_income:,.0f} ريال
            """)
        
        st.metric("الإيجار السنوي المقترح", f"{annual_rent:,.0f} ريال")
        st.caption(f"شهرياً: {monthly_rent:,.0f} ريال | للمتر: {rent_per_m2:,.1f} ريال/م²")
        
        st.info(f"""
        **ملاحظات:**
        - هذه الطريقة مناسبة للمباني الجديدة أو ذات القيمة الإنشائية العالية
        - تأخذ في الاعتبار تكلفة استبدال المبنى حالياً
        - تعكس قيمة الأرض والبناء معاً
        """)
    
    def calculate_site_rental_value(self, site_data, method):
        """حساب القيمة الإيجارية للموقع"""
        
        with st.spinner("🔍 جاري تحديد القيمة الإيجارية للموقع..."):
            
            # عرض خطوات الحساب
            steps = {
                "مقارنة إيجارات مواقع مشابهة": [
                    "1. جمع وتحليل الإيجارات المشابهة",
                    "2. تطبيق تعديلات الخدمات والموقع",
                    "3. حساب متوسط القيم المعدلة",
                    "4. تحديد الإيجار المناسب"
                ],
                "القيمة المتبقية للتطوير": [
                    "1. حساب القيمة الإجمالية للمشروع",
                    "2. خصم تكاليف التطوير وربح المطور",
                    "3. تحديد قيمة الأرض",
                    "4. حساب الإيجار كنسبة من القيمة"
                ],
                "نسبة من قيمة الأرض": [
                    "1. تحديد القيمة السوقية للأرض",
                    "2. تطبيق نسبة العائد المناسبة",
                    "3. حساب الإيجار السنوي",
                    "4. تحويل للقيمة الشهرية"
                ],
                "طريقة الدخل (للمواقع التجارية)": [
                    "1. تقدير الدخل المتوقع للمشروع",
                    "2. حساب المصاريف التشغيلية",
                    "3. تحديد الربح التشغيلي",
                    "4. استخلاص الإيجار المناسب"
                ],
                "طريقة التكلفة (للمواقع المبنية)": [
                    "1. حساب تكلفة الاستبدال",
                    "2. تطبيق الإهلاك والاستهلاك",
                    "3. تحديد القيمة الحالية",
                    "4. حساب العائد المطلوب"
                ]
            }
            
            if method in steps:
                st.info(f"### 📋 خطوات طريقة {method}:")
                for step in steps[method]:
                    st.write(f"✅ {step}")
            
            # حساب القيمة الإيجارية
            results = self._perform_site_rental_calculation(site_data, method)
            
            if results:
                self.display_site_rental_results(results, site_data)
                
                # حفظ النتائج
                st.session_state.last_site_valuation = {
                    'site_data': site_data,
                    'method': method,
                    'results': results,
                    'timestamp': datetime.now()
                }
            else:
                st.error("❌ لم يتمكن النظام من تحديد القيمة الإيجارية. يرجى التحقق من البيانات.")
    
    def _perform_site_rental_calculation(self, site_data, method):
        """إجراء الحسابات الفعلية"""
        
        try:
            if method == "مقارنة إيجارات مواقع مشابهة":
                return self._calculate_by_comparables(site_data)
            elif method == "القيمة المتبقية للتطوير":
                return self._calculate_by_residual(site_data)
            elif method == "نسبة من قيمة الأرض":
                return self._calculate_by_percentage(site_data)
            elif method == "طريقة الدخل (للمواقع التجارية)":
                return self._calculate_by_income(site_data)
            elif method == "طريقة التكلفة (للمواقع المبنية)":
                return self._calculate_by_cost(site_data)
        except Exception as e:
            st.error(f"❌ خطأ في الحساب: {str(e)}")
            return None
    
    def _calculate_by_comparables(self, site_data):
        """الحساب عن طريق المقارنة"""
        
        comparables = st.session_state.get('site_comparables', [])
        
        if not comparables:
            # بيانات افتراضية للعرض
            comparables = [
                {
                    'rent_per_m2': 100, 
                    'area': 1200, 
                    'services_count': 3, 
                    'location_score': 4,
                    'frontage': 25,
                    'year_rented': 2023,
                    'lease_term': 5
                },
                {
                    'rent_per_m2': 90, 
                    'area': 1500, 
                    'services_count': 2, 
                    'location_score': 3,
                    'frontage': 20,
                    'year_rented': 2022,
                    'lease_term': 3
                },
                {
                    'rent_per_m2': 110, 
                    'area': 1000, 
                    'services_count': 4, 
                    'location_score': 5,
                    'frontage': 30,
                    'year_rented': 2024,
                    'lease_term': 10
                }
            ]
        
        # حساب المتوسطات
        base_rent = np.mean([c['rent_per_m2'] for c in comparables])
        
        # تطبيق التعديلات
        adjustments = []
        total_adjustment = 0
        
        # تعديل الخدمات
        avg_services = np.mean([c['services_count'] for c in comparables])
        site_services = sum(site_data['services'].values())
        
        if site_services > avg_services:
            service_adj = min((site_services - avg_services) * 0.02, 0.10)
            total_adjustment += service_adj
            adjustments.append(f"الخدمات: +{service_adj*100:.1f}%")
        elif site_services < avg_services:
            service_adj = max((site_services - avg_services) * 0.02, -0.10)
            total_adjustment += service_adj
            adjustments.append(f"الخدمات: {service_adj*100:.1f}%")
        
        # تعديل طول الواجهة
        avg_frontage = np.mean([c.get('frontage', 20) for c in comparables])
        site_frontage = site_data.get('frontage', 20)
        
        if site_frontage > avg_frontage:
            frontage_adj = min((site_frontage - avg_frontage) / avg_frontage * 0.1, 0.15)
            total_adjustment += frontage_adj
            adjustments.append(f"الواجهة: +{frontage_adj*100:.1f}%")
        elif site_frontage < avg_frontage:
            frontage_adj = max((site_frontage - avg_frontage) / avg_frontage * 0.1, -0.10)
            total_adjustment += frontage_adj
            adjustments.append(f"الواجهة: {frontage_adj*100:.1f}%")
        
        # تعديل جودة الموقع (افتراضي)
        location_adj = 0.05  # +5% للموقع الجيد
        total_adjustment += location_adj
        adjustments.append(f"جودة الموقع: +{location_adj*100:.1f}%")
        
        # تعديل فترة الإيجار
        avg_lease_term = np.mean([c.get('lease_term', 5) for c in comparables])
        site_lease_term = site_data.get('lease_term', 5)
        
        if site_lease_term > avg_lease_term:
            term_adj = min((site_lease_term - avg_lease_term) * 0.005, 0.10)
            total_adjustment -= term_adj  # فترة أطول = خصم
            adjustments.append(f"فترة الإيجار الطويلة: -{term_adj*100:.1f}%")
        
        # حساب القيمة النهائية
        adjusted_rent = base_rent * (1 + total_adjustment)
        annual_rent = adjusted_rent * site_data['area']
        monthly_rent = annual_rent / 12
        
        return {
            'method': 'comparables',
            'base_rent_per_m2': round(base_rent, 2),
            'adjusted_rent_per_m2': round(adjusted_rent, 2),
            'adjustment_percentage': round(total_adjustment * 100, 2),
            'adjustments': adjustments,
            'annual_rent': round(annual_rent, 2),
            'monthly_rent': round(monthly_rent, 2),
            'rent_per_m2': round(adjusted_rent, 2),
            'comparable_count': len(comparables),
            'confidence_score': min(0.95, 0.7 + (len(comparables) * 0.05))
        }
    
    def _calculate_by_residual(self, site_data):
        """الحساب بطريقة القيمة المتبقية"""
        
        # قيم افتراضية (في الواقع ستكون من المستخدم)
        land_value = 1000000
        land_yield_rate = 0.08  # 8%
        
        annual_rent = land_value * land_yield_rate
        monthly_rent = annual_rent / 12
        rent_per_m2 = annual_rent / site_data['area']
        
        return {
            'method': 'residual',
            'land_value': land_value,
            'yield_rate': round(land_yield_rate * 100, 2),
            'annual_rent': round(annual_rent, 2),
            'monthly_rent': round(monthly_rent, 2),
            'rent_per_m2': round(rent_per_m2, 2),
            'confidence_score': 0.75
        }
    
    def _calculate_by_percentage(self, site_data):
        """الحساب بنسبة من القيمة"""
        
        # قيم افتراضية
        land_value = 1000000
        percentage = 8.0  # 8%
        
        annual_rent = land_value * (percentage / 100)
        monthly_rent = annual_rent / 12
        rent_per_m2 = annual_rent / site_data['area']
        
        return {
            'method': 'percentage',
            'land_value': land_value,
            'percentage': percentage,
            'annual_rent': round(annual_rent, 2),
            'monthly_rent': round(monthly_rent, 2),
            'rent_per_m2': round(rent_per_m2, 2),
            'confidence_score': 0.80
        }
    
    def _calculate_by_income(self, site_data):
        """الحساب بطريقة الدخل"""
        
        # قيم افتراضية
        expected_revenue = 500000
        rental_to_revenue = 15  # 15%
        
        suggested_rent = expected_revenue * (rental_to_revenue / 100)
        monthly_rent = suggested_rent / 12
        rent_per_m2 = suggested_rent / site_data['area']
        
        return {
            'method': 'income',
            'expected_revenue': expected_revenue,
            'rental_to_revenue': rental_to_revenue,
            'annual_rent': round(suggested_rent, 2),
            'monthly_rent': round(monthly_rent, 2),
            'rent_per_m2': round(rent_per_m2, 2),
            'confidence_score': 0.70
        }
    
    def _calculate_by_cost(self, site_data):
        """الحساب بطريقة التكلفة"""
        
        # قيم افتراضية
        construction_cost_per_m2 = 3000
        total_area = site_data['area']
        replacement_cost = construction_cost_per_m2 * total_area
        required_return = 0.10  # 10%
        
        annual_rent = replacement_cost * required_return
        monthly_rent = annual_rent / 12
        rent_per_m2 = annual_rent / total_area
        
        return {
            'method': 'cost',
            'replacement_cost': round(replacement_cost, 2),
            'required_return': round(required_return * 100, 2),
            'annual_rent': round(annual_rent, 2),
            'monthly_rent': round(monthly_rent, 2),
            'rent_per_m2': round(rent_per_m2, 2),
            'confidence_score': 0.65
        }
    
    def display_site_rental_results(self, results, site_data):
        """عرض نتائج تحديد القيمة الإيجارية"""
        
        st.success("✅ تم تحديد القيمة الإيجارية بنجاح!")
        
        st.markdown("### 📊 نتائج التقييم الإيجاري")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 الإيجار السنوي", f"{results['annual_rent']:,.0f} ر.س")
        
        with col2:
            st.metric("📅 الإيجار الشهري", f"{results['monthly_rent']:,.0f} ر.س")
        
        with col3:
            if 'rent_per_m2' in results:
                st.metric("📐 ريال/م²/سنة", f"{results['rent_per_m2']:,.1f}")
            else:
                st.metric("📊 المنهجية", results['method'])
        
        with col4:
            if 'adjustment_percentage' in results:
                st.metric("⚖️ إجمالي التعديل", f"{results['adjustment_percentage']:+.1f}%")
            elif 'confidence_score' in results:
                st.metric("⭐ درجة الثقة", f"{results['confidence_score']*100:.0f}%")
            else:
                st.metric("📍 مساحة الموقع", f"{site_data['area']:,.0f} م²")
        
        # عرض التفاصيل حسب الطريقة
        st.markdown("---")
        
        if results['method'] == 'comparables':
            self._display_comparable_details(results)
        elif results['method'] == 'residual':
            self._display_residual_details(results)
        elif results['method'] == 'percentage':
            self._display_percentage_details(results)
        elif results['method'] == 'income':
            self._display_income_details(results)
        elif results['method'] == 'cost':
            self._display_cost_details(results)
        
        # خيارات إضافية
        st.markdown("---")
        
        col_opt1, col_opt2, col_opt3, col_opt4 = st.columns(4)
        
        with col_opt1:
            if st.button("📄 إنشاء عقد إيجار", use_container_width=True):
                self.generate_lease_agreement(results, site_data)
        
        with col_opt2:
            if st.button("📊 تحليل تفصيلي", use_container_width=True):
                self.show_detailed_analysis(results, site_data)
        
        with col_opt3:
            if st.button("💾 حفظ التقييم", use_container_width=True):
                self.save_site_valuation(results, site_data)
                st.success("✅ تم حفظ التقييم الإيجاري")
        
        with col_opt4:
            if st.button("🔄 تقييم جديد", use_container_width=True):
                st.rerun()
    
    def _display_comparable_details(self, results):
        """عرض تفاصيل طريقة المقارنة"""
        
        st.subheader("🏘️ تفاصيل المواقع المقارنة")
        
        st.write(f"""
        **ملخص التحليل:**
        - عدد المواقع المقارنة: {results.get('comparable_count', 0)}
        - متوسط الإيجار الأساسي: {results.get('base_rent_per_m2', 0):,.1f} ريال/م²
        - الإيجار المعدل: {results.get('adjusted_rent_per_m2', 0):,.1f} ريال/م²
        - درجة الثقة: {results.get('confidence_score', 0)*100:.0f}%
        """)
        
        if results.get('adjustments'):
            st.write("**التعديلات المطبقة:**")
            for adj in results['adjustments']:
                st.write(f"• {adj}")
        
        # عرض توصيات إضافية
        st.subheader("🎯 توصيات الإيجار")
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.write("**للمالك:**")
            st.write("• ضع سعراً بين ±5% من القيمة المقترحة")
            st.write("• ضع في الاعتبار فترة الإيجار الطويلة")
            st.write("• فكر في زيادة سنوية بنسبة 3-5%")
        
        with col_rec2:
            st.write("**للمستأجر:**")
            st.write("• تفاوض على فترة سماح للسداد")
            st.write("• اطلب تحديد مسؤوليات الصيانة")
            st.write("• تأكد من شروط التجديد")
    
    def _display_residual_details(self, results):
        """عرض تفاصيل طريقة القيمة المتبقية"""
        
        st.subheader("🏗️ تفاصيل طريقة القيمة المتبقية")
        
        st.write(f"""
        **المدخلات:**
        - قيمة الأرض: {results.get('land_value', 0):,.0f} ريال
        - معدل العائد: {results.get('yield_rate', 0):.1f}%
        """)
        
        st.write(f"""
        **الحساب:**
        - الإيجار السنوي = قيمة الأرض × معدل العائد
        - = {results.get('land_value', 0):,.0f} × {results.get('yield_rate', 0)/100:.3f}
        - = **{results.get('annual_rent', 0):,.0f} ريال**
        """)
        
        st.info(f"""
        **تفسير معدل العائد {results.get('yield_rate', 0):.1f}%:**
        - يعكس العائد المتوقع من استثمار الأرض
        - يأخذ في الاعتبار المخاطر وفرص النمو
        - يتناسب مع أسعار الفائدة السائدة
        """)
    
    def _display_percentage_details(self, results):
        """عرض تفاصيل طريقة النسبة"""
        
        st.subheader("💎 تفاصيل طريقة النسبة من القيمة")
        
        st.write(f"""
        **المدخلات:**
        - قيمة الأرض: {results.get('land_value', 0):,.0f} ريال
        - النسبة المئوية: {results.get('percentage', 0):.1f}%
        """)
        
        st.write(f"""
        **الحساب:**
        - الإيجار السنوي = قيمة الأرض × النسبة المئوية
        - = {results.get('land_value', 0):,.0f} × {results.get('percentage', 0)/100:.3f}
        - = **{results.get('annual_rent', 0):,.0f} ريال**
        """)
        
        st.info(f"""
        **تفسير النسبة {results.get('percentage', 0):.1f}%:**
        - نسب متوسطة للأراضي السكنية: 5-7%
        - نسب للمواقع التجارية: 7-10%
        - نسب للمواقع الصناعية: 6-9%
        - نسب للمواقع الزراعية: 3-5%
        """)
    
    def _display_income_details(self, results):
        """عرض تفاصيل طريقة الدخل"""
        
        st.subheader("💼 تفاصيل طريقة الدخل")
        
        st.write(f"""
        **المدخلات:**
        - الدخل المتوقع: {results.get('expected_revenue', 0):,.0f} ريال
        - نسبة الإيجار من الدخل: {results.get('rental_to_revenue', 0):.1f}%
        """)
        
        st.write(f"""
        **الحساب:**
        - الإيجار المقترح = الدخل المتوقع × نسبة الإيجار
        - = {results.get('expected_revenue', 0):,.0f} × {results.get('rental_to_revenue', 0)/100:.3f}
        - = **{results.get('annual_rent', 0):,.0f} ريال**
        """)
        
        st.info(f"""
        **تفسير نسبة الإيجار {results.get('rental_to_revenue', 0):.1f}%:**
        - نسب متوسطة للمطاعم: 8-12%
        - نسب للمحلات التجارية: 10-15%
        - نسب للمكاتب: 15-20%
        - نسب للمراكز التجارية: 12-18%
        """)
    
    def _display_cost_details(self, results):
        """عرض تفاصيل طريقة التكلفة"""
        
        st.subheader("🏗️ تفاصيل طريقة التكلفة")
        
        st.write(f"""
        **المدخلات:**
        - تكلفة الاستبدال: {results.get('replacement_cost', 0):,.0f} ريال
        - العائد المطلوب: {results.get('required_return', 0):.1f}%
        """)
        
        st.write(f"""
        **الحساب:**
        - الإيجار السنوي = تكلفة الاستبدال × العائد المطلوب
        - = {results.get('replacement_cost', 0):,.0f} × {results.get('required_return', 0)/100:.3f}
        - = **{results.get('annual_rent', 0):,.0f} ريال**
        """)
        
        st.info(f"""
        **ملاحظات:**
        - هذه الطريقة مناسبة للمباني الجديدة
        - تأخذ في الاعتبار تكلفة إعادة الإنشاء
        - تعكس القيمة الاقتصادية الحقيقية
        """)
    
    def show_detailed_analysis(self, results, site_data):
        """عرض تحليل تفصيلي"""
        
        st.subheader("📊 تحليل تفصيلي للقيمة الإيجارية")
        
        # تحليل السوق
        st.markdown("### 📈 تحليل السوق الإيجاري")
        
        market_data = {
            'المؤشر': ['متوسط السوق', 'أعلى سعر', 'أقل سعر', 'العرض المتاح'],
            'القيمة': [
                f"{results.get('rent_per_m2', 0)*0.9:,.1f}-{results.get('rent_per_m2', 0)*1.1:,.1f} ريال/م²",
                f"{results.get('rent_per_m2', 0)*1.3:,.1f} ريال/م²",
                f"{results.get('rent_per_m2', 0)*0.7:,.1f} ريال/م²",
                "15-20 موقع مماثل"
            ]
        }
        
        st.table(pd.DataFrame(market_data))
        
        # توصيات التسعير
        st.markdown("### 🎯 استراتيجيات التسعير")
        
        col_strat1, col_strat2 = st.columns(2)
        
        with col_strat1:
            st.write("**للاستئجار السريع:**")
            st.write(f"- السعر: {results.get('rent_per_m2', 0)*0.95:,.1f} ريال/م²")
            st.write(f"- السنوي: {results.get('annual_rent', 0)*0.95:,.0f} ريال")
            st.write("- المزايا: جذب مستأجرين سريعاً")
        
        with col_strat2:
            st.write("**للاستثمار طويل الأجل:**")
            st.write(f"- السعر: {results.get('rent_per_m2', 0)*1.05:,.1f} ريال/م²")
            st.write(f"- السنوي: {results.get('annual_rent', 0)*1.05:,.0f} ريال")
            st.write("- المزايا: عائد أعلى واستقرار")
        
        # تحليل المخاطر
        st.markdown("### ⚠️ تحليل المخاطر")
        
        risks = [
            {"المخاطر": "تقلبات السوق", "التأثير": "متوسط", "التخفيف": "عقد طويل الأجل"},
            {"المخاطر": "تغير السياسات", "التأثير": "منخفض", "التخفيف": "مراجعة دورية"},
            {"المخاطر": "صعوبة السداد", "التأثير": "مرتفع", "التخفيف": "كفالة شهرين"},
            {"المخاطر": "تلف الممتلكات", "التأثير": "متوسط", "التخفيف": "تأمين شامل"}
        ]
        
        st.table(pd.DataFrame(risks))
    
    def generate_lease_agreement(self, results, site_data):
        """توليد نموذج عقد إيجار"""
        
        st.info("📝 جاري إنشاء نموذج عقد إيجار...")
        
        # حساب القيم المختلفة
        annual_rent = results.get('annual_rent', 0)
        monthly_rent = results.get('monthly_rent', 0)
        security_deposit = monthly_rent * 2  # كفالة شهرين
        
        agreement_template = f"""
        # عقد إيجار موقع
        
        **رقم العقد:** LEASE-{datetime.now().strftime('%Y%m%d%H%M')}
        **تاريخ العقد:** {datetime.now().strftime('%Y-%m-%d')}
        
        ## ١. أطراف العقد
        - **المؤجر (الطرف الأول):** [اسم المؤجر]
          - الهوية/السجل التجاري: [رقم الهوية/السجل]
          - العنوان: [عنوان المؤجر]
          - الهاتف: [هاتف المؤجر]
          - البريد الإلكتروني: [بريد المؤجر]
        
        - **المستأجر (الطرف الثاني):** [اسم المستأجر]
          - الهوية/السجل التجاري: [رقم الهوية/السجل]
          - العنوان: [عنوان المستأجر]
          - الهاتف: [هاتف المستأجر]
          - البريد الإلكتروني: [بريد المستأجر]
        
        ## ٢. وصف الموقع المؤجر
        - **اسم الموقع:** {site_data.get('name', 'غير محدد')}
        - **الموقع:** {site_data.get('city', '')} - {site_data.get('district', '')}
        - **المساحة:** {site_data.get('area', 0):,.0f} متر مربع
        - **طول الواجهة:** {site_data.get('frontage', 0):,.1f} متر
        - **الخدمات المتوفرة:** {', '.join([self.services_list[k] for k, v in site_data.get('services', {}).items() if v])}
        - **التصنيف البلدي:** {site_data.get('zoning', 'غير محدد')}
        - **الاستخدامات المسموحة:** {site_data.get('allowed_uses', 'حسب التصنيف البلدي')}
        
        ## ٣. بنود الإيجار
        - **مدة العقد:** {site_data.get('lease_term', 5)} سنوات
        - **تاريخ بداية الإيجار:** [تاريخ البداية]
        - **تاريخ نهاية الإيجار:** [تاريخ النهاية]
        - **قيمة الإيجار السنوية:** {annual_rent:,.0f} ريال سعودي
        - **قيمة الإيجار الشهرية:** {monthly_rent:,.0f} ريال سعودي
        - **الكفالة:** {security_deposit:,.0f} ريال سعودي (شهرين إيجار)
        - **طريقة السداد:** [شهري/ربع سنوي/سنوي] في أول كل [فترة]
        - **زيادة الإيجار:** 3% سنوياً أو حسب اتفاق الطرفين
        
        ## ٤. الغرض من الاستخدام
        يُستخدم الموقع المؤجر للأغراض التالية فقط:
        {site_data.get('allowed_uses', 'حسب التصنيف البلدي')}
        
        ## ٥. التزامات الأطراف
        
        **أ. التزامات المؤجر:**
        1. تسليم الموقع للمستأجر في الحالة المتفق عليها
        2. صيانة الهيكل الإنشائي والأنظمة الرئيسية
        3. توفير الخدمات الأساسية (كهرباء، مياه، صرف صحي)
        4. عدم التعرض لحق المستأجر في الانتفاع بالمؤجر خلال مدة العقد
        
        **ب. التزامات المستأجر:**
        1. دفع الإيجار في موعده المحدد
        2. صيانة الموقع والمحافظة عليه
        3. استخدام الموقع للغرض المتفق عليه فقط
        4. عدم إجراء تعديلات دون موافقة كتابية من المؤجر
        5. إعادة الموقع في نهاية العقد كما كان عند التسليم
        
        ## ٦. شروط التجديد والفسخ
        
        **أ. التجديد:**
        - للمستأجر الحق في تجديد العقد لفترة مماثلة بشروط تتوافق مع سوق الإيجار وقت التجديد
        - يجب إخطار المؤجر برغبة التجديد قبل 90 يوم من انتهاء العقد
        
        **ب. الفسخ:**
        1. للمؤجر فسخ العقد في حال تأخر المستأجر عن دفع الإيجار لمدة 30 يوم
        2. للمستأجر فسخ العقد بموافقة المؤجر أو بدفع تعويض قدره [مبلغ التعويض]
        3. ينفسخ العقد تلقائياً في حال هدم الموقع أو تعرضه لأضرار جسيمة
        
        ## ٧. أحكام عامة
        1. يخضع هذا العقد لأحكام نظام الإيجار السعودي
        2. أي نزاع ينشأ عن هذا العقد يحل ودياً أو عن طريق المحاكم المختصة
        3. يعتبر العقد نافذاً من تاريخ توقيعه من الطرفين
        4. يمكن تعديل العقد بموافقة كتابية من الطرفين
        
        ## ٨. التوقيعات
        
        **المؤجر (الطرف الأول):**
        
        الاسم: __________________________
        التوقيع: _________________________
        التاريخ: _________________________
        
        **المستأجر (الطرف الثاني):**
        
        الاسم: __________________________
        التوقيع: _________________________
        التاريخ: _________________________
        
        **الشهود:**
        
        1. الاسم: __________________________
           التوقيع: _________________________
        
        2. الاسم: __________________________
           التوقيع: _________________________
        """
        
        st.markdown(agreement_template)
        
        # خيارات تنزيل
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            if st.button("📥 تحميل كملف PDF", use_container_width=True):
                st.info("⏳ جاري تحضير ملف PDF... (هذه خاصية متقدمة تحتاج لإعدادات إضافية)")
        
        with col_dl2:
            if st.button("📄 نسخ إلى الحافظة", use_container_width=True):
                st.info("✅ تم نسخ نص العقد إلى الحافظة")
                # في الإصدار النهائي، نستخدم pyperclip أو مكتبة مشابهة
    
    def save_site_valuation(self, results, site_data):
        """حفظ نتائج التقييم الإيجاري"""
        
        valuation_data = {
            'site_data': site_data,
            'valuation_results': results,
            'valuation_date': datetime.now().isoformat(),
            'valuator': st.session_state.get('user_name', 'غير معروف'),
            'valuation_method': results.get('method', 'غير محدد')
        }
        
        # حفظ في الجلسة
        if 'site_valuations' not in st.session_state:
            st.session_state.site_valuations = []
        
        st.session_state.site_valuations.append(valuation_data)
    
    def render_rental_map(self):
        """عرض خريطة الإيجارات"""
        
        st.subheader("🗺️ خريطة الإيجارات في المنطقة")
        st.info("📍 هذه الخاصية تحت التطوير - ستظهر خريطة تفاعلية للإيجارات المشابهة")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # خريطة افتراضية
            st.markdown("""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; text-align: center; height: 400px; display: flex; align-items: center; justify-content: center;">
                <div>
                    <h3>📍 خريطة الإيجارات</h3>
                    <p>سيتم عرض مواقع الأراضي المؤجرة وأسعار الإيجار</p>
                    <p style="color: #666; margin-top: 20px;">
                        🚧 هذه الخاصية قيد التطوير<br>
                        ستتوفر في الإصدار القادم
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("🗺️ تصفية النتائج")
            
            city_filter = st.selectbox(
                "المدينة",
                ["الكل", "الرياض", "جدة", "الدمام", "مكة", "المدينة"]
            )
            
            site_type_filter = st.multiselect(
                "نوع الموقع",
                list(self.site_types.values())
            )
            
            rent_range = st.slider(
                "نطاق الإيجار (ريال/م²/سنة)",
                0, 500, (50, 200)
            )
            
            if st.button("🔍 تطبيق التصفية", use_container_width=True):
                st.success(f"تم تطبيق التصفية: {len(site_type_filter) if site_type_filter else 'الكل'}")
    
    def render_area_analysis(self):
        """تحليل المنطقة والإيجارات السائدة"""
        
        st.subheader("📊 تحليل منطقة الموقع")
        
        tab1, tab2, tab3 = st.tabs(["الإحصائيات", "الاتجاهات", "المقارنة"])
        
        with tab1:
            st.markdown("### 📈 إحصائيات الإيجارات")
            
            # بيانات افتراضية
            area_stats = {
                'المؤشر': ['متوسط الإيجار', 'أعلى إيجار', 'أقل إيجار', 'عدد المعاملات', 'متوسط المساحة'],
                'القيمة': ['85 ريال/م²', '120 ريال/م²', '60 ريال/م²', '42 معاملة', '1,250 م²'],
                'التغير': ['+3.2%', '+5.1%', '-1.8%', '+12%', '+2.5%']
            }
            
            st.table(pd.DataFrame(area_stats))
            
            st.markdown("### 🏘️ توزيع الأنواع")
            
            # رسم بياني افتراضي
            chart_data = pd.DataFrame({
                'نوع الموقع': ['سكني', 'تجاري', 'صناعي', 'زراعي', 'سياحي'],
                'نسبة السوق': [35, 25, 20, 15, 5],
                'متوسط الإيجار': [70, 95, 65, 40, 110]
            })
            
            st.dataframe(chart_data, use_container_width=True)
        
        with tab2:
            st.markdown("### 📅 اتجاهات السوق")
            
            # بيانات تاريخية افتراضية
            timeline_data = pd.DataFrame({
                'السنة': [2020, 2021, 2022, 2023, 2024],
                'متوسط الإيجار': [65, 70, 75, 80, 85],
                'عدد المعاملات': [28, 32, 35, 38, 42],
                'نمو القيمة': [0, 7.7, 7.1, 6.7, 6.3]
            })
            
            st.dataframe(timeline_data, use_container_width=True)
            
            st.info("""
            **ملاحظات الاتجاه:**
            - استقرار في نمو أسعار الإيجارات عند 6-8% سنوياً
            - زيادة في عدد المعاملات بنسبة 10% سنوياً
            - نمو الطلب على المواقع التجارية بنسبة 12% سنوياً
            """)
        
        with tab3:
            st.markdown("### ⚖️ مقارنة مع مناطق مجاورة")
            
            comparison_data = pd.DataFrame({
                'المنطقة': ['حي النخيل', 'حي العليا', 'حي السليمانية', 'حي الملك فهد', 'حي المروج'],
                'متوسط الإيجار': [85, 95, 75, 65, 90],
                'نسبة النمو': ['+6.3%', '+7.1%', '+5.8%', '+4.9%', '+6.8%'],
                'مستوى الخدمات': ['ممتاز', 'جيد جداً', 'جيد', 'متوسط', 'ممتاز'],
                'التقييم': ['⭐⭐⭐⭐☆', '⭐⭐⭐⭐☆', '⭐⭐⭐☆☆', '⭐⭐☆☆☆', '⭐⭐⭐⭐⭐']
            })
            
            st.dataframe(comparison_data, use_container_width=True)
            
            st.warning("""
            **تحذيرات هامة:**
            - الأسعار تختلف حسب مستوى الخدمات والموقع الدقيق
            - القيم المعروضة هي متوسطات وقد تختلف حسب المواقع الفردية
            - يفضل التحقق من المعاملات الفعلية في المنطقة
            """)
    
    def render_rental_reports(self):
        """عرض تقارير الإيجارات"""
        
        st.subheader("📑 تقارير الإيجارات المحفوظة")
        
        if 'site_valuations' not in st.session_state or not st.session_state.site_valuations:
            st.info("📭 لا توجد تقييمات محفوظة بعد. قم بإجراء تقييم أولاً.")
            return
        
        # عرض التقييمات المحفوظة
        for i, valuation in enumerate(st.session_state.site_valuations):
            with st.expander(f"تقرير #{i+1}: {valuation['site_data'].get('name', 'غير معروف')}", expanded=(i==0)):
                col_info, col_values = st.columns(2)
                
                with col_info:
                    st.write(f"""
                    **معلومات الموقع:**
                    - الاسم: {valuation['site_data'].get('name', 'غير معروف')}
                    - الموقع: {valuation['site_data'].get('city', '')} - {valuation['site_data'].get('district', '')}
                    - المساحة: {valuation['site_data'].get('area', 0):,.0f} م²
                    - النوع: {valuation['site_data'].get('type', 'غير محدد')}
                    - تاريخ التقييم: {valuation['valuation_date'][:10]}
                    """)
                
                with col_values:
                    results = valuation['valuation_results']
                    st.write(f"""
                    **نتائج التقييم:**
                    - الإيجار السنوي: {results.get('annual_rent', 0):,.0f} ريال
                    - الإيجار الشهري: {results.get('monthly_rent', 0):,.0f} ريال
                    - ريال/م²/سنة: {results.get('rent_per_m2', 0):,.1f}
                    - المنهجية: {valuation['valuation_method']}
                    - المقيم: {valuation.get('valuator', 'غير معروف')}
                    """)
                
                # أزرار التحكم
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button("📄 عرض التفاصيل", key=f"view_{i}"):
                        st.session_state.active_valuation = valuation
                        st.rerun()
                
                with col_btn2:
                    if st.button("📥 تصدير PDF", key=f"export_{i}"):
                        st.info("جاري تجهيز التقرير للتصدير...")
                
                with col_btn3:
                    if st.button("🗑️ حذف", key=f"delete_{i}"):
                        st.session_state.site_valuations.pop(i)
                        st.success("تم حذف التقرير")
                        st.rerun()
        
        # خيارات إضافية
        st.markdown("---")
        
        col_tools1, col_tools2, col_tools3 = st.columns(3)
        
        with col_tools1:
            if st.button("📊 تقرير إحصائي", use_container_width=True):
                self.generate_statistical_report()
        
        with col_tools2:
            if st.button("📈 تحليل السوق", use_container_width=True):
                self.generate_market_analysis()
        
        with col_tools3:
            if st.button("🧹 مسح الكل", use_container_width=True, type="secondary"):
                if st.session_state.site_valuations:
                    st.session_state.site_valuations = []
                    st.success("تم مسح جميع التقارير")
                    st.rerun()
    
    def generate_statistical_report(self):
        """توليد تقرير إحصائي"""
        
        if 'site_valuations' not in st.session_state or not st.session_state.site_valuations:
            st.warning("لا توجد بيانات كافية لتوليد تقرير إحصائي")
            return
        
        st.subheader("📊 التقرير الإحصائي")
        
        # جمع البيانات
        rents = [v['valuation_results'].get('annual_rent', 0) for v in st.session_state.site_valuations]
        areas = [v['site_data'].get('area', 0) for v in st.session_state.site_valuations]
        rent_per_m2 = [v['valuation_results'].get('rent_per_m2', 0) for v in st.session_state.site_valuations]
        
        # الإحصائيات
        stats_df = pd.DataFrame({
            'المؤشر': [
                'متوسط الإيجار السنوي',
                'أعلى إيجار سنوي',
                'أقل إيجار سنوي',
                'متوسط المساحة',
                'متوسط ريال/م²',
                'عدد التقييمات'
            ],
            'القيمة': [
                f"{np.mean(rents):,.0f} ريال",
                f"{np.max(rents):,.0f} ريال",
                f"{np.min(rents):,.0f} ريال",
                f"{np.mean(areas):,.0f} م²",
                f"{np.mean(rent_per_m2):,.1f} ريال",
                f"{len(rents)} تقييم"
            ]
        })
        
        st.table(stats_df)
        
        # توزيع المنهجيات
        methods = {}
        for v in st.session_state.site_valuations:
            method = v['valuation_method']
            methods[method] = methods.get(method, 0) + 1
        
        methods_df = pd.DataFrame({
            'المنهجية': list(methods.keys()),
            'عدد الاستخدامات': list(methods.values())
        })
        
        st.markdown("### 📋 توزيع المنهجيات المستخدمة")
        st.dataframe(methods_df, use_container_width=True)
    
    def generate_market_analysis(self):
        """توليد تحليل للسوق"""
        
        st.subheader("📈 تحليل سوق الإيجارات")
        
        # بيانات سوقية افتراضية
        market_analysis = {
            'العنصر': [
                'مستوى الطلب الحالي',
                'معدل الشغور',
                'متوسط فترة الإيجار',
                'معدل الزيادة السنوية',
                'العائد المتوقع',
                'مستوى المخاطرة'
            ],
            'التقييم': [
                'مرتفع',
                '12%',
                '5 سنوات',
                '5-7%',
                '8-10%',
                'متوسط'
            ],
            'التفسير': [
                'زيادة في طلب المستثمرين',
                'أعلى من المعدل الوطني (8%)',
                'فترة متوسطة تناسب الطرفين',
                'متوافقة مع التضخم',
                'جذاب للمستثمرين',
                'مقبول مع إدارة جيدة'
            ]
        }
        
        st.table(pd.DataFrame(market_analysis))
        
        st.info("""
        **توصيات السوق الحالية:**
        
        1. **للمالكين:**
           - استغل الطلب المرتفع لتحسين شروط الإيجار
           - فكر في عقود طويلة الأجل مع زيادات دورية
           - ركز على تحسين الخدمات لزيادة القيمة
        
        2. **للمستأجرين:**
           - ابحث عن مواقع بفترات سماح للسداد
           - تفاوض على شروط صيانة واضحة
           - اطلب خيار التجديد مسبقاً
        
        3. **للمستثمرين:**
           - المواقع التجارية تحقق أعلى عائد
           - المواقع السكنية أكثر استقراراً
           - استثمر في تحسين الخدمات لزيادة القيمة
        """)
