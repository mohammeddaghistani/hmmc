from fpdf import FPDF
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        try:
            # استخدام fpdf2 مع دعم Unicode
            self.add_font('DejaVu', '', 'assets/DejaVuSans.ttf', uni=True)
            self.set_font('DejaVu', '', 12)
        except Exception as e:
            st.error(f"⚠️ خطأ في تحميل الخط: {e}")

    def add_arabic_content(self, text):
        processed = fix_arabic(text)
        self.multi_cell(0, 10, txt=processed, align='R')

def render_report_module(role):
    st.subheader("📑 نظام التقارير")
    # ... كود عرض التقارير الأصلي
