import streamlit as st
import pandas as pd
from datetime import datetime
from modules.auth import check_permission

def render_admin_panel(user_role):
    """عرض لوحة الإدارة"""
    
    if not check_permission('admin'):
        st.error("⛔ ليس لديك صلاحية للوصول إلى لوحة الإدارة")
        return
    
    st.markdown("""
    <div class="section-header">
        <h2>⚙️ لوحة إدارة النظام</h2>
        <p>إدارة المستخدمين والإعدادات والنظام</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات الإدارة
    tab1, tab2, tab3, tab4 = st.tabs(["👥 إدارة المستخدمين", "⚙️ إعدادات النظام", "📊 قاعدة البيانات", "🔒 السجلات والأمان"])
    
    with tab1:
        render_user_management()
    
    with tab2:
        render_system_settings()
    
    with tab3:
        render_database_management()
    
    with tab4:
        render_security_logs()

def render_user_management():
    """إدارة المستخدمين"""
    
    st.subheader("👥 إدارة المستخدمين والأدوار")
    
    # عرض قائمة المستخدمين
    users = [
        {"id": 1, "username": "admin", "name": "المسؤول العام", "role": "admin", "status": "نشط", "last_login": "2024-01-15"},
        {"id": 2, "username": "committee1", "name": "لجنة المراجعة", "role": "committee", "status": "نشط", "last_login": "2024-01-14"},
        {"id": 3, "username": "valuer1", "name": "المقيّم أحمد", "role": "valuer", "status": "نشط", "last_login": "2024-01-13"},
        {"id": 4, "username": "dataentry1", "name": "مدخل البيانات", "role": "dataentry", "status": "غير نشط", "last_login": "2024-01-10"}
    ]
    
    df = pd.DataFrame(users)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    # إضافة مستخدم جديد
    st.subheader("➕ إضافة مستخدم جديد")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("اسم المستخدم")
            new_password = st.text_input("كلمة المرور", type="password")
            confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
        
        with col2:
            full_name = st.text_input("الاسم الكامل")
            user_role = st.selectbox("الدور", ["admin", "committee", "valuer", "dataentry"])
            user_email = st.text_input("البريد الإلكتروني")
        
        if st.form_submit_button("➕ إضافة مستخدم"):
            if new_password == confirm_password:
                st.success(f"✅ تم إضافة المستخدم {new_username} بنجاح")
            else:
                st.error("❌ كلمات المرور غير متطابقة")

def render_system_settings():
    """إعدادات النظام"""
    
    st.subheader("⚙️ إعدادات النظام العامة")
    
    with st.form("system_settings_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            system_name = st.text_input("اسم النظام", value="نظام التقييم الإيجاري")
            company_name = st.text_input("اسم الشركة", value="شركة التقييم العقاري")
            default_currency = st.selectbox("العملة الافتراضية", ["ريال سعودي", "دولار أمريكي", "يورو"])
        
        with col2:
            confidence_threshold = st.slider("حد الثقة الأدنى %", 0, 100, 70)
            max_similar_deals = st.number_input("أقصى عدد صفقات مشابهة", 1, 50, 10)
            auto_backup = st.checkbox("نسخ احتياطي تلقائي", value=True)
        
        st.markdown("---")
        
        # إعدادات التقارير
        st.subheader("📑 إعدادات التقارير")
        
        col3, col4 = st.columns(2)
        
        with col3:
            report_header = st.text_area("تذييل التقرير", "نظام التقييم الإيجاري - جميع الحقوق محفوظة")
            include_logo = st.checkbox("تضمين الشعار في التقارير", value=True)
        
        with col4:
            default_export_format = st.selectbox("صيغة التصدير الافتراضية", ["PDF", "Excel", "Word"])
            auto_generate_id = st.checkbox("توليد أرقام تلقائية", value=True)
        
        if st.form_submit_button("💾 حفظ الإعدادات"):
            st.success("✅ تم حفظ الإعدادات بنجاح")

def render_database_management():
    """إدارة قاعدة البيانات"""
    
    st.subheader("📊 إدارة قاعدة البيانات")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("حجم قاعدة البيانات", "245 MB")
    
    with col2:
        st.metric("عدد السجلات", "12,450")
    
    with col3:
        st.metric("آخر نسخة احتياطية", "اليوم 08:00")
    
    st.markdown("---")
    
    # إجراءات قاعدة البيانات
    st.subheader("🔧 إجراءات قاعدة البيانات")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if st.button("🔄 تحديث الإحصائيات", use_container_width=True):
            st.success("✅ تم تحديث إحصائيات قاعدة البيانات")
    
    with col5:
        if st.button("💾 نسخ احتياطي", use_container_width=True):
            st.success("✅ تم إنشاء نسخة احتياطية بنجاح")
    
    with col6:
        if st.button("🧹 تنظيف البيانات المؤقتة", use_container_width=True):
            st.warning("⚠️ هذا الإجراء سيزيل البيانات المؤقتة. هل أنت متأكد؟")
    
    st.markdown("---")
    
    # استعادة النسخ الاحتياطية
    st.subheader("🔄 استعادة النسخ الاحتياطية")
    
    backups = [
        {"name": "backup_20240115", "date": "2024-01-15 08:00", "size": "245 MB"},
        {"name": "backup_20240114", "date": "2024-01-14 08:00", "size": "242 MB"},
        {"name": "backup_20240113", "date": "2024-01-13 08:00", "size": "240 MB"}
    ]
    
    selected_backup = st.selectbox(
        "اختر نسخة احتياطية",
        backups,
        format_func=lambda x: f"{x['name']} - {x['date']} ({x['size']})"
    )
    
    if st.button("🔄 استعادة النسخة المحددة", type="secondary"):
        st.warning(f"⚠️ سيتم استعادة النسخة {selected_backup['name']}. هذا الإجراء لا يمكن التراجع عنه.")

def render_security_logs():
    """سجلات الأمان"""
    
    st.subheader("🔒 سجلات الأمان والنشاط")
    
    # الفلاتر
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_type = st.selectbox("نوع السجل", ["جميع السجلات", "تسجيل دخول", "تعديلات", "أخطاء"])
    
    with col2:
        log_date = st.date_input("التاريخ")
    
    with col3:
        log_user = st.text_input("اسم المستخدم")
    
    # عرض السجلات
    logs = [
        {"time": "2024-01-15 14:30", "user": "admin", "action": "تسجيل دخول", "ip": "192.168.1.100", "status": "ناجح"},
        {"time": "2024-01-15 14:25", "user": "valuer1", "action": "إضافة تقييم", "ip": "192.168.1.101", "status": "ناجح"},
        {"time": "2024-01-15 14:20", "user": "dataentry1", "action": "تعديل صفقة", "ip": "192.168.1.102", "status": "ناجح"},
        {"time": "2024-01-15 14:15", "user": "unknown", "action": "محاولة دخول", "ip": "10.0.0.1", "status": "فشل"}
    ]
    
    df_logs = pd.DataFrame(logs)
    st.dataframe(df_logs, use_container_width=True)
    
    st.markdown("---")
    
    # إحصائيات الأمان
    st.subheader("📊 إحصائيات الأمان")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.metric("محاولات الدخول الفاشلة", "3", "+1")
    
    with col5:
        st.metric("آخر تسجيل دخول", "قبل 5 دقائق")
    
    with col6:
        st.metric("المستخدمون النشطون", "3")
