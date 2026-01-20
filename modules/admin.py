import streamlit as st
from modules.db import get_setting, update_setting

def render_admin_panel(user_role):
    st.header("⚙️ لوحة التحكم في معدلات النظام")
    
    with st.form("global_multipliers"):
        st.subheader("📊 معدلات أنواع التأجير (Multipliers)")
        c1, c2 = st.columns(2)
        with c1:
            m_temp = st.number_input("معامل التأجير المؤقت", value=float(get_setting('mult_temp', 0.85)))
            m_direct = st.number_input("معامل التأجير المباشر", value=float(get_setting('mult_direct', 1.25)))
        with c2:
            m_long = st.number_input("معامل الاستثمار طويل الأجل", value=float(get_setting('mult_long', 1.60)))
        
        st.divider()
        st.subheader("🏗️ قيم التقييم الأساسية")
        c3, c4 = st.columns(2)
        with c3:
            cost = st.number_input("تكلفة البناء المعتمدة (ر/م²)", value=float(get_setting('const_cost', 3500)))
        with c4:
            disc = st.number_input("معدل الخصم DCF %", value=float(get_setting('discount_rate', 0.10)))

        if st.form_submit_button("💾 حفظ كافة المعدلات وتحديث النظام"):
            update_setting('mult_temp', m_temp)
            update_setting('mult_long', m_long)
            update_setting('mult_direct', m_direct)
            update_setting('const_cost', cost)
            update_setting('discount_rate', disc)
            st.success("✅ تم تحديث كافة المعدلات برمجياً بنجاح")
