# modules/mobile_ui.py
import streamlit as st

class MobileUI:
    def __init__(self):
        pass

    def render_sidebar_menu(self):
        """دالة تجريبية لعرض قائمة جانبية محسنة للجوال"""
        st.sidebar.markdown("### 📱 واجهة الجوال")
        return st.sidebar.radio("الانتقال إلى:", ["الرئيسية", "التقارير"])
