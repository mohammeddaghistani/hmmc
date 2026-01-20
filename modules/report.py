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
    def __init__(self):
        super().__init__()
        try:
            # استخدام fpdf2 مع تفعيل Unicode وربط ملف الخط في مجلد assets
            self.add_font('DejaVu', '', 'assets/DejaVuSans.ttf', uni=True)
            self.set_font('DejaVu', '', 12)
        except Exception as e:
            st.error(f"⚠️ خطأ: تأكد من وجود ملف assets/DejaVuSans.ttf - {e}")

    def add_arabic_content(self, text):
        processed_text = fix_arabic(text)
        self.multi_cell(0, 10, txt=processed_text, align='R')

def render_report_module(user_role):
    st.markdown('<div class="main-header"><h2>📑 نظام التقارير والإحصائيات</h2></div>', unsafe_allow_html=True)
    # ... بقية كود عرض التقارير الأصلي مع استخدام PDFReport المطور ...
