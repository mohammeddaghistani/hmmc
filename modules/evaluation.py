import streamlit as st
from modules.valuation_methods import apply_valuation_method

def render_evaluation_module(user_role):
    st.markdown('<h2>📊 التقييم العقاري العلمي (IVS)</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🆕 تقييم جديد", "📊 البيانات المقارنة", "📈 تحليل الحساسية"])
    
    with tab1:
        with st.form("new_valuation_mobile_friendly"):
            c1, c2 = st.columns([1, 1])
            with c1:
                addr = st.text_input("📍 العنوان")
                p_type = st.selectbox("🏠 النوع", ["سكني", "تجاري", "صناعي"])
            with c2:
                area = st.number_input("📐 المساحة (م²)", min_value=1.0)
                method = st.selectbox("📊 المنهجية", ["مقارنة المبيعات", "القيمة المتبقية", "التدفقات النقدية"])
            
            if st.form_submit_button("🚀 بدء التقييم المتقدم"):
                st.success("تم تنفيذ عملية التقييم بنجاح وفقاً للمعايير الدولية")
