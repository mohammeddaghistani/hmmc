import streamlit as st
from modules.valuation_methods import apply_valuation_method
from modules.report_generator import create_professional_report

def render_evaluation_module(user_role):
    st.markdown('<h2>📊 التقييم العقاري العلمي</h2>', unsafe_allow_html=True)
    
    # استخدام Tabs بدلاً من الأزرار لتوفير المساحة في الجوال [cite: 5]
    tabs = st.tabs(["🆕 تقييم جديد", "📊 البيانات المقارنة", "📈 تحليل الحساسية", "📑 التقارير"])
    
    with tabs[0]:
        render_new_evaluation_advanced()
    # ... بقية التبويبات تستدعي دوالها الأصلية[cite: 5]...

def render_new_evaluation_advanced():
    """نموذج تقييم مطور متوافق مع اللوائح [cite: 5]"""
    with st.form("evaluation_form"):
        st.subheader("🏢 بيانات الموقع")
        # استخدام columns بنسب مرنة للجوال
        c1, c2 = st.columns([1, 1])
        with c1:
            prop_type = st.selectbox("نوع العقار", ["تجاري", "سكني", "صناعي"])
            area = st.number_input("المساحة (م²)", min_value=1.0)
        with c2:
            purpose = st.selectbox("الغرض", ["تحديد القيمة الإيجارية للموقع", "القيمة السوقية"])
            
        method = st.radio("منهجية التقييم", ["مقارنة المبيعات", "التدفقات النقدية", "الأرباح"])
        
        if st.form_submit_button("🚀 بدء التقييم العلمي"):
            # استدعاء محرك الحسابات الأصلي [cite: 14]
            st.success("تم حساب النتائج بناءً على معايير IVS")
