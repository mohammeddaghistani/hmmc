import streamlit as st
from modules.db import get_setting, update_setting

def render_admin_panel(user_role):
    st.header("⚙️ إدارة معدلات النظام العامة")
    
    # التأكد من وجود البيانات الافتراضية عند أول تشغيل
    current_mult_temp = get_setting('mult_temp', 0.85)
    current_mult_long = get_setting('mult_long', 1.60)
    current_cost = get_setting('construction_cost_m2', 3500)

    with st.form("settings_form"):
        st.subheader("📊 معاملات أنواع التأجير (Multipliers)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            m_temp = st.number_input(
                "معامل التأجير المؤقت", 
                value=float(current_mult_temp),
                format="%.2f"
            )
            
        with col2:
            m_long = st.number_input(
                "معامل الاستثمار طويل الأجل", 
                value=float(current_mult_long),
                format="%.2f"
            )
            
        cost = st.number_input(
            "تكلفة البناء المعتمدة (ر/م²)", 
            value=float(current_cost)
        )
        
        submitted = st.form_submit_button("💾 حفظ الإعدادات")
        
        if submitted:
            # تحديث القيم في قاعدة البيانات
            update_setting('mult_temp', m_temp)
            update_setting('mult_long', m_long)
            update_setting('construction_cost_m2', cost)
            
            st.success("✅ تم تحديث المعدلات بنجاح")
            # تنبيه المستخدم بضرورة إعادة التحميل لتطبيق التغييرات
            st.info("سيتم تطبيق المعدلات الجديدة في الحسابات القادمة.")
