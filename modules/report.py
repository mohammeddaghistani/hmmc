from fpdf import FPDF
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(text):
    """معالجة النصوص العربية للعرض الصحيح في PDF"""
    if not text: return ""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class PDFReport(FPDF):
    """فئة توليد PDF تدعم العربية والـ Unicode"""
    def __init__(self):
        super().__init__()
        try:
            # استخدام fpdf2 مع دعم Unicode وربط ملف الخط
            self.add_font('DejaVu', '', 'assets/DejaVuSans.ttf', uni=True)
            self.set_font('DejaVu', '', 12)
        except Exception as e:
            st.error(f"⚠️ خطأ في تحميل الخط العربي: {e}. تأكد من وجود assets/DejaVuSans.ttf")

    def add_arabic_content(self, text):
        """إضافة محتوى عربي مع معالجة الاتجاه"""
        self.set_font('DejaVu', '', 12)
        for line in text.split('\n'):
            processed = fix_arabic(line)
            self.multi_cell(0, 10, txt=processed, align='R')

def render_report_module(user_role):
    st.markdown('<div class="main-header"><h2>📑 نظام التقارير والإحصائيات</h2></div>', unsafe_allow_html=True)
    # ... كود التبويبات والتقارير الأصلي ...
