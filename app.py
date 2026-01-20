import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# الوحدات النمطية
from modules.db import init_db, ensure_settings
from modules.auth import login_required, logout
from modules.dashboard import render_dashboard
from modules.style import apply_custom_style, get_custom_css
from modules.evaluation import render_evaluation_module
from modules.report import render_report_module
from modules.admin import render_admin_panel

# تطبيق التصميم المخصص
apply_custom_style()

# تهيئة حالة الجلسة
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

def main():
    """الدالة الرئيسية للتطبيق"""
    
    # تطبيق CSS المخصص
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # شريط العنوان مع الشعار
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <h1 class="app-title">🚀 نظام دعم قرار التقييم الإيجاري</h1>
            <p class="app-subtitle">نظام متكامل للتقييم والإدارة العقارية</p>
        </div>
        <div class="header-status">
            <span class="status-badge">📍 الرياض، المملكة العربية السعودية</span>
            <span class="status-badge">📅 {}</span>
        </div>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)
    
    # التحقق من المصادقة
    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_main_application()

def render_login_page():
    """عرض صفحة تسجيل الدخول"""
    
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <h2>🔐 تسجيل الدخول</h2>
                <p>الرجاء إدخال بيانات الدخول الخاصة بك</p>
            </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password = st.text_input("🔒 كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            
            login_button = st.form_submit_button("🚀 تسجيل الدخول", use_container_width=True)
            
            if login_button:
                user = login_required(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_role = user.get('role', 'guest')
                    st.session_state.user_name = user.get('name', 'مستخدم')
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    
    st.markdown("""
        </div>
        <div class="login-footer">
            <p class="hint-text">💡 للحصول على حساب، يرجى التواصل مع مسؤول النظام</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_main_application():
    """عرض التطبيق الرئيسي بعد المصادقة"""
    
    # شريط التنقل العلوي
    render_navigation_bar()
    
    # عرض المحتوى بناءً على الصفحة المختارة
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard':
        render_dashboard(st.session_state.user_role)
    elif page == 'evaluation':
        render_evaluation_module(st.session_state.user_role)
    elif page == 'reports':
        render_report_module(st.session_state.user_role)
    elif page == 'admin':
        render_admin_panel(st.session_state.user_role)
    elif page == 'profile':
        render_profile_page()

def render_navigation_bar():
    """شريط التنقل العلوي"""
    
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="user-info">
            <span class="user-role {st.session_state.user_role}">{st.session_state.user_role.upper()}</span>
            <span class="user-name">👋 مرحباً، {st.session_state.user_name}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # أزرار التنقل
    with col2:
        if st.button("📊 لوحة التحكم", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col3:
        if st.button("📈 التقييم", use_container_width=True):
            st.session_state.current_page = 'evaluation'
            st.rerun()
    
    with col4:
        if st.button("📑 التقارير", use_container_width=True):
            st.session_state.current_page = 'reports'
            st.rerun()
    
    with col5:
        if st.button("⚙️ الإعدادات", use_container_width=True):
            st.session_state.current_page = 'profile'
            st.rerun()
    
    with col6:
        if st.button("🚪 تسجيل الخروج", use_container_width=True, type="secondary"):
            logout()
            st.session_state.authenticated = False
            st.rerun()

def render_profile_page():
    """عرض صفحة الملف الشخصي"""
    
    st.markdown("""
    <div class="section-header">
        <h2>👤 الملف الشخصي والإعدادات</h2>
        <p>إدارة معلومات حسابك وإعدادات النظام</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="profile-card">
            <div class="profile-avatar">
                <span class="avatar-icon">👤</span>
            </div>
            <h3>{}</h3>
            <p class="role-badge">{}</p>
            <p class="profile-stats">📍 عضو منذ: يناير 2024</p>
        </div>
        """.format(st.session_state.user_name, st.session_state.user_role.upper()), 
        unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.subheader("🛠️ إعدادات الحساب")
            
            tabs = st.tabs(["معلوماتي", "الأمان", "التفضيلات"])
            
            with tabs[0]:
                with st.form("profile_form"):
                    name = st.text_input("الاسم الكامل", value=st.session_state.user_name)
                    email = st.text_input("البريد الإلكتروني", placeholder="example@domain.com")
                    phone = st.text_input("رقم الهاتف", placeholder="+966 5X XXX XXXX")
                    
                    if st.form_submit_button("💾 حفظ التغييرات"):
                        st.success("✅ تم حفظ التغييرات بنجاح")
            
            with tabs[1]:
                st.info("🔒 ميزات الأمان قريباً...")
            
            with tabs[2]:
                st.info("🎨 تخصيص الواجهة قريباً...")

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
