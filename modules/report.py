import plotly.express as px
import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display

# --- دالة مساعدة لمعالجة النصوص العربية ---
def fix_arabic(text):
    """تحويل النص العربي ليكون متوافقاً مع مكتبة FPDF (تشكيل وعكس الاتجاه)"""
    if not text:
        return ""
    # إعادة تشكيل الحروف (Shaping) ثم عكس الاتجاه (Bidi)
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class PDFReport(FPDF):
    """فئة مخصصة لتوليد تقارير PDF تدعم العربية والـ Unicode """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # إضافة خط يدعم العربية (يجب أن يكون في مجلد assets)
        try:
            self.add_font('DejaVu', '', 'assets/DejaVuSans.ttf', uni=True)
            self.set_font('DejaVu', '', 12)
        except Exception as e:
            st.error(f"⚠️ خطأ: ملف الخط غير موجود في assets/DejaVuSans.ttf - {e}")

    def header(self):
        """رأس الصفحة مع الشعار والعنوان """
        try:
            self.image('assets/logo.png', 10, 8, 33)
        except:
            pass 
        
        self.set_font('DejaVu', '', 16)
        title = fix_arabic('تقرير التقييم العقاري المهني')
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)

    def footer(self):
        """تذييل الصفحة مع رقم الصفحة """
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        page_num = fix_arabic(f'الصفحة {self.page_no()}')
        self.cell(0, 10, page_num, 0, 0, 'C')

    def add_arabic_content(self, text):
        """إضافة نصوص عربية متعددة الأسطر مع الحفاظ على التنسيق """
        self.set_font('DejaVu', '', 12)
        # تقسيم النص لأسطر ومعالجة كل سطر على حدة
        for line in text.split('\n'):
            if not line.strip():
                self.ln(5)
                continue
            processed_line = fix_arabic(line)
            self.multi_cell(w=0, h=10, txt=processed_line, align='R')

def render_report_module(user_role):
    """واجهة عرض التقارير في التطبيق """
    st.markdown('<div class="main-header"><h2>📑 نظام التقارير والإحصائيات المهنية</h2></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 تقارير التقييم", "📈 إحصائيات الأداء"])
    
    with tab1:
        st.subheader("📋 سجل التقارير المكتملة")
        # هنا يتم استعراض التقارير المخزنة في قاعدة البيانات
        # يمكن للمستخدم النقر على "عرض التقرير" لاستدعاء منطق PDFReport
