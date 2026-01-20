import streamlit as st
from modules.db import get_setting, update_setting

def render_admin_panel(user_role):
    st.header("⚙️ إدارة معدلات النظام العامة")
    with st.form("settings_form"):
        st.subheader("📊 معاملات أنواع التأجير (Multipliers)")
        m_temp = st.number_input("معامل التأجير المؤقت", value=float(get_setting('mult_temp', 0.85)))
        m_long = st.number_input("معامل الاستثمار طويل الأجل", value=float(get_setting('mult_long', 1.60)))
        cost = st.number_input("تكلفة البناء المعتمدة (ر/م²)", value=float(get_setting('construction_cost_m2', 3500)))
        
        if st.form_submit_button("💾 حفظ الإعدادات"):
            update_setting('mult_temp', m_temp)
            update_setting('mult_long', m_long)
            update_setting('construction_cost_m2', cost)
            st.success("✅ تم تحديث المعدلات بنجاح")
