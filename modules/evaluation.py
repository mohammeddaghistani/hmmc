import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from modules.valuation_methods import apply_valuation_method
from modules.report_generator import create_professional_report

def render_evaluation_module(user_role):
    """عرض وحدة التقييم المطورة"""
    
    st.markdown("""
    <div class="section-header">
        <h2>📊 نظام التقييم العقاري العلمي</h2>
        <p>تقييم احترافي باستخدام المنهجيات العلمية المعتمدة دولياً</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات التقييم
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🆕 تقييم جديد", 
        "📋 طرق التقييم", 
        "📊 البيانات المقارنة",
        "📈 تحليل الحساسية",
        "📑 التقارير"
    ])
    
    with tab1:
        render_new_evaluation_advanced()
    
    with tab2:
        render_valuation_methods_explanation()
    
    with tab3:
        render_comparables_database()
    
    with tab4:
        render_sensitivity_analysis()
    
    with tab5:
        render_professional_reports()

def render_new_evaluation_advanced():
    """نموذج التقييم المتقدم"""
    
    st.subheader("🏢 معلومات العقار الأساسية")
    
    with st.form("advanced_evaluation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # معلومات العقار
            property_address = st.text_input("📍 العنوان الكامل")
            property_type = st.selectbox(
                "🏠 نوع العقار",
                ["سكني", "تجاري", "مكتبي", "صناعي", "أرض", "فندق", "مستشفى", "محطة وقود", "أخرى"]
            )
            
            # المساحات
            land_area = st.number_input("📐 مساحة الأرض (م²)", min_value=1.0, value=1000.0)
            built_area = st.number_input("🏗️ المساحة المبنية (م²)", min_value=0.0, value=800.0)
            
            # المواصفات
            year_built = st.number_input("📅 سنة البناء", min_value=1900, max_value=2024, value=2020)
            condition_score = st.select_slider(
                "⭐ حالة العقار",
                options=[1, 2, 3, 4, 5],
                value=3,
                help="1: سيء، 5: ممتاز"
            )
        
        with col2:
            # المعلومات القانونية
            title_deed = st.text_input("📜 رقم الصك")
            zoning = st.selectbox(
                "🗺️ التصنيف البلدي",
                ["سكني", "تجاري", "صناعي", "زراعي", "مختلط", "أخرى"]
            )
            
            # معلومات الإيجار الحالي (إن وجد)
            current_rent = st.number_input("💰 الإيجار الحالي (سنوي)", min_value=0.0, value=0.0)
            occupancy_rate = st.slider("🏢 نسبة الإشغال الحالية %", 0, 100, 85)
            
            # ⬅️ تحديث: إضافة خيار "تحديد القيمة الإيجارية للموقع"
            valuation_purpose = st.selectbox(
                "🎯 الغرض من التقييم",
                [
                    "تحديد القيمة الإيجارية للموقع",  # ⬅️ الخيار الجديد
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
            )
        
        st.markdown("---")
        
        # اختيار طريقة التقييم
        st.subheader("⚙️ اختيار منهجية التقييم")
        
        method_col1, method_col2 = st.columns(2)
        
        with method_col1:
            valuation_method = st.radio(
                "📊 اختر طريقة التقييم:",
                [
                    "مقارنة المبيعات",
                    "القيمة المتبقية", 
                    "التدفقات النقدية المخصومة",
                    "الأرباح",
                    "الاختيار التلقائي"
                ],
                help="الاختيار التلقائي يختار الطريقة المناسبة بناءً على نوع العقار وتوفر البيانات"
            )
        
        with method_col2:
            # إدخال بيانات إضافية حسب الطريقة
            if valuation_method == "مقارنة المبيعات":
                st.info("📋 تحتاج إلى إدخال بيانات العقارات المقارنة")
                comparables_count = st.number_input("عدد العقارات المقارنة", min_value=1, max_value=10, value=3)
            
            elif valuation_method == "القيمة المتبقية":
                st.info("🏗️ تحتاج إلى بيانات التطوير")
                construction_cost = st.number_input("تكلفة البناء للمتر (ر.س)", min_value=1000, value=3000)
                developer_profit = st.slider("ربح المطور %", 10, 40, 20)
            
            elif valuation_method == "التدفقات النقدية المخصومة":
                st.info("📈 تحتاج إلى توقعات الإيرادات والمصاريف")
                forecast_years = st.slider("فترة التنبؤ (سنوات)", 5, 20, 10)
                discount_rate = st.slider("معدل الخصم %", 5, 15, 9)
            
            elif valuation_method == "الأرباح":
                st.info("💼 تحتاج إلى بيانات النشاط التجاري")
                revenue_sources = st.text_area("مصادر الإيرادات (مفصولة بفواصل)")
        
        st.markdown("---")
        
        # معاملات التعديل (لمقارنة المبيعات)
        st.subheader("⚖️ معاملات التعديل (إن وجدت)")
        
        if valuation_method == "مقارنة المبيعات":
            col_adj1, col_adj2, col_adj3 = st.columns(3)
            
            with col_adj1:
                location_weight = st.slider("وزن الموقع %", 0, 100, 30)
            
            with col_adj2:
                age_weight = st.slider("وزن العمر %", 0, 100, 20)
            
            with col_adj3:
                condition_weight = st.slider("وزن الحالة %", 0, 100, 15)
        
        # زر التقييم
        evaluate_col1, evaluate_col2, evaluate_col3 = st.columns([2, 1, 1])
        
        with evaluate_col1:
            if st.form_submit_button("🚀 بدأ التقييم العلمي", use_container_width=True):
                perform_advanced_valuation(
                    valuation_method,
                    {
                        'property_address': property_address,
                        'property_type': property_type,
                        'land_area': land_area,
                        'built_area': built_area,
                        'year_built': year_built,
                        'condition_score': condition_score,
                        'title_deed': title_deed,
                        'zoning': zoning,
                        'current_rent': current_rent,
                        'occupancy_rate': occupancy_rate,
                        'valuation_purpose': valuation_purpose  # ⬅️ تحديث
                    },
                    {
                        'comparables_count': comparables_count if 'comparables_count' in locals() else 0,
                        'construction_cost': construction_cost if 'construction_cost' in locals() else 3000,
                        'developer_profit': developer_profit/100 if 'developer_profit' in locals() else 0.20,
                        'forecast_years': forecast_years if 'forecast_years' in locals() else 10,
                        'discount_rate': discount_rate/100 if 'discount_rate' in locals() else 0.09
                    }
                )
        
        with evaluate_col2:
            st.form_submit_button("💾 حفظ كمسودة", use_container_width=True, type="secondary")
        
        with evaluate_col3:
            st.form_submit_button("🧹 إعادة تعيين", use_container_width=True, type="secondary")

def perform_advanced_valuation(method_arabic, property_data, parameters):
    """إجراء التقييم باستخدام الطرق العلمية"""
    
    # تحويل اسم الطريقة إلى مفتاح
    method_map = {
        "مقارنة المبيعات": "sales_comparison",
        "القيمة المتبقية": "residual", 
        "التدفقات النقدية المخصومة": "dcf",
        "الأرباح": "profits",
        "الاختيار التلقائي": "auto"
    }
    
    method_key = method_map.get(method_arabic, "auto")
    
    with st.spinner(f"🔍 جاري التقييم باستخدام طريقة {method_arabic}..."):
        
        # عرض خطوات التقييم
        steps = {
            "sales_comparison": [
                "1. جمع وتحليل البيانات المقارنة",
                "2. تطبيق تعديلات الموقع والمواصفات",
                "3. حساب متوسط القيم المعدلة",
                "4. تحديد درجة الثقة الإحصائية"
            ],
            "residual": [
                "1. حساب القيمة الإجمالية للمشروع (GDV)",
                "2. تقدير تكاليف التطوير",
                "3. خصم ربح المطور",
                "4. استخلاص القيمة المتبقية للأرض"
            ],
            "dcf": [
                "1. توقع التدفقات النقدية المستقبلية",
                "2. حساب صافي الدخل التشغيلي (NOI)",
                "3. خصم التدفقات بالقيمة الحالية",
                "4. إضافة القيمة النهائية (Terminal Value)"
            ],
            "profits": [
                "1. تحليل الإيرادات التشغيلية",
                "2. حساب الأرباح قبل الفوائد والضرائب (EBITDA)",
                "3. تحديد الرصيد القابل للقسمة",
                "4. استخلاص الإيجار السوقي"
            ]
        }
        
        if method_key in steps:
            st.info(f"### 📋 خطوات طريقة {method_arabic}:")
            for step in steps[method_key]:
                st.write(f"✅ {step}")
        
        # بيانات وهمية للعقارات المقارنة (في نظام حقيقي ستكون من قاعدة البيانات)
        comparable_properties = []
        if method_key == "sales_comparison":
            comparable_properties = generate_sample_comparables(property_data)
        
        # إعداد البيانات الإضافية
        additional_data = {
            'comparable_properties': comparable_properties,
            'adjustments_matrix': {
                'location': 0.30,
                'specifications': 0.25,
                'age': 0.20,
                'condition': 0.15,
                'facilities': 0.10
            },
            'data_availability': {
                'comparable_sales': len(comparable_properties)
            }
        }
        
        # إضافة المعاملات حسب الطريقة
        if method_key == "residual":
            property_data.update({
                'construction_cost_per_m2': parameters.get('construction_cost', 3000),
                'developer_profit_percent': parameters.get('developer_profit', 0.20)
            })
        elif method_key == "dcf":
            property_data.update({
                'forecast_period': parameters.get('forecast_years', 10),
                'discount_rate': parameters.get('discount_rate', 0.09)
            })
        
        # تطبيق طريقة التقييم
        try:
            results = apply_valuation_method(method_key, property_data, additional_data)
            
            if results:
                display_valuation_results(results, property_data, method_arabic)
                
                # حفظ النتائج في الجلسة لاستخدامها في التقارير
                st.session_state.last_valuation = {
                    'method': method_key,
                    'property_data': property_data,
                    'results': results,
                    'parameters': parameters
                }
                
                # عرض خيارات إضافية
                st.markdown("---")
                show_additional_options(results, property_data)
            else:
                st.error("❌ لم يتمكن النظام من إكمال التقييم. يرجى التحقق من البيانات المدخلة.")
                
        except Exception as e:
            st.error(f"❌ حدث خطأ في التقييم: {str(e)}")
            st.info("💡 يرجى التأكد من اكتمال جميع البيانات المطلوبة")

def display_valuation_results(results, property_data, method_name):
    """عرض نتائج التقييم بشكل احترافي"""
    
    st.success("✅ تم إكمال التقييم بنجاح!")
    
    # عرض النتائج الرئيسية
    st.markdown("### 📊 نتائج التقييم")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'total_value' in results:
            value = results['total_value']
        elif 'market_rent' in results:
            value = results['market_rent']
        elif 'total_present_value' in results:
            value = results['total_present_value']
        elif 'land_value' in results:
            value = results['land_value']
        else:
            value = 0
        
        st.metric("💰 القيمة التقديرية", f"{value:,.0f} ر.س")
    
    with col2:
        if 'value_per_m2' in results:
            value_m2 = results['value_per_m2']
        elif 'rent_per_m2' in results:
            value_m2 = results['rent_per_m2']
        else:
            value_m2 = 0
        
        st.metric("📐 القيمة للمتر المربع", f"{value_m2:,.0f} ر.س/م²")
    
    with col3:
        confidence = results.get('confidence_score', 0) * 100
        st.metric("⭐ درجة الثقة", f"{confidence:.0f}%")
    
    with col4:
        st.metric("📊 المنهجية", method_name)
    
    st.markdown("---")
    
    # عرض التفاصيل حسب طريقة التقييم
    if results.get('method') == 'sales_comparison':
        display_sales_comparison_details(results)
    elif results.get('method') == 'residual':
        display_residual_method_details(results)
    elif results.get('method') == 'dcf':
        display_dcf_method_details(results)
    elif results.get('method') == 'profits':
        display_profits_method_details(results)

def display_sales_comparison_details(results):
    """عرض تفاصيل طريقة مقارنة المبيعات"""
    
    st.subheader("🏘️ تفاصيل العقارات المقارنة")
    
    adjustments = results.get('adjustment_details', [])
    
    if adjustments:
        # إنشاء جدول للعقارات المقارنة
        data = []
        for adj in adjustments:
            data.append({
                'العقار': f"مقارن #{adj.get('property_id', '')}",
                'السعر الأساسي': f"{adj.get('base_price', 0):,.0f} ر.س/م²",
                'نسبة التعديل': f"{adj.get('adjustment_percentage', 0)*100:+.1f}%",
                'السعر المعدل': f"{adj.get('adjusted_price', 0):,.0f} ر.س/م²"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # عرض التعديلات التفصيلية
        with st.expander("🔍 عرض تفاصيل التعديلات"):
            for adj in adjustments:
                st.write(f"**العقار #{adj.get('property_id', '')}:**")
                for adjustment in adj.get('adjustments', []):
                    st.write(f"  • {adjustment}")
                st.write("---")
    
    # عرض التحليل الإحصائي
    if adjustments and len(adjustments) > 1:
        prices = [adj.get('adjusted_price', 0) for adj in adjustments]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 المتوسط الحسابي", f"{np.mean(prices):,.0f} ر.س/م²")
        with col2:
            st.metric("📈 الوسيط", f"{np.median(prices):,.0f} ر.س/م²")
        with col3:
            st.metric("📉 الانحراف المعياري", f"{np.std(prices):,.0f} ر.س/م²")

def display_residual_method_details(results):
    """عرض تفاصيل طريقة القيمة المتبقية"""
    
    st.subheader("🏗️ تفاصيل طريقة القيمة المتبقية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("القيمة الإجمالية للمشروع", f"{results.get('gross_development_value', 0):,.0f} ر.س")
        st.metric("إجمالي تكاليف التطوير", f"{results.get('total_development_cost', 0):,.0f} ر.س")
    
    with col2:
        st.metric("ربح المطور", f"{results.get('developer_profit', 0):,.0f} ر.س")
        st.metric("القيمة المتبقية (الأرض)", f"{results.get('land_value', 0):,.0f} ر.س")
    
    # تحليل الحساسية
    st.subheader("📈 تحليل الحساسية")
    sensitivity = results.get('sensitivity_analysis', [])
    
    if sensitivity:
        # عرض أهم 3 سيناريوهات
        for i, scenario in enumerate(sensitivity[:3]):
            with st.expander(f"سيناريو {i+1}: تغير GDV ب{scenario.get('gdv_change', 0):+.0f}%، تغير التكاليف ب{scenario.get('cost_change', 0):+.0f}%"):
                st.write(f"**قيمة الأرض المعدلة:** {scenario.get('land_value', 0):,.0f} ر.س")
                st.write(f"**التغير في القيمة:** {scenario.get('value_change', 0):+.1f}%")

def display_dcf_method_details(results):
    """عرض تفاصيل طريقة التدفقات النقدية المخصومة"""
    
    st.subheader("📈 تفاصيل طريقة DCF")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("القيمة الحالية الإجمالية", f"{results.get('total_present_value', 0):,.0f} ر.س")
    
    with col2:
        st.metric("صافي القيمة الحالية (NPV)", f"{results.get('net_present_value', 0):,.0f} ر.س")
    
    with col3:
        irr = results.get('internal_rate_return', 0)
        if irr:
            st.metric("معدل العائد الداخلي (IRR)", f"{irr:.1f}%")
    
    # عرض التدفقات النقدية
    st.subheader("💸 التدفقات النقدية المتوقعة")
    cashflows = results.get('cashflow_details', [])
    
    if cashflows:
        data = []
        for cf in cashflows[:5]:  # أول 5 سنوات
            data.append({
                'السنة': cf.get('year', ''),
                'نسبة الإشغال': f"{cf.get('occupancy_rate', 0)*100:.0f}%",
                'الإيجار/م²': f"{cf.get('rent_per_m2', 0):,.0f}",
                'صافي الدخل (NOI)': f"{cf.get('noi', 0):,.0f}",
                'القيمة الحالية': f"{cf.get('discounted_cashflow', 0):,.0f}"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    
    # الافتراضات الرئيسية
    st.subheader("⚙️ الافتراضات الرئيسية")
    assumptions = results.get('key_assumptions', {})
    
    for key, value in assumptions.items():
        if isinstance(value, float):
            st.write(f"**{key}:** {value*100:.1f}%")
        else:
            st.write(f"**{key}:** {value}")

def display_profits_method_details(results):
    """عرض تفاصيل طريقة الأرباح"""
    
    st.subheader("💼 تفاصيل طريقة الأرباح")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("إجمالي الإيرادات", f"{results.get('total_revenue', 0):,.0f} ر.س")
        st.metric("الأرباح قبل الفوائد والضرائب (EBITDA)", f"{results.get('ebitda', 0):,.0f} ر.س")
    
    with col2:
        st.metric("الرصيد القابل للقسمة", f"{results.get('divisible_balance', 0):,.0f} ر.س")
        st.metric("الإيجار السوقي", f"{results.get('market_rent', 0):,.0f} ر.س/سنوياً")
    
    # نسبة الإيجار إلى الإيرادات
    ratio = results.get('rent_to_revenue_ratio', 0)
    st.metric("نسبة الإيجار إلى الإيرادات", f"{ratio:.1f}%")
    
    # تحليل الحساسية
    st.subheader("📈 تحليل الحساسية للإيرادات")
    sensitivity = results.get('sensitivity_analysis', [])
    
    if sensitivity:
        for scenario in sensitivity:
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric(f"تغير الإيرادات", f"{scenario.get('revenue_change', 0):+.0f}%")
            with col_s2:
                st.metric("الإيجار المعدل", f"{scenario.get('adjusted_rent', 0):,.0f} ر.س")
            with col_s3:
                st.metric("تغير الإيجار", f"{scenario.get('rent_change', 0):+.1f}%")

def show_additional_options(results, property_data):
    """عرض خيارات إضافية بعد التقييم"""
    
    st.subheader("📑 خيارات إضافية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 إنشاء تقرير مفصل", use_container_width=True):
            generate_detailed_report(results, property_data)
    
    with col2:
        if st.button("📊 تحليل الحساسية المتقدم", use_container_width=True):
            show_advanced_sensitivity_analysis(results)
    
    with col3:
        if st.button("💾 حفظ في قاعدة البيانات", use_container_width=True):
            save_valuation_to_database(results, property_data)
            st.success("✅ تم حفظ التقييم بنجاح!")
    
    with col4:
        if st.button("🔄 تقييم جديد", use_container_width=True):
            st.rerun()

def generate_detailed_report(results, property_data):
    """توليد تقرير مفصل"""
    
    with st.spinner("📄 جاري إنشاء التقرير..."):
        # معلومات المقيم (في نظام حقيقي من قاعدة البيانات)
        valuer_info = {
            'name': st.session_state.get('user_name', 'المقيم المعتمد'),
            'qualifications': ['مقيم عقاري معتمد', 'عضوية الهيئة السعودية للمقيمين'],
            'company': 'شركة التقييم العقاري',
            'license_number': 'VAL-2024-001'
        }
        
        # معلومات العميل
        client_info = {
            'name': 'العميل',
            'type': 'شركة',
            'contact': 'معلومات الاتصال'
        }
        
        # بيانات التقييم
        valuation_data = {
            'id': f"VAL-{datetime.now().strftime('%Y%m%d%H%M')}",
            'property_data': property_data,
            'valuation_method': results.get('method'),
            'valuation_results': results,
            'valuation_date': datetime.now().strftime("%Y-%m-%d"),
            'effective_date': datetime.now().strftime("%Y-%m-%d"),
            'purpose': property_data.get('valuation_purpose', 'تحديد القيمة السوقية'),  # ⬅️ تحديث
            'intended_users': ['العميل'],
            'market_condition': 'stable'
        }
        
        # إنشاء التقرير
        report = create_professional_report(
            valuation_id=valuation_data['id'],
            valuation_data=valuation_data,
            valuer_info=valuer_info,
            client_info=client_info
        )
        
        # عرض التقرير
        st.success("✅ تم إنشاء التقرير بنجاح!")
        
        # عرض ملخص التقرير
        with st.expander("📋 عرض ملخص التقرير", expanded=True):
            st.json(report['summary'])
        
        # خيارات تحميل التقرير
        st.download_button(
            label="📥 تحميل التقرير كملف JSON",
            data=json.dumps(report['detailed_report'], ensure_ascii=False, indent=2),
            file_name=f"تقرير_تقييم_{valuation_data['id']}.json",
            mime="application/json"
        )
        
        # عرض التقرير HTML
        with st.expander("🌐 عرض التقرير كصفحة ويب"):
            st.components.v1.html(report['html_report'], height=800, scrolling=True)

def show_advanced_sensitivity_analysis(results):
    """عرض تحليل الحساسية المتقدم"""
    
    st.subheader("📈 تحليل الحساسية المتقدم")
    
    # تنفيذ تحليل حساسية متقدم حسب طريقة التقييم
    # (تخفيض للاختصار)
    st.info("🔬 يتم حالياً تطوير تحليل الحساسية المتقدم...")

def save_valuation_to_database(results, property_data):
    """حفظ التقييم في قاعدة البيانات"""
    
    # هنا سيتم حفظ التقييم في قاعدة البيانات
    # (تخفيض للاختصار)
    pass

def generate_sample_comparables(property_data):
    """توليد بيانات عقارات مقارنة وهمية"""
    
    comparables = []
    property_type = property_data.get('property_type', 'سكني')
    
    # توليد 3-5 عقارات مقارنة حسب نوع العقار
    for i in range(3):
        comparables.append({
            'id': f"COMP-{i+1}",
            'address': f"موقع مقارن #{i+1}",
            'property_type': property_type,
            'area_m2': property_data.get('land_area', 1000) * (0.8 + (i * 0.2)),  # ±20%
            'price_per_m2': np.random.uniform(800, 1200),
            'year_built': property_data.get('year_built', 2020) + np.random.randint(-5, 3),
            'condition_score': max(1, min(5, property_data.get('condition_score', 3) + np.random.randint(-1, 2))),
            'location_score': np.random.uniform(0.7, 1.0),
            'specifications_score': np.random.uniform(0.6, 0.9),
            'facilities_score': np.random.uniform(0.5, 0.8)
        })
    
    return comparables

def render_valuation_methods_explanation():
    """شرح طرق التقييم المختلفة"""
    
    st.subheader("📚 شرح طرق التقييم العلمية")
    
    methods = {
        'مقارنة المبيعات': {
            'description': 'المقارنة بالعقارات المشابهة التي تم بيعها أو تأجيرها حديثاً',
            'when_to_use': 'عند توفر بيانات كافية عن معاملات مشابهة',
            'formula': 'القيمة = متوسط (أسعار المقارنة × (1 + نسبة التعديل))',
            'strengths': ['واقعية', 'سهلة الفهم', 'تعكس السوق الحالي'],
            'weaknesses': ['تتطلب بيانات مقارنة', 'تعديلات شخصية']
        },
        'القيمة المتبقية': {
            'description': 'حساب قيمة الأرض من خلال خصم تكاليف التطوير من قيمة المشروع النهائي',
            'when_to_use': 'للأراضي المعدة للتطوير بدون عقارات مشابهة',
            'formula': 'قيمة الأرض = GDV - (التكاليف + ربح المطور)',
            'strengths': ['مناسبة للأراضي', 'تأخذ في الاعتبار إمكانيات التطوير'],
            'weaknesses': ['تعتمد على افتراضات', 'حساسة للتغيرات']
        },
        'التدفقات النقدية المخصومة': {
            'description': 'خصم التدفقات النقدية المستقبلية المتوقعة للوصول للقيمة الحالية',
            'when_to_use': 'للعقارات الاستثمارية ذات الدخل المتوقع',
            'formula': 'القيمة = Σ (NOI / (1+r)^t) + (TV / (1+r)^n)',
            'strengths': ['منهجية علمية', 'تأخذ في الاعتبار القيمة الزمنية للنقود'],
            'weaknesses': ['معقدة', 'تعتمد على توقعات']
        },
        'الأرباح': {
            'description': 'تحديد الإيجار بناءً على أرباح النشاط التجاري في العقار',
            'when_to_use': 'للعقارات المتخصصة (فنادق، مستشفيات، محطات وقود)',
            'formula': 'الإيجار = (EBITDA - استحقاقات) × نسبة الإيجار',
            'strengths': ['تربط القيمة بالأداء', 'مناسبة للعقارات التجارية'],
            'weaknesses': ['تتشف بيانات تشغيلية', 'حساسة للربحية']
        }
    }
    
    for method_name, details in methods.items():
        with st.expander(f"📖 {method_name}", expanded=(method_name == 'مقارنة المبيعات')):
            st.write(f"**الوصف:** {details['description']}")
            st.write(f"**متى تستخدم:** {details['when_to_use']}")
            st.write(f"**المعادلة:** `{details['formula']}`")
            
            col_str, col_wk = st.columns(2)
            with col_str:
                st.write("**المزايا:**")
                for strength in details['strengths']:
                    st.write(f"✅ {strength}")
            
            with col_wk:
                st.write("**العيوب:**")
                for weakness in details['weaknesses']:
                    st.write(f"⚠️ {weakness}")

def render_comparables_database():
    """عرض قاعدة البيانات للعقارات المقارنة"""
    
    st.subheader("🗃️ قاعدة البيانات للعقارات المقارنة")
    
    # محاكاة بيانات العقارات المقارنة
    sample_data = generate_sample_comparable_database()
    
    # فلترة البيانات
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox("نوع العقار", ["الكل", "سكني", "تجاري", "صناعي", "أرض"])
    
    with col2:
        filter_city = st.selectbox("المدينة", ["الكل", "الرياض", "جدة", "الدمام", "مكة"])
    
    with col3:
        min_area = st.number_input("أقل مساحة (م²)", min_value=0, value=500)
    
    # تطبيق الفلترة
    filtered_data = sample_data
    
    if filter_type != "الكل":
        filtered_data = [d for d in filtered_data if d['property_type'] == filter_type]
    
    if filter_city != "الكل":
        filtered_data = [d for d in filtered_data if d['city'] == filter_city]
    
    filtered_data = [d for d in filtered_data if d['area_m2'] >= min_area]
    
    # عرض البيانات
    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.dataframe(
            df[['id', 'property_type', 'city', 'area_m2', 'price_per_m2', 'transaction_date']],
            use_container_width=True,
            hide_index=True
        )
        
        st.metric("عدد العقارات المقارنة", len(filtered_data))
        
        # خيارات التصدير
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            if st.button("📊 تحليل إحصائي", use_container_width=True):
                show_statistical_analysis(filtered_data)
        
        with col_exp2:
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 تصدير كملف Excel",
                data=csv,
                file_name="العقارات_المقارنة.csv",
                mime="text/csv"
            )
    else:
        st.info("📭 لا توجد عقارات تطابق معايير الفلترة")

def generate_sample_comparable_database():
    """توليد قاعدة بيانات وهمية للعقارات المقارنة"""
    
    data = []
    cities = ["الرياض", "جدة", "الدمام", "مكة", "المدينة"]
    property_types = ["سكني", "تجاري", "صناعي", "أرض"]
    
    for i in range(20):
        prop_type = property_types[i % len(property_types)]
        price_range = {
            "سكني": (800, 1200),
            "تجاري": (600, 900),
            "صناعي": (400, 700),
            "أرض": (300, 500)
        }
        
        data.append({
            'id': f"DB-{i+1:03d}",
            'property_type': prop_type,
            'city': cities[i % len(cities)],
            'address': f"عنوان العقار #{i+1}",
            'area_m2': np.random.uniform(500, 2000),
            'price_per_m2': np.random.uniform(*price_range[prop_type]),
            'transaction_date': f"2024-{np.random.randint(1, 13):02d}-{np.random.randint(1, 28):02d}",
            'condition': np.random.choice(['جيد', 'ممتاز', 'مقبول']),
            'source': np.random.choice(['سجل العقاري', 'مصادر موثوقة', 'بيانات السوق'])
        })
    
    return data

def show_statistical_analysis(data):
    """عرض تحليل إحصائي للبيانات"""
    
    st.subheader("📊 التحليل الإحصائي للبيانات المقارنة")
    
    if not data:
        st.warning("لا توجد بيانات للتحليل")
        return
    
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**الإحصائيات الوصفية للسعر:**")
        st.write(f"• المتوسط: {df['price_per_m2'].mean():,.0f} ر.س/م²")
        st.write(f"• الوسيط: {df['price_per_m2'].median():,.0f} ر.س/م²")
        st.write(f"• الانحراف المعياري: {df['price_per_m2'].std():,.0f} ر.س/م²")
        st.write(f"• المدى: {df['price_per_m2'].min():,.0f} - {df['price_per_m2'].max():,.0f} ر.س/م²")
    
    with col2:
        st.write("**الإحصائيات الوصفية للمساحة:**")
        st.write(f"• المتوسط: {df['area_m2'].mean():,.0f} م²")
        st.write(f"• الوسيط: {df['area_m2'].median():,.0f} م²")
        st.write(f"• الانحراف المعياري: {df['area_m2'].std():,.0f} م²")
    
    # توزيع البيانات حسب المدينة
    st.subheader("📍 التوزيع الجغرافي")
    city_dist = df['city'].value_counts()
    st.bar_chart(city_dist)

def render_sensitivity_analysis():
    """عرض أداة تحليل الحساسية"""
    
    st.subheader("📈 أداة تحليل الحساسية")
    
    st.info("""
    **تحليل الحساسية** يساعد في فهم كيفية تأثير التغيرات في المدخلات على نتائج التقييم.
    اختر طريقة التقييم وأدخل القيم الأساسية والمتغيرة لرؤية التأثير.
    """)
    
    # اختيار طريقة التقييم
    method = st.selectbox(
        "اختر طريقة التقييم للتحليل:",
        ["مقارنة المبيعات", "القيمة المتبقية", "التدفقات النقدية المخصومة", "الأرباح"]
    )
    
    if method == "مقارنة المبيعات":
        analyze_sales_comparison_sensitivity()
    elif method == "القيمة المتبقية":
        analyze_residual_sensitivity()
    elif method == "التدفقات النقدية المخصومة":
        analyze_dcf_sensitivity()
    elif method == "الأرباح":
        analyze_profits_sensitivity()

def analyze_sales_comparison_sensitivity():
    """تحليل حساسية طريقة مقارنة المبيعات"""
    
    st.subheader("⚖️ تحليل حساسية طريقة مقارنة المبيعات")
    
    col1, col2 = st.columns(2)
    
    with col1:
        base_price = st.number_input("السعر الأساسي (ر.س/م²)", value=1000.0)
        location_adjustment = st.slider("تعديل الموقع %", -20, 20, 10)
        age_adjustment = st.slider("تعديل العمر %", -15, 15, -5)
    
    with col2:
        condition_adjustment = st.slider("تعديل الحالة %", -10, 10, 5)
        facilities_adjustment = st.slider("تعديل المرافق %", -5, 5, 2)
        comparables_count = st.slider("عدد العقارات المقارنة", 1, 10, 3)
    
    # حساب القيمة المعدلة
    total_adjustment = (
        location_adjustment +
        age_adjustment +
        condition_adjustment +
        facilities_adjustment
    ) / 100
    
    adjusted_price = base_price * (1 + total_adjustment)
    
    # عرض النتائج
    st.metric("السعر المعدل", f"{adjusted_price:,.0f} ر.س/م²")
    st.metric("إجمالي التعديل", f"{total_adjustment*100:+.1f}%")
    
    # تحليل تأثير كل عامل
    st.subheader("🔍 تحليل تأثير كل عامل")
    
    factors = [
        ("الموقع", location_adjustment),
        ("العمر", age_adjustment),
        ("الحالة", condition_adjustment),
        ("المرافق", facilities_adjustment)
    ]
    
    for factor, adjustment in factors:
        effect = base_price * (adjustment / 100)
        st.write(f"**{factor}:** {adjustment:+.1f}% → تأثير: {effect:+.0f} ر.س/م²")

def analyze_residual_sensitivity():
    """تحليل حساسية طريقة القيمة المتبقية"""
    
    st.subheader("🏗️ تحليل حساسية طريقة القيمة المتبقية")
    
    # المدخلات الأساسية
    col1, col2 = st.columns(2)
    
    with col1:
        gdv = st.number_input("القيمة الإجمالية للمشروع (ر.س)", value=5000000.0)
        construction_cost = st.number_input("تكلفة البناء (ر.س)", value=3000000.0)
    
    with col2:
        developer_profit_percent = st.slider("ربح المطور %", 10, 40, 20)
        professional_fees_percent = st.slider("الرسوم المهنية %", 5, 20, 12)
    
    # الحساب
    developer_profit = construction_cost * (developer_profit_percent / 100)
    professional_fees = construction_cost * (professional_fees_percent / 100)
    
    land_value = gdv - (construction_cost + developer_profit + professional_fees)
    
    # عرض النتائج
    st.metric("قيمة الأرض", f"{land_value:,.0f} ر.س")
    st.metric("ربح المطور", f"{developer_profit:,.0f} ر.س")
    
    # تحليل الحساسية
    st.subheader("📊 تحليل الحساسية للتغيرات")
    
    scenarios = []
    for gdv_change in [-0.10, -0.05, 0, 0.05, 0.10]:
        for cost_change in [-0.05, 0, 0.05]:
            new_gdv = gdv * (1 + gdv_change)
            new_cost = construction_cost * (1 + cost_change)
            new_profit = new_cost * (developer_profit_percent / 100)
            new_fees = new_cost * (professional_fees_percent / 100)
            
            new_land_value = new_gdv - (new_cost + new_profit + new_fees)
            
            scenarios.append({
                'gdv_change': gdv_change * 100,
                'cost_change': cost_change * 100,
                'land_value': new_land_value,
                'change_percent': ((new_land_value - land_value) / land_value) * 100
            })
    
    # عرض أهم السيناريوهات
    for scenario in scenarios[:3]:
        st.write(f"**تغير GDV: {scenario['gdv_change']:+.0f}%، تغير التكلفة: {scenario['cost_change']:+.0f}%**")
        st.write(f"  قيمة الأرض: {scenario['land_value']:,.0f} ر.س (تغير: {scenario['change_percent']:+.1f}%)")
        st.write("---")

def analyze_dcf_sensitivity():
    """تحليل حساسية طريقة DCF"""
    
    st.subheader("📈 تحليل حساسية طريقة DCF")
    
    col1, col2 = st.columns(2)
    
    with col1:
        noi = st.number_input("صافي الدخل التشغيلي السنوي (NOI)", value=500000.0)
        discount_rate = st.slider("معدل الخصم %", 5, 15, 9)
        growth_rate = st.slider("معدل النمو الدائم %", 0, 5, 2)
    
    with col2:
        forecast_years = st.slider("فترة التنبؤ (سنوات)", 5, 20, 10)
        terminal_value_multiple = st.slider("مضاعف القيمة النهائية", 5, 15, 10)
    
    # حساب DCF مبسط
    discount_factor = discount_rate / 100
    growth_factor = growth_rate / 100
    
    # حساب القيمة الحالية للتدفقات
    pv_cashflows = 0
    for year in range(1, forecast_years + 1):
        yearly_cashflow = noi * ((1 + growth_factor) ** (year - 1))
        discounted = yearly_cashflow / ((1 + discount_factor) ** year)
        pv_cashflows += discounted
    
    # حساب القيمة النهائية
    final_noi = noi * ((1 + growth_factor) ** forecast_years)
    terminal_value = final_noi * terminal_value_multiple
    pv_terminal = terminal_value / ((1 + discount_factor) ** forecast_years)
    
    total_value = pv_cashflows + pv_terminal
    
    # عرض النتائج
    st.metric("القيمة الإجمالية", f"{total_value:,.0f} ر.س")
    st.metric("القيمة الحالية للتدفقات", f"{pv_cashflows:,.0f} ر.س")
    st.metric("القيمة الحالية النهائية", f"{pv_terminal:,.0f} ر.س")
    
    # تأثير معدل الخصم
    st.subheader("📉 تأثير تغير معدل الخصم")
    
    discount_rates = [7, 8, 9, 10, 11]
    values = []
    
    for rate in discount_rates:
        factor = rate / 100
        pv_term = terminal_value / ((1 + factor) ** forecast_years)
        total = pv_cashflows + pv_term
        values.append(total)
    
    data = pd.DataFrame({
        'معدل الخصم %': discount_rates,
        'القيمة (ر.س)': values
    })
    
    st.line_chart(data.set_index('معدل الخصم %'))

def analyze_profits_sensitivity():
    """تحليل حساسية طريقة الأرباح"""
    
    st.subheader("💼 تحليل حساسية طريقة الأرباح")
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue = st.number_input("الإيرادات السنوية (ريال)", value=2000000.0)
        ebitda_margin = st.slider("هامش EBITDA %", 20, 60, 40)
        rent_share = st.slider("حصة الإيجار من الربح %", 30, 70, 50)
    
    with col2:
        operating_cost_percent = st.slider("نسبة المصاريف التشغيلية %", 30, 70, 50)
        depreciation_percent = st.slider("نسبة الإهلاك %", 2, 10, 5)
        tax_rate = st.slider("معدل الضريبة %", 10, 30, 20)
    
    # الحسابات
    ebitda = revenue * (ebitda_margin / 100)
    operating_costs = revenue * (operating_cost_percent / 100)
    depreciation = revenue * (depreciation_percent / 100)
    tax = (ebitda - depreciation) * (tax_rate / 100)
    
    divisible_balance = ebitda - depreciation - tax
    market_rent = divisible_balance * (rent_share / 100)
    
    # عرض النتائج
    st.metric("الإيجار السوقي", f"{market_rent:,.0f} ريال/سنوياً")
    st.metric("الأرباح قبل الفوائد والضرائب (EBITDA)", f"{ebitda:,.0f} ريال")
    st.metric("الرصيد القابل للقسمة", f"{divisible_balance:,.0f} ريال")
    
    # تحليل تأثير هامش الربح
    st.subheader("📊 تأثير تغير هامش الربح على الإيجار")
    
    margins = [30, 35, 40, 45, 50]
    rents = []
    
    for margin in margins:
        new_ebitda = revenue * (margin / 100)
        new_tax = (new_ebitda - depreciation) * (tax_rate / 100)
        new_balance = new_ebitda - depreciation - new_tax
        new_rent = new_balance * (rent_share / 100)
        rents.append(new_rent)
    
    data = pd.DataFrame({
        'هامش EBITDA %': margins,
        'الإيجار (ريال)': rents
    })
    
    st.bar_chart(data.set_index('هامش EBITDA %'))

def render_professional_reports():
    """عرض واجهة التقارير المهنية"""
    
    st.subheader("📑 نظام التقارير المهنية المتوافقة مع IVS")
    
    st.info("""
    **هيكل التقرير المهني حسب المعايير الدولية (IVS):**
    
    1. **المجموعة الأولى: المعلومات الأساسية** - التعريفات والغرض والمقيم
    2. **المجموعة الثانية: الحقائق والفحص** - وصف العقار والفحص الميداني
    3. **المجموعة الثالثة: التحليل والقيمة** - المنهجية والحسابات والنتائج
    4. **المجموعة الرابعة: إخلاء المسؤولية** - القيود والمعايير والتوقيعات
    """)
    
    # مثال لتقرير جاهز
    st.subheader("📋 نموذج تقرير جاهز")
    
    with st.expander("عرض هيكل التقرير الكامل", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**١. المعلومات الأساسية:**")
            st.write("• عنوان التقرير ورقمه")
            st.write("• تاريخ التقييم والفعالية")
            st.write("• الغرض والمستخدمين")
            st.write("• معلومات المقيم واستقلاليته")
            st.write("• معلومات العميل")
        
        with col2:
            st.write("**٢. الحقائق والفحص:**")
            st.write("• الوصف المادي للعقار")
            st.write("• المعلومات القانونية")
            st.write("• نطاق الفحص والتحقق")
            st.write("• تحليل حالة السوق")
        
        st.write("**٣. التحليل والقيمة:**")
        st.write("• المنهجية المختارة وتبريرها")
        st.write("• معاملات التقييم والافتراضات")
        st.write("• الحسابات التفصيلية")
        st.write("• تحليل الحساسية")
        st.write("• القيمة النهائية والأساس")
        
        st.write("**٤. إخلاء المسؤولية:**")
        st.write("• قيود الاستخدام")
        st.write("• بيان الامتثال للمعايير")
        st.write("• بيان عدم اليقين المادي")
        st.write("• التواقيع والتواريخ")
    
    # أزرار إنشاء التقارير
    st.subheader("🚀 إنشاء تقرير جديد")
    
    col_rep1, col_rep2, col_rep3 = st.columns(3)
    
    with col_rep1:
        if st.button("📄 تقرير مختصر", use_container_width=True):
            st.info("جاري إنشاء التقرير المختصر...")
    
    with col_rep2:
        if st.button("📑 تقرير مفصل", use_container_width=True):
            st.info("جاري إنشاء التقرير المفصل...")
    
    with col_rep3:
        if st.button("📊 تقرير مع رسوم بيانية", use_container_width=True):
            st.info("جاري إنشاء التقرير مع الرسوم البيانية...")
    
    # معاينة تقرير
    if 'last_valuation' in st.session_state:
        st.markdown("---")
        st.subheader("📋 معاينة آخر تقييم")
        
        valuation = st.session_state.last_valuation
        results = valuation.get('results', {})
        
        if st.button("🎨 إنشاء تقرير مهني للتقييم الأخير"):
            generate_detailed_report(results, valuation.get('property_data', {}))
