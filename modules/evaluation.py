import streamlit as st
import pandas as pd
import numpy as np
from modules.valuation_methods import apply_valuation_method

def render_evaluation_module(user_role):
    st.markdown('<div class="main-header"><h2>📊 نظام التقييم العقاري العلمي</h2></div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🆕 تقييم جديد", "📊 البيانات المقارنة", "📈 تحليل الحساسية"])

    with tab1:
        render_new_valuation_form()
    with tab2:
        render_comparables_database_full()
    with tab3:
        render_sensitivity_tool_fixed()

def render_new_valuation_form():
    with st.form("adv_eval_form"):
        c1, c2 = st.columns(2)
        with c1:
            addr = st.text_input("📍 العنوان")
            area = st.number_input("📐 المساحة (م²)", value=1000.0)
        with c2:
            p_type = st.selectbox("🏠 نوع العقار", ["سكني", "تجاري", "صناعي"])
            method = st.selectbox("📊 المنهجية", ["sales_comparison", "residual", "dcf"], 
                                  format_func=lambda x: {"sales_comparison": "مقارنة المبيعات", "residual": "القيمة المتبقية", "dcf": "التدفقات النقدية"}[x])
        if st.form_submit_button("🚀 بدء التقييم العلمي"):
            res = apply_valuation_method(method, {'land_area': area, 'property_type': p_type, 'base_price': 1000}, {})
            st.success("✅ تم إكمال التقييم")
            st.metric("القيمة التقديرية", f"{res['total_value']:,.2f} ريال")

def render_comparables_database_full():
    st.subheader("🗃️ قاعدة بيانات الصفقات المقارنة")
    df = pd.DataFrame({'رقم الصفقة': ['#101', '#102'], 'المنطقة': ['النخيل', 'الياسمين'], 'سعر المتر': [1200, 1150]})
    st.dataframe(df, use_container_width=True)

def render_sensitivity_tool_fixed():
    st.subheader("📈 أداة تحليل الحساسية")
    base_val = st.number_input("القيمة الأساسية", value=1000000.0)
    factor = st.slider("نسبة التغير %", -25, 25, 0)
    new_val = base_val * (1 + factor/100)
    st.markdown(f"**القيمة بعد التأثير:** :blue[{new_val:,.2f} ريال]")
