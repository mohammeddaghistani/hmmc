import streamlit as st
from modules.db import get_setting, update_setting

def render_admin_panel(user_role):
    st.header("⚙️ الإدارة وإعدادات النظام")
    
    tab1, tab2 = st.tabs(["👥 المستخدمين", "🎚️ إعدادات المعدلات والقيم"])
    
    with tab1:
        st.write("إدارة صلاحيات المستخدمين (أدمن، مقيم، لجنة)")

    with tab2:
        st.subheader("📊 التحكم في معدلات الضرب والمعادلات")
        with st.form("global_settings"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### معدلات أنواع التأجير")
                m_temp = st.number_input("معامل التأجير المؤقت", value=float(get_setting('mult_temporary', 0.85)))
                m_long = st.number_input("معامل الاستثمار طويل الأجل", value=float(get_setting('mult_long_term', 1.6)))
            with col2:
                st.markdown("##### إعدادات التقييم")
                const_cost = st.number_input("تكلفة البناء المعتمدة (ر/م²)", value=float(get_setting('construction_cost_m2', 3500)))
                discount = st.number_input("معدل الخصم الافتراضي (DCF)", value=float(get_setting('default_discount_rate', 0.10)))

            if st.form_submit_button("💾 حفظ الإعدادات العامة"):
                update_setting('mult_temporary', m_temp)
                update_setting('mult_long_term', m_long)
                update_setting('construction_cost_m2', const_cost)
                update_setting('default_discount_rate', discount)
                st.success("✅ تم تحديث كافة معدلات النظام بنجاح")
