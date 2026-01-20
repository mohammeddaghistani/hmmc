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
    if not text:
        return ""
    # إعادة تشكيل الحروف (ربطها) ثم عكس الاتجاه (من اليمين لليسار)
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class PDFReport(FPDF):
    """فئة مخصصة لتوليد تقارير PDF تدعم العربية"""
    
    def header(self):
        # إضافة شعار (تأكد من وجود المجلد والصورة)
        try:
            self.image('assets/logo.png', 10, 8, 33)
        except:
            pass # يتخطى الشعار إذا لم يجد الملف
            
        # إضافة خط يدعم العربية (يجب توفر الملف في مجلد fonts)
        try:
            self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf')
            self.set_font('DejaVu', '', 16)
        except:
            self.set_font('Arial', 'B', 16)
            
        title = fix_arabic('تقرير التقييم العقاري')
        self.cell(0, 10, title, 0, 0, 'C')
        self.ln(20)
    
    def footer(self):
        self.set_y(-15)
        try:
            self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf')
            self.set_font('DejaVu', '', 8)
        except:
            self.set_font('Arial', 'I', 8)
            
        page_num = fix_arabic(f'الصفحة {self.page_no()}')
        self.cell(0, 10, page_num, 0, 0, 'C')
    
    def add_arabic_content(self, text):
        """إضافة نص عربي مع المعالجة"""
        try:
            self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf')
            self.set_font('DejaVu', '', 12)
        except:
            st.error("خطأ: لم يتم العثور على ملف الخط في fonts/DejaVuSans.ttf")
            return
            
        # تقسيم النص إلى أسطر ومعالجة كل سطر
        for line in text.split('\n'):
            processed_line = fix_arabic(line)
            self.multi_cell(0, 10, processed_line, align='R')

def render_report_module(user_role):
    """عرض وحدة التقارير"""
    
    st.markdown("""
    <div style="text-align: right; direction: rtl;">
        <h2>📑 نظام التقارير والإحصائيات</h2>
        <p>توليد تقارير احترافية وتحليلات مفصلة</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات التقارير
    tab1, tab2, tab3, tab4 = st.tabs(["📊 تقارير التقييم", "📈 إحصائيات", "🎯 تقارير مخصصة", "📤 تصدير البيانات"])
    
    with tab1:
        render_evaluation_reports()
    
    with tab2:
        render_statistics()
    
    with tab3:
        render_custom_reports()
    
    with tab4:
        render_export_options()

def render_evaluation_reports():
    """عرض تقارير التقييم"""
    
    st.subheader("📋 تقارير التقييمات المكتملة")
    
    # فلترة التقارير
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_type = st.selectbox(
            "نوع التقرير",
            ["جميع التقارير", "معلقة", "مكتملة", "ملغاة"]
        )
    
    with col2:
        date_from = st.date_input("من تاريخ")
    
    with col3:
        date_to = st.date_input("إلى تاريخ")
    
    # بيانات وهمية
    reports = [
        {
            "id": "REP-2024-001",
            "property": "حي النخيل - الرياض",
            "value": "450,000 ر.س",
            "confidence": "92%",
            "status": "مكتمل",
            "date": "2024-01-15",
            "prepared_by": "المقيّم أحمد"
        },
        {
            "id": "REP-2024-002",
            "property": "حي الياسمين - جدة",
            "value": "320,000 ر.س",
            "confidence": "85%",
            "status": "معلق",
            "date": "2024-01-14",
            "prepared_by": "المقيّم محمد"
        },
        {
            "id": "REP-2024-003",
            "property": "حي الربيع - الدمام",
            "value": "380,000 ر.س",
            "confidence": "88%",
            "status": "مكتمل",
            "date": "2024-01-13",
            "prepared_by": "المقيّم خالد"
        }
    ]
    
    # عرض التقارير
    for report in reports:
        with st.expander(f"📄 {report['id']} - {report['property']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💰 القيمة", report['value'])
            
            with col2:
                st.metric("⭐ الثقة", report['confidence'])
            
            with col3:
                status_color = "🟢" if report['status'] == "مكتمل" else "🟡"
                st.metric("📊 الحالة", f"{status_color} {report['status']}")
            
            st.caption(f"📅 التاريخ: {report['date']} | 👤 المعد: {report['prepared_by']}")
            
            col4, col5, col6 = st.columns(3)
            
            with col4:
                if st.button("📄 عرض التقرير", key=f"view_{report['id']}"):
                    generate_pdf_report(report)
            
            with col5:
                if st.button("📧 إرسال", key=f"send_{report['id']}"):
                    st.success(f"تم إرسال التقرير {report['id']}")
            
            with col6:
                if st.button("🗑️ حذف", key=f"delete_{report['id']}", type="secondary"):
                    st.warning(f"هل أنت متأكد من حذف التقرير {report['id']}?")

def generate_pdf_report(report_data):
    """توليد تقرير PDF مع حل مشاكل الترميز واللغة"""
    
    pdf = PDFReport()
    pdf.add_page()
    
    # محتوى التقرير
    content = f"""
تقرير التقييم العقاري
=====================

معلومات التقرير:
رقم التقرير: {report_data['id']}
العقار: {report_data['property']}
القيمة المقدرة: {report_data['value']}
درجة الثقة: {report_data['confidence']}
الحالة: {report_data['status']}
التاريخ: {report_data['date']}
المعد: {report_data['prepared_by']}

ملخص التقييم:
تم إجراء التقييم بناءً على منهجية علمية تعتمد على:
1. تحليل الصفقات المشابهة
2. دراسة السوق العقاري المحلي
3. تقييم حالة العقار وموقعه
4. تطبيق المعايير الاحترافية

التوصيات:
• القيمة المقدرة تعكس السوق الحالي
• درجة الثقة {report_data['confidence']} تشير إلى موثوقية عالية

التوقيع:
_________________________
مدير التقييم - نظام التقييم الإيجاري
    """
    
    pdf.add_arabic_content(content)
    
    # حل مشكلة encode('latin-1'):
    # في مكتبة fpdf2، تعيد دالة output() بيانات bytes مباشرة
    pdf_bytes = pdf.output()
    
    # إنشاء زر التحميل
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'''
    <div style="text-align: center; margin-top: 10px;">
        <a href="data:application/pdf;base64,{b64}" download="تقرير_تقييم_{report_data['id']}.pdf" 
           style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
           📥 تحميل التقرير (PDF)
        </a>
    </div>
    '''
    st.markdown(href, unsafe_allow_html=True)
    st.success("تم إنشاء التقرير بنجاح، يمكنك التحميل الآن.")

def render_statistics():
    """عرض الإحصائيات"""
    
    st.subheader("📈 إحصائيات وأداء النظام")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4>📊 توزيع التقييمات حسب النوع</h4>", unsafe_allow_html=True)
        
        data = {
            'النوع': ['سكني', 'تجاري', 'مكتبي', 'صناعي', 'أخرى'],
            'النسبة': [45, 25, 15, 10, 5]
        }
        df = pd.DataFrame(data)
        
        # تم استخدام px بنجاح هنا
        fig = px.pie(df, values='النسبة', names='النوع', 
                    color_discrete_sequence=px.colors.sequential.Blues)
        fig.update_layout(showlegend=True, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("<h4>📅 التقييمات خلال آخر 6 أشهر</h4>", unsafe_allow_html=True)
        
        months = ['يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
        evaluations = [120, 135, 150, 165, 180, 195]
        
        fig = px.bar(x=months, y=evaluations,
                    labels={'x': 'الشهر', 'y': 'عدد التقييمات'},
                    color=evaluations,
                    color_continuous_scale='Blues')
        
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    col3, col4, col5, col6 = st.columns(4)
    metrics = [
        ("🏢 إجمالي التقييمات", "1,245", "+12%"),
        ("⭐ متوسط الثقة", "87%", "+5%"),
        ("💰 متوسط القيمة", "425K", "+3%"),
        ("⏱️ متوسط وقت التقييم", "2.5 ساعة", "-15%")
    ]
    for col, (title, value, change) in zip([col3, col4, col5, col6], metrics):
        with col:
            st.metric(title, value, change)

def render_custom_reports():
    """عرض تقارير مخصصة"""
    st.subheader("🎯 تقارير مخصصة حسب المعايير")
    
    with st.form("custom_report_form"):
        st.info("🔍 حدد معايير التقرير المطلوب:")
        col1, col2 = st.columns(2)
        
        with col1:
            report_period = st.selectbox(
                "الفترة الزمنية",
                ["الأسبوع الحالي", "الشهر الحالي", "الربع الحالي", "السنة الحالية", "مخصص"]
            )
            property_types = st.multiselect(
                "أنواع العقارات",
                ["سكني", "تجاري", "مكتبي", "صناعي", "زراعي"],
                default=["سكني", "تجاري"]
            )
        
        with col2:
            cities = st.multiselect(
                "المدن",
                ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الشرقية"],
                default=["الرياض", "جدة"]
            )
            min_confidence = st.slider(
                "أقل درجة ثقة",
                0, 100, 70
            )
        
        st.markdown("---")
        col3, col4 = st.columns(2)
        with col3:
            output_format = st.radio("صيغة الملف", ["PDF", "Excel", "CSV", "HTML"])
        with col4:
            include_charts = st.checkbox("📊 تضمين الرسوم البيانية", value=True)
            include_details = st.checkbox("📋 تضمين التفاصيل الكاملة", value=True)
            
        col5, col6 = st.columns(2)
        with col5:
            generate = st.form_submit_button("🚀 توليد التقرير", use_container_width=True)
        with col6:
            preview = st.form_submit_button("👁️ معاينة قبل التوليد", use_container_width=True, type="secondary")
        
        if generate:
            st.success("✅ تم توليد التقرير بنجاح!")
            sample_data = {
                "المعيار": ["الفترة", "أنواع العقارات", "المدن", "درجة الثقة"],
                "القيمة": [report_period, ", ".join(property_types), ", ".join(cities), f"{min_confidence}%"]
            }
            st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

def render_export_options():
    """عرض خيارات تصدير البيانات"""
    st.subheader("📤 تصدير البيانات والإحصائيات")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📊 تصدير البيانات الخام (Excel/CSV)")
        st.button("تصدير الآن", key="export_raw")
    with col2:
        st.info("📈 تصدير تقارير الأداء (PDF/PPT)")
        st.button("تصدير الآن", key="export_stats")
    
    st.markdown("---")
    st.subheader("🕐 تصدير مجدول")
    col3, col4 = st.columns(2)
    with col3:
        st.selectbox("نوع الجدولة", ["يومي", "أسبوعي", "شهري"])
    with col4:
        st.time_input("وقت التصدير")
    st.text_input("المستلمون (البريد الإلكتروني)")
    st.button("✅ تفعيل الجدولة", use_container_width=True)
