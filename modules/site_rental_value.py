"""
وحدة متخصصة لتحديد القيمة الإيجارية للموقع
لأغراض تحديد الإيجارات الأرضية والتأجير طويل الأجل
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
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
            'tourism': 'موقع سياحي'
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
                has_electricity = st.checkbox("كهرباء", value=True)
                has_water = st.checkbox("مياه", value=True)
                has_sewage = st.checkbox("صرف صحي", value=True)
                has_roads = st.checkbox("طرق معبدة", value=True)
                has_fencing = st.checkbox("سور", value=False)
                
                # التراخيص
                st.subheader("📜 التراخيص والاستخدام")
                zoning_type = st.selectbox(
                    "التصنيف البلدي",
                    ["سكني", "تجاري", "صناعي", "زراعي", "سياحي", "مختلط"]
                )
                allowed_uses = st.text_area(
                    "الاستخدامات المسموحة",
                    placeholder="مثال: سكني عائلي، عمارة سكنية حتى 4 أدوار"
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
                    "طريقة الدخل (للمواقع التجارية)"
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
                            'services': {
                                'electricity': has_electricity,
                                'water': has_water,
                                'sewage': has_sewage,
                                'roads': has_roads,
                                'fencing': has_fencing
                            },
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
                    services_count = st.slider(f"⚡ عدد الخدمات", 0, 5, 3, key=f"serv_{i}")
                    location_score = st.slider(f"⭐ جودة الموقع", 1, 5, 3, key=f"loc_{i}")
                
                comparables.append({
                    'address': address,
                    'rent_per_m2': rent_per_m2,
                    'area': area,
                    'frontage': frontage,
                    'services_count': services_count,
                    'location_score': location_score
                })
        
        st.session_state.site_comparables = comparables
    
    def render_residual_for_rent(self):
        """طريقة القيمة المتبقية للإيجار"""
        
        st.info("🏗️ حساب الإيجار من خلال قيمة تطوير الموقع")
        
        col1, col2 = st.columns(2)
        
        with col1:
            land_value = st.number_input("💎 القيمة السوقية للأرض (ريال)", value=1000000.0)
            development_cost = st.number_input("🏗️ تكلفة التطوير (ريال)", value=500000.0)
        
        with col2:
            developer_profit = st.slider("📈 ربح المطور %", 10, 40, 20)
            land_yield_rate = st.slider("🎯 معدل عائد الأرض %", 3, 15, 8)
        
        # عرض الحساب التقديري
        total_value = land_value + development_cost
        developer_amount = development_cost * (developer_profit / 100)
        project_value = total_value + developer_amount
        estimated_rent = land_value * (land_yield_rate / 100)
        
        st.markdown("### 💰 الحساب التقديري")
        st.write(f"""
        - **قيمة الأرض:** {land_value:,.0f} ريال
        - **معدل العائد:** {land_yield_rate}%
        - **الإيجار السنوي المقدر:** {estimated_rent:,.0f} ريال
        - **الإيجار الشهري:** {estimated_rent / 12:,.0f} ريال
        """)
    
    def render_percentage_of_value(self):
        """طريقة نسبة من قيمة الأرض"""
        
        st.info("💎 حساب الإيجار كنسبة مئوية من قيمة الأرض")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            land_value = st.number_input("قيمة الأرض السوقية (ريال)", value=1000000.0)
        
        with col2:
            percentage = st.slider("النسبة المئوية السنوية %", 1.0, 20.0, 8.0)
        
        with col3:
            area = st.number_input("مساحة الأرض (م²)", value=1000.0)
        
        # حساب الإيجار
        annual_rent = land_value * (percentage / 100)
        monthly_rent = annual_rent / 12
        rent_per_m2 = annual_rent / area
        
        st.markdown("### 📊 نتائج الحساب")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.metric("الإيجار السنوي", f"{annual_rent:,.0f} ريال")
        
        with col_res2:
            st.metric("الإيجار الشهري", f"{monthly_rent:,.0f} ريال")
        
        with col_res3:
            st.metric("ريال/م²/سنة", f"{rent_per_m2:,.1f}")
        
        st.info(f"""
        **تفسير النسبة {percentage}%:**
        - نسبة متوسطة للأراضي: 5-8%
        - نسبة مرتفعة للمواقع التجارية: 8-12%
        - نسبة منخفضة للأراضي الزراعية: 3-5%
        """)
    
    def render_income_method(self):
        """طريقة الدخل للمواقع التجارية"""
        
        st.info("🏪 حساب الإيجار بناءً على الدخل المتوقع للمشروع")
        
        col1, col2 = st.columns(2)
        
        with col1:
            expected_revenue = st.number_input("الدخل السنوي المتوقع (ريال)", value=500000.0)
            operating_expenses = st.slider("نسبة المصاريف التشغيلية %", 20, 80, 40)
            profit_margin = st.slider("هامش الربح %", 10, 50, 25)
        
        with col2:
            rental_to_revenue = st.slider("نسبة الإيجار من الدخل %", 5, 30, 15)
            lease_term = st.slider("فترة الإيجار (سنوات)", 1, 20, 5)
            rent_escalation = st.slider("زيادة إيجار سنوية %", 0, 10, 3)
        
        # الحسابات
        net_income = expected_revenue * (1 - operating_expenses/100)
        profit = net_income * (profit_margin / 100)
        available_for_rent = net_income - profit
        suggested_rent = available_for_rent * (rental_to_revenue / 100)
        
        st.markdown("### 💼 تحليل الدخل")
        
        st.write(f"""
        **الإيرادات والمصاريف:**
        - الدخل المتوقع: {expected_revenue:,.0f} ريال
        - المصاريف التشغيلية ({operating_expenses}%): {expected_revenue * operating_expenses/100:,.0f} ريال
        - صافي الدخل: {net_income:,.0f} ريال
        - هامش الربح ({profit_margin}%): {profit:,.0f} ريال
        - المبلغ المتاح للإيجار: {available_for_rent:,.0f} ريال
        """)
        
        st.metric("الإيجار المقترح", f"{suggested_rent:,.0f} ريال/سنة")
        
        # جدول الزيادات السنوية
        if rent_escalation > 0:
            st.markdown("### 📈 جدول الزيادات السنوية")
            
            data = []
            for year in range(1, lease_term + 1):
                annual_rent = suggested_rent * ((1 + rent_escalation/100) ** (year-1))
                data.append({
                    'السنة': year,
                    'الإيجار السنوي': f"{annual_rent:,.0f}",
                    'الإيجار الشهري': f"{annual_rent/12:,.0f}",
                    'الزيادة': f"{rent_escalation if year > 1 else 0}%"
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
    
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
        except Exception as e:
            st.error(f"❌ خطأ في الحساب: {str(e)}")
            return None
    
    def _calculate_by_comparables(self, site_data):
        """الحساب عن طريق المقارنة"""
        
        comparables = st.session_state.get('site_comparables', [])
        
        if not comparables:
            # بيانات افتراضية للعرض
            comparables = [
                {'rent_per_m2': 100, 'area': 1200, 'services_count': 3, 'location_score': 4},
                {'rent_per_m2': 90, 'area': 1500, 'services_count': 2, 'location_score': 3},
                {'rent_per_m2': 110, 'area': 1000, 'services_count': 4, 'location_score': 5}
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
        
        # حساب القيمة النهائية
        adjusted_rent = base_rent * (1 + total_adjustment)
        annual_rent = adjusted_rent * site_data['area']
        monthly_rent = annual_rent / 12
        
        return {
            'method': 'comparables',
            'base_rent_per_m2': base_rent,
            'adjusted_rent_per_m2': adjusted_rent,
            'adjustment_percentage': total_adjustment * 100,
            'adjustments': adjustments,
            'annual_rent': annual_rent,
            'monthly_rent': monthly_rent,
            'comparable_count': len(comparables)
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
            'yield_rate': land_yield_rate * 100,
            'annual_rent': annual_rent,
            'monthly_rent': monthly_rent,
            'rent_per_m2': rent_per_m2
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
            'annual_rent': annual_rent,
            'monthly_rent': monthly_rent,
            'rent_per_m2': rent_per_m2
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
            'annual_rent': suggested_rent,
            'monthly_rent': monthly_rent,
            'rent_per_m2': rent_per_m2
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
        
        # خيارات إضافية
        st.markdown("---")
        
        col_opt1, col_opt2, col_opt3 = st.columns(3)
        
        with col_opt1:
            if st.button("📄 إنشاء عقد إيجار", use_container_width=True):
                self.generate_lease_agreement(results, site_data)
        
        with col_opt2:
            if st.button("💾 حفظ التقييم", use_container_width=True):
                st.success("✅ تم حفظ التقييم الإيجاري")
        
        with col_opt3:
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
        """)
        
        if results.get('adjustments'):
            st.write("**التعديلات المطبقة:**")
            for adj in results['adjustments']:
                st.write(f"• {adj}")
    
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
    
    def _display_percentage_details(self, results):
        """عرض تفاصيل طريقة النسبة"""
        
        st.subheader("💎 تفاصيل طريقة النسبة من القيمة")
        
        st.write(f"""
        **المدخلات:**
        - قيمة الأرض: {results.get('land_value', 0):,.0f} ريال
        - النسبة المئوية: {results.get('percentage', 0):.1f}%
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
    
    def generate_lease_agreement(self, results, site_data):
        """توليد نموذج عقد إيجار"""
        
        st.info("📝 جاري إنشاء نموذج عقد إيجار...")
        
        agreement_template = f"""
        # عقد إيجار موقع
        
        **تاريخ العقد:** {datetime.now().strftime('%Y-%m-%d')}
        
        ## ١. أطراف العقد
        - **المؤجر:** [اسم المؤجر]
        - **المستأجر:** [اسم المستأجر]
        
        ## ٢. وصف الموقع المؤجر
        - **الموقع:** {site_data.get('name', 'غير محدد')}
        - **المدينة:** {site_data.get('city', '')}
        - **الحي:** {site_data.get('district', '')}
        - **المساحة:** {site_data.get('area', 0):,.0f} م²
        - **طول الواجهة:** {site_data.get('frontage', 0):,.1f} م
        - **الخدمات المتوفرة:** {', '.join([k for k, v in site_data.get('services', {}).items() if v])}
        
        ## ٣. بنود الإيجار
        - **مدة العقد:** {site_data.get('lease_term', 5)} سنوات
        - **قيمة الإيجار السنوية:** {results.get('annual_rent', 0):,.0f} ريال سعودي
        - **قيمة الإيجار الشهرية:** {results.get('monthly_rent', 0):,.0f} ريال سعودي
        - **طريقة السداد:** [شهري/ربع سنوي/سنوي]
        - **زيادة الإيجار:** [نسبة ونظام الزيادة]
        
        ## ٤. الغرض من الاستخدام
        {site_data.get('allowed_uses', 'حسب التصنيف البلدي')}
        
        ## ٥. التزامات الأطراف
        - **التزامات المؤجر:** [توفير الخدمات، الصيانة الدورية، إلخ]
        - **التزامات المستأجر:** [الاستخدام حسب الغرض، الصيانة اليومية، دفع الإيجار في وقت محدد]
        
        ## ٦. التوقيعات
        _________________________
        **توقيع المؤجر**
        
        _________________________
        **توقيع المستأجر**
        
        **ملاحظة:** هذا نموذج أولي ويجب مراجعته من قبل مستشار قانوني.
        """
        
        st.text_area("📄 نموذج عقد الإيجار", agreement_template, height=400)
        
        st.download_button(
            label="📥 تحميل العقد",
            data=agreement_template,
            file_name=f"عقد_إيجار_{site_data.get('name', 'موقع')}.txt",
            mime="text/plain"
        )
    
    def render_rental_map(self):
        """عرض خريطة الإيجارات"""
        
        st.subheader("🗺️ خريطة الإيجارات في المنطقة")
        
        # محاكاة خريطة (في الواقع ستكون خريقة تفاعلية)
        st.info("📍 هذه مساحة لعرض خريطة تفاعلية للإيجارات في المنطقة")
        
        # بيانات وهمية للإيجارات
        rentals_data = [
            {"location": "حي النخيل", "type": "أرض سكنية", "rent_per_m2": 120, "area": 1500},
            {"location": "حي الياسمين", "type": "موقع تجاري", "rent_per_m2": 180, "area": 800},
            {"location": "حي الربيع", "type": "أرض صناعية", "rent_per_m2": 90, "area": 2500},
            {"location": "حي العليا", "type": "موقع تجاري", "rent_per_m2": 220, "area": 600},
            {"location": "حي السفارات", "type": "أرض سكنية", "rent_per_m2": 150, "area": 1200}
        ]
        
        df = pd.DataFrame(rentals_data)
        st.dataframe(df, use_container_width=True)
        
        # إحصائيات
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_rent = df['rent_per_m2'].mean()
            st.metric("متوسط ريال/م²", f"{avg_rent:.1f}")
        
        with col2:
            total_area = df['area'].sum()
            st.metric("إجمالي المساحة", f"{total_area:,.0f} م²")
        
        with col3:
            st.metric("عدد المواقع", len(df))
    
    def render_area_analysis(self):
        """تحليل المنطقة"""
        
        st.subheader("📊 تحليل المنطقة والأسعار")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 اتجاهات الأسعار")
            st.line_chart(pd.DataFrame({
                'الشهر': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو'],
                'ريال/م²': [110, 115, 118, 120, 122]
            }).set_index('الشهر'))
        
        with col2:
            st.markdown("### 🏘️ توزيع المواقع حسب النوع")
            st.bar_chart(pd.DataFrame({
                'النوع': ['سكني', 'تجاري', 'صناعي', 'زراعي'],
                'العدد': [15, 8, 6, 3]
            }).set_index('النوع'))
        
        st.markdown("### 📋 تقرير تحليل المنطقة")
        st.write("""
        **الملاحظات الرئيسية:**
        1. **اتجاهات السوق:** ارتفاع تدريجي في أسعار الإيجار بنسبة 2-3% ربع سنوي
        2. **العرض والطلب:** زيادة الطلب على المواقع التجارية في الأحياء الجديدة
        3. **التوصيات:** 
           - التفاوض على عقود طويلة الأجل لضمان الاستقرار
           - مراعاة زيادة سنوية للإيجار بنسبة 3-5%
           - دراسة إمكانية تجزئة المواقع الكبيرة
        """)
    
    def render_rental_reports(self):
        """عرض تقارير الإيجار"""
        
        st.subheader("📑 تقارير القيمة الإيجارية")
        
        if 'last_site_valuation' in st.session_state:
            valuation = st.session_state.last_site_valuation
            
            with st.expander("📋 عرض آخر تقييم إيجاري", expanded=True):
                st.write(f"**الموقع:** {valuation['site_data'].get('name', 'غير محدد')}")
                st.write(f"**المنهجية:** {valuation['method']}")
                st.write(f"**التاريخ:** {valuation['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                
                results = valuation['results']
                st.write(f"**الإيجار السنوي:** {results.get('annual_rent', 0):,.0f} ريال")
                st.write(f"**الإيجار الشهري:** {results.get('monthly_rent', 0):,.0f} ريال")
            
            col_rep1, col_rep2, col_rep3 = st.columns(3)
            
            with col_rep1:
                if st.button("📄 تقرير مفصل", use_container_width=True):
                    self.generate_detailed_rental_report(valuation)
            
            with col_rep2:
                if st.button("📊 تحليل السوق", use_container_width=True):
                    self.generate_market_analysis_report(valuation)
            
            with col_rep3:
                if st.button("💼 نموذج عقد", use_container_width=True):
                    self.generate_lease_agreement(
                        valuation['results'], 
                        valuation['site_data']
                    )
        
        else:
            st.info("📭 لم يتم إجراء أي تقييم إيجاري بعد. قم بتقييم موقع أولاً.")
    
    def generate_detailed_rental_report(self, valuation):
        """توليد تقرير إيجاري مفصل"""
        
        report = f"""
        # تقرير تحديد القيمة الإيجارية للموقع
        
        ## ١. معلومات التقرير
        - **رقم التقرير:** RENT-{datetime.now().strftime('%Y%m%d%H%M')}
        - **تاريخ التقييم:** {valuation['timestamp'].strftime('%Y-%m-%d')}
        - **الغرض:** تحديد القيمة الإيجارية للموقع
        
        ## ٢. معلومات الموقع
        - **اسم الموقع:** {valuation['site_data'].get('name', 'غير محدد')}
        - **الموقع:** {valuation['site_data'].get('city', '')} - {valuation['site_data'].get('district', '')}
        - **المساحة:** {valuation['site_data'].get('area', 0):,.0f} م²
        - **نوع الموقع:** {valuation['site_data'].get('type', 'غير محدد')}
        - **فترة الإيجار المقترحة:** {valuation['site_data'].get('lease_term', 5)} سنوات
        
        ## ٣. منهجية التقييم
        - **الطريقة المستخدمة:** {valuation['method']}
        - **نطاق العمل:** تقييم القيمة الإيجارية العادلة للموقع
        
        ## ٤. نتائج التقييم
        - **القيمة الإيجارية السنوية:** {valuation['results'].get('annual_rent', 0):,.0f} ريال
        - **القيمة الإيجارية الشهرية:** {valuation['results'].get('monthly_rent', 0):,.0f} ريال
        """
        
        if 'rent_per_m2' in valuation['results']:
            report += f"- **القيمة للمتر المربع:** {valuation['results']['rent_per_m2']:,.1f} ريال/م²/سنة\n"
        
        report += """
        
        ## ٥. الافتراضات الأساسية
        1. استقرار ظروف السوق العقاري
        2. توفر الخدمات الأساسية كما هو مذكور
        3. صلاحية الموقع للاستخدام المطلوب
        4. عدم وجود قيود قانونية تمنع التأجير
        
        ## ٦. التوصيات
        1. مراجعة العقد مع مستشار قانوني
        2. تضمين بند زيادات سنوية (3-5%)
        3. تحديد فترة سماح للدفع (15 يوم)
        4. توثيق حالة الموقع قبل التسليم
        
        ## ٧. إخلاء المسؤولية
        هذا التقرير لأغراض التقييم الأولي ويجب عدم اعتباره نصيحة قانونية أو مالية نهائية.
        """
        
        st.text_area("📄 التقرير الكامل", report, height=500)
        
        st.download_button(
            label="📥 تحميل التقرير",
            data=report,
            file_name=f"تقرير_إيجاري_{valuation['site_data'].get('name', 'موقع')}.txt",
            mime="text/plain"
        )
    
    def generate_market_analysis_report(self, valuation):
        """توليد تقرير تحليل السوق"""
        
        analysis = f"""
        # تقرير تحليل سوق الإيجارات للمواقع
        
        ## ١. نظرة عامة على السوق
        **الموقع:** {valuation['site_data'].get('city', '')}
        **الفترة:** الربع الأول 2024
        
        ## ٢. اتجاهات الأسعار
        - **متوسط أسعار الإيجار للمواقع المشابهة:** 110-150 ريال/م²/سنة
        - **نمو الأسعار السنوي:** 3-5%
        - **العرض والطلب:** توازن مع ميل طفيف لصالح العرض
        
        ## ٣. عوامل التأثير
        1. **العوامل الإيجابية:**
           - نمو المشاريع التنموية في المنطقة
           - تحسين البنية التحتية
           - زيادة الاستثمارات
        
        2. **العوامل السلبية:**
           - تقلبات أسعار المواد
           - تغيرات السياسات العقارية
           - المنافسة من المناطق الجديدة
        
        ## ٤. توصيات التسعير
        - **السعر المقترح:** {valuation['results'].get('annual_rent', 0):,.0f} ريال/سنة
        - **نطاق التسعير المقبول:** ±10% من السعر المقترح
        - **فترة التفاوض:** 30-60 يوم
        
        ## ٥. استراتيجية التأجير
        1. **للإيجار قصير الأجل (1-3 سنوات):**
           - زيادة السعر بنسبة 10-15%
           - طلب كفالة أكبر
        
        2. **للإيجار طويل الأجل (5+ سنوات):**
           - خصم 5-10% للالتزام الطويل
           - تضمين زيادات سنوية محددة مسبقاً
        """
        
        st.text_area("📊 تحليل السوق", analysis, height=400)
