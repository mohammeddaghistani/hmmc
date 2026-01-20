import streamlit as st
from modules.db import get_setting, update_setting

def render_admin_panel(user_role):
    st.header("⚙️ إدارة معدلات النظام العامة")
    
    with st.form("settings_form"):
        st.subheader("📊 معاملات أنواع التأجير (Multipliers)")
        c1, c2 = st.columns(2)
        with c1:
            m_temp = st.number_input("معامل التأجير المؤقت", value=float(get_setting('mult_temporary', 0.85)))
            m_direct = st.number_input("معامل التأجير المباشر", value=float(get_setting('mult_direct', 1.25)))
        with col2:
            m_long = st.number_input("معامل الاستثمار طويل الأجل", value=float(get_setting('mult_long_term', 1.60)))
            m_exem = st.number_input("معامل المستثنى من المنافسة", value=float(get_setting('mult_exempt', 1.10)))
        
        st.divider()
        st.subheader("🏗️ معايير التقييم العلمي")
        c3, c4 = st.columns(2)
        with c3:
            cost = st.number_input("تكلفة البناء المعتمدة (ر/م²)", value=float(get_setting('construction_cost_m2', 3500)))
        with col4:
            yield_rate = st.number_input("معدل العائد المستهدف (Yield)", value=float(get_setting('default_yield', 0.08)))

        if st.form_submit_button("💾 حفظ كافة التعديلات"):
            update_setting('mult_temporary', m_temp)
            update_setting('mult_direct', m_direct)
            update_setting('mult_long_term', m_long)
            update_setting('mult_exempt', m_exem)
            update_setting('construction_cost_m2', cost)
            update_setting('default_yield', yield_rate)
            st.success("✅ تم تحديث كافة معدلات وقيم النظام بنجاح")
