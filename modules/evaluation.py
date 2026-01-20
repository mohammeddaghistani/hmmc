import streamlit as st
import pandas as pd
import numpy as np
from modules.valuation_methods import apply_valuation_method

def render_evaluation_module(user_role):
    st.markdown('<div class="main-header"><h2>📊 التقييم العقاري العلمي (IVS)</h2></div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["🆕 تقييم جديد", "📊 البيانات المقارنة", "📈 تحليل الحساسية", "📑 التقارير"])

    with tab1: render_new_evaluation_form()
    with tab2: render_comparables_database()
    with tab3: render_sensitivity_analysis_tool()
    with tab4: st.info("استخدم قسم التقارير من القائمة الجانبية لتوليد ملفات PDF")

def render_new_evaluation_form():
    """نموذج التقييم الأصلي مع المعادلات الحقيقية"""
    with st.form("adv_eval"):
        c1, c2 = st.columns(2)
        with c1:
            addr = st.text_input("📍 عنوان العقار المراد تقييمه")
            area = st.number_input("📐 المساحة الإجمالية (م²)", value=1000.0)
        with c2:
            p_type = st.selectbox("🏠 نوع العقار", ["تجاري", "سكني", "صناعي"])
            method = st.selectbox("📊 منهجية التقييم", ["sales_comparison", "residual", "dcf"], 
                                  format_func=lambda x: {"sales_comparison": "مقارنة المبيعات", "residual": "القيمة المتبقية", "dcf": "التدفقات النقدية"}[x])
        
        if st.form_submit_button("🚀 بدء عملية التقييم العلمي"):
            res = apply_valuation_method(method, {'land_area': area, 'property_type': p_type}, {'comparable_properties': [], 'adjustments_matrix': {}})
            if res:
                st.success("✅ تم إكمال التقييم بنجاح وفقاً للمعايير الدولية")
                st.metric("القيمة التقديرية الإجمالية", f"{res.get('total_value', 0):,.0f} ريال")

def render_comparables_database():
    """تفعيل قاعدة بيانات العقارات المقارنة"""
    st.subheader("🗃️ قاعدة بيانات الصفقات المقارنة")
    # بيانات نموذجية للمقارنة (تُجلب من جدول deals مستقبلاً)
    data = {
        'رقم الصفقة': ['#101', '#102', '#103'],
        'المنطقة': ['الصحافة', 'الياسمين', 'النرجس'],
        'المساحة (م²)': [500, 750, 1000],
        'سعر المتر (ريال)': [1200, 1150, 1300],
        'تاريخ الصفقة': ['2024-01-10', '2023-12-15', '2024-01-05']
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

def render_sensitivity_analysis_tool():
    """تفعيل أداة تحليل الحساسية"""
    st.subheader("📈 تحليل حساسية القيمة")
    st.write("دراسة تأثير تغير العوامل (مثل سعر المتر أو معدل الإشغال) على القيمة النهائية.")
    factor = st.slider("نسبة التغير المتوقعة في سعر السوق %", -25, 25, 0)
    base_val = 1000000
    new_val = base_val * (1 + factor/100)
    st.write(f"القيمة الأساسية: {base_price:,.0f} ريال")
    st.markdown(f"**القيمة بعد التأثير:** :blue[{new_val:,.0f} ريال]")
