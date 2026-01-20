import streamlit as st
from datetime import datetime
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# الوحدات النمطية
from modules.db import init_db, ensure_settings
from modules.auth import login_required, logout, register_user, get_all_users
from modules.dashboard import render_dashboard
from modules.style import apply_custom_style, get_custom_css, get_responsive_css
from modules.evaluation import render_evaluation_module
from modules.report import render_report_module
from modules.admin import render_admin_panel
from modules.site_rental_value import SiteRentalValuation
from modules.municipal_lease_types import MunicipalLeaseTypes
from modules.investment_committee import InvestmentCommitteeSystem
from modules.map_system import MapSystem
from modules.equation_manager import EquationManager
from modules.user_manager import UserManager
from modules.mobile_ui import MobileUI

# تهيئة التطبيق
st.set_page_config(
    page_title="نظام تأجير العقارات البلدية",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تطبيق التصميم المخصص
apply_custom_style()

# تهيئة حالة الجلسة
SESSION_DEFAULTS = {
    'authenticated': False,
    'user_role': None,
    'user_name': "",
    'user_id': None,
    'current_page': "dashboard",
    'selected_lease_type': None,
    'selected_subtype': None,
    'mobile_view': False,
    'dark_mode': False,
    'language': 'ar',
    'map_type': 'basic',
    'equations': {},
    'user_permissions': {}
}

for key, value in SESSION_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

def main():
    """الدالة الرئيسية للتطبيق"""
    
    # كشف نوع الجهاز
    detect_device_type()
    
    # تطبيق CSS متجاوب
    apply_responsive_design()
    
    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_main_application()

def detect_device_type():
    """كشف نوع الجهاز"""
    user_agent = st.get_option('browser.userAgent')
    mobile_keywords = ['Mobile', 'Android', 'iPhone', 'iPad']
    
    if any(keyword in user_agent for keyword in mobile_keywords):
        st.session_state.mobile_view = True
        st.session_state.sidebar_collapsed = True
    else:
        st.session_state.mobile_view = False

def apply_responsive_design():
    """تطبيق تصميم متجاوب"""
    responsive_css = get_responsive_css()
    custom_css = get_custom_css() + responsive_css
    
    if st.session_state.dark_mode:
        custom_css += """
        <style>
        body { background-color: #121212; color: #ffffff; }
        .stApp { background-color: #121212; }
        </style>
        """
    
    st.markdown(custom_css, unsafe_allow_html=True)

def render_login_page():
    """عرض صفحة تسجيل الدخول"""
    
    # خلفية متحركة للشاشة الرئيسية
    st.markdown("""
    <style>
    .login-background {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        width: 100%;
        max-width: 500px;
        text-align: center;
    }
    @media (max-width: 768px) {
        .login-card {
            padding: 30px 20px;
            margin: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-background">', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="login-card">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div style="font-size: 60px; margin-bottom: 20px;">🏛️</div>
                    <h1 style="color: #333; margin-bottom: 10px;">نظام العقارات البلدية</h1>
                    <p style="color: #666; margin-bottom: 30px;">تسجيل الدخول إلى النظام</p>
                </div>
            """, unsafe_allow_html=True)
            
            # تبويبات تسجيل الدخول / إنشاء حساب
            tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("👤 اسم المستخدم", 
                                           placeholder="أدخل اسم المستخدم",
                                           key="login_username")
                    password = st.text_input("🔒 كلمة المرور", 
                                           type="password",
                                           placeholder="أدخل كلمة المرور",
                                           key="login_password")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        remember_me = st.checkbox("تذكرني")
                    with col_btn2:
                        if st.form_submit_button("🚀 تسجيل الدخول", use_container_width=True):
                            user = login_required(username, password)
                            if user:
                                st.session_state.authenticated = True
                                st.session_state.user_role = user.get('role', 'user')
                                st.session_state.user_name = user.get('name', 'مستخدم')
                                st.session_state.user_id = user.get('id')
                                st.rerun()
                            else:
                                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            
            with tab2:
                with st.form("register_form"):
                    new_username = st.text_input("👤 اسم مستخدم جديد",
                                               placeholder="اختر اسم مستخدم")
                    new_password = st.text_input("🔒 كلمة مرور جديدة",
                                               type="password",
                                               placeholder="اختر كلمة مرور قوية")
                    confirm_password = st.text_input("✓ تأكيد كلمة المرور",
                                                   type="password",
                                                   placeholder="أعد إدخال كلمة المرور")
                    full_name = st.text_input("📝 الاسم الكامل",
                                            placeholder="الاسم الثلاثي")
                    email = st.text_input("📧 البريد الإلكتروني",
                                        placeholder="example@domain.com")
                    
                    if st.form_submit_button("📝 إنشاء حساب", use_container_width=True):
                        if new_password != confirm_password:
                            st.error("❌ كلمة المرور غير متطابقة")
                        else:
                            success = register_user(new_username, new_password, full_name, email)
                            if success:
                                st.success("✅ تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
                            else:
                                st.error("❌ فشل إنشاء الحساب. ربما اسم المستخدم موجود مسبقاً")
            
            st.markdown("""
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <p style="color: #666; font-size: 14px;">
                        💡 للحصول على صلاحيات إضافية، يرجى التواصل مع مدير النظام
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_main_application():
    """عرض التطبيق الرئيسي"""
    
    # شريط التنقل العلوي
    render_top_navigation()
    
    # الشريط الجانبي (يظهر في شاشات كبيرة)
    if not st.session_state.mobile_view:
        render_sidebar()
    
    # عرض المحتوى الرئيسي
    render_main_content()

def render_top_navigation():
    """شريط التنقل العلوي المتجاوب"""
    
    # CSS متخصص للشريط العلوي
    st.markdown("""
    <style>
    .top-nav {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 15px 20px;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    .nav-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .brand-text h1 {
        color: white;
        margin: 0;
        font-size: 1.5rem;
    }
    .brand-text p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        font-size: 0.9rem;
    }
    .nav-actions {
        display: flex;
        align-items: center;
        gap: 15px;
        flex-wrap: wrap;
    }
    .mobile-menu-btn {
        display: none;
    }
    @media (max-width: 768px) {
        .mobile-menu-btn {
            display: block;
        }
        .nav-actions {
            display: none;
        }
        .nav-content {
            justify-content: space-between;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="top-nav">
        <div class="nav-content">
            <div class="nav-brand">
                <div style="font-size: 32px;">🏛️</div>
                <div class="brand-text">
                    <h1>نظام العقارات البلدية</h1>
                    <p>الإصدار المتوافق مع اللوائح البلدية</p>
                </div>
            </div>
            
            <div class="nav-actions">
                <div style="display: flex; gap: 10px; align-items: center;">
                    <div style="color: white; background: rgba(255,255,255,0.1); padding: 8px 15px; border-radius: 20px;">
                        👤 {user_name} | {user_role}
                    </div>
                    <button onclick="window.location.href='?page=profile'" style="background: #4CAF50; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        الملف الشخصي
                    </button>
                    <button onclick="logout()" style="background: #f44336; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        تسجيل الخروج
                    </button>
                </div>
            </div>
            
            <div class="mobile-menu-btn">
                <button onclick="toggleMobileMenu()" style="background: none; border: none; color: white; font-size: 24px;">
                    ☰
                </button>
            </div>
        </div>
    </div>
    
    <script>
    function logout() {
        window.location.href = '?logout=true';
    }
    function toggleMobileMenu() {
        const menu = document.querySelector('.nav-actions');
        menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
    }
    </script>
    """.format(
        user_name=st.session_state.user_name,
        user_role=st.session_state.user_role
    ), unsafe_allow_html=True)
    
    # القائمة المنسدلة للموبايل
    if st.session_state.mobile_view:
        render_mobile_menu()

def render_mobile_menu():
    """قائمة الموبايل المنسدلة"""
    
    with st.expander("☰ القائمة", expanded=False):
        col1, col2 = st.columns(2)
        
        menu_items = [
            ("📊 لوحة التحكم", "dashboard"),
            ("📈 التقييم العقاري", "evaluation"),
            ("🏛️ أنواع التأجير", "lease_types"),
            ("👥 لجنة الاستثمار", "committee"),
            ("🗺️ الخرائط", "maps"),
            ("📑 التقارير", "reports"),
            ("⚙️ الإعدادات", "settings"),
            ("👑 لوحة التحكم", "admin" if st.session_state.user_role == "admin" else None)
        ]
        
        for i, (label, page) in enumerate(menu_items):
            if page:
                if i % 2 == 0:
                    with col1:
                        if st.button(label, use_container_width=True, key=f"mobile_{page}"):
                            st.session_state.current_page = page
                            st.rerun()
                else:
                    with col2:
                        if st.button(label, use_container_width=True, key=f"mobile_{page}"):
                            st.session_state.current_page = page
                            st.rerun()

def render_sidebar():
    """الشريط الجانبي للشاشات الكبيرة"""
    
    with st.sidebar:
        st.markdown("""
        <style>
        .sidebar-user {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
        }
        .user-avatar {
            font-size: 50px;
            margin-bottom: 10px;
        }
        .sidebar-nav button {
            width: 100%;
            margin: 5px 0;
            text-align: right;
            padding: 12px 20px;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .sidebar-nav button:hover {
            transform: translateX(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # معلومات المستخدم
        st.markdown(f"""
        <div class="sidebar-user">
            <div class="user-avatar">👤</div>
            <h3>{st.session_state.user_name}</h3>
            <p style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 20px; display: inline-block;">
                {st.session_state.user_role.upper()}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # التنقل
        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
        
        menu_options = [
            {"icon": "📊", "label": "لوحة التحكم", "page": "dashboard"},
            {"icon": "📈", "label": "التقييم العقاري", "page": "evaluation"},
            {"icon": "📍", "label": "القيمة الإيجارية", "page": "site_rental"},
            {"icon": "🏛️", "label": "أنواع التأجير", "page": "lease_types"},
            {"icon": "👥", "label": "لجنة الاستثمار", "page": "committee"},
            {"icon": "🗺️", "label": "الخرائط", "page": "maps"},
            {"icon": "📑", "label": "التقارير", "page": "reports"},
            {"icon": "⚙️", "label": "الإعدادات", "page": "settings"},
        ]
        
        if st.session_state.user_role == "admin":
            menu_options.append({"icon": "👑", "label": "لوحة التحكم", "page": "admin"})
        
        for option in menu_options:
            if st.button(f"{option['icon']} {option['label']}", 
                        use_container_width=True,
                        key=f"nav_{option['page']}"):
                st.session_state.current_page = option['page']
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # الإحصائيات السريعة
        st.markdown("---")
        st.markdown("### 📊 إحصائيات سريعة")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("العقود", "24", "+5")
        with col_stat2:
            st.metric("المستخدمين", "18", "+2")
        
        # تبديل الوضع الليلي
        dark_mode = st.toggle("🌙 الوضع الليلي", st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

def render_main_content():
    """عرض المحتوى الرئيسي"""
    
    # تحميل واجهة المستخدم المناسبة للجهاز
    if st.session_state.mobile_view:
        ui = MobileUI()
        ui.render_page(st.session_state.current_page)
    else:
        render_desktop_page()

def render_desktop_page():
    """عرض صفحة سطح المكتب"""
    
    page = st.session_state.current_page
    
    if page == 'dashboard':
        render_dashboard(st.session_state.user_role)
    elif page == 'evaluation':
        render_evaluation_module(st.session_state.user_role)
    elif page == 'site_rental':
        rental_valuator = SiteRentalValuation()
        rental_valuator.render_enhanced_valuation()
    elif page == 'lease_types':
        render_lease_types_page()
    elif page == 'committee':
        render_committee_page()
    elif page == 'maps':
        render_maps_page()
    elif page == 'reports':
        render_report_module(st.session_state.user_role)
    elif page == 'settings':
        render_settings_page()
    elif page == 'admin':
        render_admin_page()
    elif page == 'profile':
        render_profile_page()

def render_lease_types_page():
    """صفحة أنواع التأجير"""
    
    st.markdown("""
    <div class="page-header">
        <h1>🏛️ أنواع التأجير البلدية</h1>
        <p>اختر نوع التأجير المناسب حسب اللوائح البلدية</p>
    </div>
    """, unsafe_allow_html=True)
    
    lease_types = MunicipalLeaseTypes()
    
    # عرض الأنواع كبطاقات
    col1, col2 = st.columns(2)
    
    with col1:
        render_lease_type_card(
            "🎪 تأجير مؤقت",
            "للأنشطة المؤقتة (6 أشهر)",
            "المادة 3 من الضوابط",
            ["فعاليات", "مهرجانات", "أنشطة موسمية"],
            "TEMPORARY_ACTIVITY"
        )
        
        render_lease_type_card(
            "🎯 تأجير مباشر",
            "بعد إعلانات متكررة",
            "المادة 27 من اللائحة",
            ["حدائق عامة", "عقارات غير جذابة"],
            "DIRECT_LEASE"
        )
    
    with col2:
        render_lease_type_card(
            "🏗️ تأجير طويل الأجل",
            "مشاريع استثمارية",
            "المادة 21 من اللائحة",
            ["مبانٍ ثابتة", "مشاريع كبرى"],
            "LONG_TERM_INVESTMENT"
        )
        
        render_lease_type_card(
            "⚖️ عقارات مستثناة",
            "من المنافسة العامة",
            "المادة 10 من اللائحة",
            ["جهات حكومية", "مشاريع مبتكرة"],
            "EXEMPTED_FROM_COMPETITION"
        )

def render_lease_type_card(title, subtitle, regulation, features, lease_type):
    """عرض بطاقة نوع تأجير"""
    
    with st.container():
        st.markdown(f"""
        <div class="lease-card">
            <div class="lease-card-header">
                <h3>{title}</h3>
                <span class="regulation-badge">{regulation}</span>
            </div>
            <p class="lease-subtitle">{subtitle}</p>
            <div class="lease-features">
                {"".join([f'<span class="feature-tag">{feature}</span>' for feature in features])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"اختيار {title}", key=f"select_{lease_type}", use_container_width=True):
            st.session_state.selected_lease_type = lease_type
            st.success(f"تم اختيار {title}")

def render_committee_page():
    """صفحة لجنة الاستثمار"""
    
    st.markdown("""
    <div class="page-header">
        <h1>👥 لجنة الاستثمار البلدية</h1>
        <p>إدارة لجان الاستثمار واتخاذ القرارات</p>
    </div>
    """, unsafe_allow_html=True)
    
    committee_system = InvestmentCommitteeSystem()
    
    # تبويبات الصفحة
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 تشكيل اللجنة",
        "💰 تحديد القيم",
        "📊 القرارات",
        "📈 الإحصائيات"
    ])
    
    with tab1:
        render_committee_formation(committee_system)
    
    with tab2:
        render_rental_valuation(committee_system)
    
    with tab3:
        render_committee_decisions()
    
    with tab4:
        render_committee_statistics()

def render_maps_page():
    """صفحة الخرائط"""
    
    st.markdown("""
    <div class="page-header">
        <h1>🗺️ نظام الخرائط العقارية</h1>
        <p>عرض وتحليل المواقع العقارية على الخرائط</p>
    </div>
    """, unsafe_allow_html=True)
    
    map_system = MapSystem()
    
    # اختيار نوع الخريطة
    col1, col2 = st.columns([3, 1])
    
    with col1:
        map_type = st.radio(
            "نوع الخريطة:",
            ["🗺️ خريطة أساسية", "🛰️ خريطة ستلايت", "🌆 خريطة هجينة"],
            horizontal=True
        )
        
        # تحويل إلى نوع الخريطة الداخلي
        map_type_dict = {
            "🗺️ خريطة أساسية": "basic",
            "🛰️ خريطة ستلايت": "satellite",
            "🌆 خريطة هجينة": "hybrid"
        }
        
        st.session_state.map_type = map_type_dict.get(map_type, "basic")
    
    with col2:
        # خيارات إضافية
        show_markers = st.checkbox("عرض العلامات", value=True)
        show_heatmap = st.checkbox("خريطة الحرارة", value=False)
    
    # عرض الخريطة
    map_system.render_map(
        map_type=st.session_state.map_type,
        show_markers=show_markers,
        show_heatmap=show_heatmap
    )
    
    # تحكمات الخريطة
    with st.expander("🎮 تحكمات الخريطة المتقدمة", expanded=False):
        col_control1, col_control2, col_control3 = st.columns(3)
        
        with col_control1:
            zoom_level = st.slider("مستوى التكبير", 1, 20, 12)
        
        with col_control2:
            center_lat = st.number_input("خط العرض", value=24.7136)
        
        with col_control3:
            center_lng = st.number_input("خط الطول", value=46.6753)
        
        if st.button("تطبيق الإعدادات"):
            map_system.update_map(center_lat, center_lng, zoom_level)
            st.rerun()

def render_settings_page():
    """صفحة إعدادات النظام"""
    
    st.markdown("""
    <div class="page-header">
        <h1>⚙️ إعدادات النظام</h1>
        <p>تخصيص النظام حسب احتياجاتك</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات الإعدادات
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 الحساب",
        "🌍 اللغة والمظهر",
        "📊 التقييم",
        "🔐 الأمان",
        "📱 الجهاز"
    ])
    
    with tab1:
        render_account_settings()
    
    with tab2:
        render_appearance_settings()
    
    with tab3:
        render_evaluation_settings()
    
    with tab4:
        render_security_settings()
    
    with tab5:
        render_device_settings()

def render_account_settings():
    """إعدادات الحساب"""
    
    with st.form("account_settings_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("الاسم الكامل", value=st.session_state.user_name)
            email = st.text_input("البريد الإلكتروني", placeholder="example@domain.com")
            phone = st.text_input("رقم الهاتف", placeholder="+966 XXXXXXXX")
        
        with col2:
            department = st.selectbox("القسم", ["التقييم", "الإدارة", "المالية", "التخطيط"])
            position = st.text_input("المنصب", placeholder="مدير قسم")
            notification_email = st.checkbox("إشعارات البريد الإلكتروني", value=True)
            notification_sms = st.checkbox("إشعارات SMS", value=False)
        
        if st.form_submit_button("💾 حفظ التغييرات", use_container_width=True):
            st.success("✅ تم حفظ إعدادات الحساب")

def render_appearance_settings():
    """إعدادات المظهر"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox("اللغة", ["العربية", "الإنجليزية"], index=0)
        theme = st.selectbox("السمة", ["فاتحة", "داكنة", "تلقائية"])
        font_size = st.select_slider("حجم الخط", ["صغير", "متوسط", "كبير", "كبير جداً"], value="متوسط")
        density = st.select_slider("كثافة الواجهة", ["مضغوط", "عادي", "مريح"], value="عادي")
    
    with col2:
        primary_color = st.color_picker("اللون الأساسي", "#1e3c72")
        secondary_color = st.color_picker("اللون الثانوي", "#2a5298")
        roundness = st.slider("دائرة الزوايا", 0, 20, 8)
        animations = st.checkbox("الحركات", value=True)
    
    if st.button("🎨 تطبيق المظهر", use_container_width=True):
        st.success("✅ تم تطبيق إعدادات المظهر")

def render_evaluation_settings():
    """إعدادات التقييم"""
    
    equation_manager = EquationManager()
    
    st.markdown("### 📊 معادلات التقييم")
    
    # معادلات التقييم العقاري
    equations = equation_manager.get_all_equations()
    
    for eq_type, eq_data in equations.items():
        with st.expander(f"📐 معادلات {eq_data['name']}", expanded=False):
            for eq_name, eq_formula in eq_data['equations'].items():
                col_eq1, col_eq2, col_eq3 = st.columns([3, 1, 1])
                
                with col_eq1:
                    st.code(eq_formula, language="python")
                
                with col_eq2:
                    if st.button("تعديل", key=f"edit_{eq_type}_{eq_name}"):
                        st.session_state.editing_equation = f"{eq_type}_{eq_name}"
                
                with col_eq3:
                    if st.button("اختبار", key=f"test_{eq_type}_{eq_name}"):
                        st.info("جاري اختبار المعادلة...")
    
    # إضافة معادلة جديدة
    with st.form("new_equation_form"):
        st.markdown("### ➕ إضافة معادلة جديدة")
        
        eq_name = st.text_input("اسم المعادلة")
        eq_type = st.selectbox("نوع المعادلة", ["تقييم عقاري", "إيجار", "استثمار"])
        eq_formula = st.text_area("صيغة المعادلة (Python)")
        
        if st.form_submit_button("➕ إضافة معادلة", use_container_width=True):
            if eq_name and eq_formula:
                equation_manager.add_equation(eq_type, eq_name, eq_formula)
                st.success("✅ تمت إضافة المعادلة")

def render_security_settings():
    """إعدادات الأمان"""
    
    st.markdown("### 🔐 أمان الحساب")
    
    with st.form("security_form"):
        current_password = st.text_input("كلمة المرور الحالية", type="password")
        new_password = st.text_input("كلمة المرور الجديدة", type="password")
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
        
        col_sec1, col_sec2 = st.columns(2)
        
        with col_sec1:
            two_factor = st.checkbox("المصادقة الثنائية", value=False)
            session_timeout = st.number_input("انتهاء الجلسة (دقائق)", 5, 240, 30)
        
        with col_sec2:
            login_alerts = st.checkbox("تنبيهات تسجيل الدخول", value=True)
            ip_restriction = st.checkbox("تقييد عناوين IP", value=False)
        
        if st.form_submit_button("💾 حفظ إعدادات الأمان", use_container_width=True):
            if new_password and new_password == confirm_password:
                st.success("✅ تم تحديث إعدادات الأمان")
            else:
                st.error("❌ كلمة المرور غير متطابقة")

def render_device_settings():
    """إعدادات الجهاز"""
    
    st.markdown("### 📱 إعدادات الجهاز")
    
    col_dev1, col_dev2 = st.columns(2)
    
    with col_dev1:
        st.markdown("#### معلومات الجهاز")
        st.write(f"**نوع الجهاز:** {'جوال' if st.session_state.mobile_view else 'حاسوب'}")
        st.write(f"**عرض الشاشة:** {st.get_option('browser.gatherUsageStats')}")
        st.write(f"**المتصفح:** {st.get_option('browser.userAgent')[:50]}...")
        
        cache_size = st.slider("حجم الذاكرة المؤقتة (MB)", 10, 500, 100)
        auto_refresh = st.checkbox("تحديث تلقائي", value=True)
    
    with col_dev2:
        st.markdown("#### أداء النظام")
        
        cpu_usage = st.progress(45)
        st.caption("استخدام المعالج: 45%")
        
        memory_usage = st.progress(60)
        st.caption("استخدام الذاكرة: 60%")
        
        storage_usage = st.progress(75)
        st.caption("استخدام التخزين: 75%")
        
        if st.button("🔄 تحسين الأداء", use_container_width=True):
            st.info("جاري تحسين أداء النظام...")

def render_admin_page():
    """صفحة إدارة النظام"""
    
    if st.session_state.user_role != "admin":
        st.error("⛔ ليس لديك صلاحية الوصول إلى هذه الصفحة")
        return
    
    st.markdown("""
    <div class="page-header">
        <h1>👑 لوحة تحكم الإدمن</h1>
        <p>إدارة النظام بالكامل والتحكم في جميع الإعدادات</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات الإدارة
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "👥 المستخدمين",
        "⚙️ النظام",
        "📊 المعادلات",
        "🗺️ الخرائط",
        "📈 الإحصائيات",
        "📋 السجلات",
        "🚀 الأدوات"
    ])
    
    with tab1:
        render_user_management()
    
    with tab2:
        render_system_settings()
    
    with tab3:
        render_equation_management()
    
    with tab4:
        render_map_management()
    
    with tab5:
        render_system_statistics()
    
    with tab6:
        render_audit_logs()
    
    with tab7:
        render_admin_tools()

def render_user_management():
    """إدارة المستخدمين"""
    
    user_manager = UserManager()
    users = get_all_users()
    
    # بحث وتصفية
    col_search, col_filter, col_action = st.columns([2, 2, 1])
    
    with col_search:
        search_query = st.text_input("🔍 بحث عن مستخدم", placeholder="اسم أو بريد أو قسم")
    
    with col_filter:
        role_filter = st.multiselect("تصفية حسب الصلاحية", ["admin", "manager", "evaluator", "user"])
    
    with col_action:
        if st.button("➕ مستخدم جديد", use_container_width=True):
            st.session_state.show_user_form = True
    
    # عرض المستخدمين في جدول
    if users:
        df = pd.DataFrame(users)
        
        # التصفية
        if search_query:
            df = df[df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]
        
        if role_filter:
            df = df[df['role'].isin(role_filter)]
        
        # عرض الجدول مع خيارات
        st.dataframe(
            df[['username', 'name', 'email', 'role', 'created_at']],
            use_container_width=True,
            hide_index=True
        )
        
        # تحرير الصلاحيات
        st.markdown("### ✏️ تعديل صلاحيات المستخدمين")
        
        for _, user in df.iterrows():
            with st.expander(f"👤 {user['name']} ({user['role']})", expanded=False):
                col_per1, col_per2 = st.columns(2)
                
                with col_per1:
                    new_role = st.selectbox(
                        "الصلاحية",
                        ["admin", "manager", "evaluator", "viewer", "user"],
                        index=["admin", "manager", "evaluator", "viewer", "user"].index(user['role']),
                        key=f"role_{user['username']}"
                    )
                    
                    # صلاحيات محددة
                    st.markdown("**الصلاحيات المحددة:**")
                    
                    permissions = [
                        ("create_evaluation", "إنشاء تقييمات"),
                        ("edit_evaluation", "تعديل تقييمات"),
                        ("delete_evaluation", "حذف تقييمات"),
                        ("view_reports", "عرض التقارير"),
                        ("export_data", "تصدير البيانات"),
                        ("manage_users", "إدارة المستخدمين"),
                        ("system_settings", "إعدادات النظام")
                    ]
                    
                    user_perms = user_manager.get_user_permissions(user['username'])
                    
                    for perm_id, perm_label in permissions:
                        has_perm = user_perms.get(perm_id, False)
                        new_perm = st.checkbox(perm_label, value=has_perm, key=f"perm_{user['username']}_{perm_id}")
                        
                        if new_perm != has_perm:
                            user_manager.update_permission(user['username'], perm_id, new_perm)
                
                with col_per2:
                    # إجراءات
                    if st.button("💾 حفظ التغييرات", key=f"save_{user['username']}", use_container_width=True):
                        user_manager.update_user_role(user['username'], new_role)
                        st.success(f"✅ تم تحديث صلاحيات {user['name']}")
                    
                    if st.button("🗑️ حذف المستخدم", key=f"delete_{user['username']}", use_container_width=True, type="secondary"):
                        if user_manager.delete_user(user['username']):
                            st.success(f"✅ تم حذف المستخدم {user['name']}")
                            st.rerun()
    
    # نموذج إضافة مستخدم جديد
    if st.session_state.get('show_user_form'):
        with st.form("add_user_form"):
            st.markdown("### 📝 إضافة مستخدم جديد")
            
            col_new1, col_new2 = st.columns(2)
            
            with col_new1:
                new_username = st.text_input("اسم المستخدم")
                new_password = st.text_input("كلمة المرور", type="password")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
            
            with col_new2:
                new_name = st.text_input("الاسم الكامل")
                new_email = st.text_input("البريد الإلكتروني")
                new_role = st.selectbox("الصلاحية", ["user", "evaluator", "manager", "admin"])
            
            col_submit, col_cancel = st.columns(2)
            
            with col_submit:
                if st.form_submit_button("➕ إضافة المستخدم", use_container_width=True):
                    if new_password == confirm_password:
                        success = register_user(new_username, new_password, new_name, new_email, new_role)
                        if success:
                            st.success("✅ تمت إضافة المستخدم بنجاح")
                            st.session_state.show_user_form = False
                            st.rerun()
                    else:
                        st.error("❌ كلمة المرور غير متطابقة")
            
            with col_cancel:
                if st.form_submit_button("إلغاء", use_container_width=True, type="secondary"):
                    st.session_state.show_user_form = False
                    st.rerun()

def render_system_settings():
    """إعدادات النظام العام"""
    
    st.markdown("### ⚙️ إعدادات النظام العامة")
    
    with st.form("system_settings_form"):
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            st.markdown("#### الإعدادات العامة")
            
            system_name = st.text_input("اسم النظام", value="نظام العقارات البلدية")
            company_name = st.text_input("اسم المؤسسة", value="وزارة الشؤون البلدية")
            system_version = st.text_input("إصدار النظام", value="2.0.0")
            
            maintenance_mode = st.checkbox("وضع الصيانة", value=False)
            registration_open = st.checkbox("التسجيل مفتوح", value=True)
            
            st.markdown("#### الإشعارات")
            
            email_notifications = st.checkbox("إشعارات البريد", value=True)
            sms_notifications = st.checkbox("إشعارات SMS", value=False)
            push_notifications = st.checkbox("إشعارات التطبيق", value=True)
        
        with col_sys2:
            st.markdown("#### إعدادات التقييم")
            
            default_currency = st.selectbox("العملة الافتراضية", ["ريال سعودي", "دولار أمريكي", "يورو"])
            area_unit = st.selectbox("وحدة المساحة", ["متر مربع", "قدم مربع", "هكتار"])
            
            auto_save = st.checkbox("حفظ تلقائي", value=True)
            save_interval = st.slider("فترة الحفظ (ثواني)", 30, 300, 60)
            
            st.markdown("#### إعدادات التقارير")
            
            report_format = st.selectbox("صيغة التقارير", ["PDF", "Excel", "Word", "HTML"])
            include_charts = st.checkbox("تضمين الرسوم البيانية", value=True)
            auto_generate = st.checkbox("توليد تلقائي للتقارير", value=False)
        
        if st.form_submit_button("💾 حفظ إعدادات النظام", use_container_width=True):
            st.success("✅ تم حفظ إعدادات النظام")

def render_equation_management():
    """إدارة المعادلات"""
    
    equation_manager = EquationManager()
    
    st.markdown("### 📊 إدارة معادلات التقييم")
    
    # أنواع المعادلات
    equation_types = [
        ("عقارية", "معادلات التقييم العقاري"),
        ("إيجارية", "معادلات الإيجار"),
        ("استثمارية", "معادلات الاستثمار"),
        ("مالية", "معادلات مالية"),
        ("إحصائية", "معادلات إحصائية")
    ]
    
    for eq_type, eq_label in equation_types:
        with st.expander(f"📐 {eq_label}", expanded=False):
            equations = equation_manager.get_equations_by_type(eq_type)
            
            for eq in equations:
                col_eq1, col_eq2, col_eq3 = st.columns([3, 1, 1])
                
                with col_eq1:
                    st.markdown(f"**{eq['name']}**")
                    st.code(eq['formula'], language="python")
                    st.caption(f"المستخدمة في: {eq.get('usage_count', 0)} مرة")
                
                with col_eq2:
                    if st.button("✏️ تعديل", key=f"edit_eq_{eq['id']}"):
                        st.session_state.editing_equation = eq['id']
                
                with col_eq3:
                    if st.button("🧪 اختبار", key=f"test_eq_{eq['id']}"):
                        result = equation_manager.test_equation(eq['id'])
                        st.info(f"النتيجة: {result}")
            
            # إضافة معادلة جديدة
            with st.form(f"add_eq_{eq_type}"):
                new_name = st.text_input("اسم المعادلة", key=f"name_{eq_type}")
                new_formula = st.text_area("صيغة المعادلة", key=f"formula_{eq_type}")
                
                if st.form_submit_button(f"➕ إضافة معادلة {eq_label}", use_container_width=True):
                    if new_name and new_formula:
                        equation_manager.add_equation(eq_type, new_name, new_formula)
                        st.success(f"✅ تمت إضافة المعادلة")
                        st.rerun()
    
    # محرر المعادلات المتقدم
    st.markdown("---")
    st.markdown("### 🧮 محرر المعادلات المتقدم")
    
    col_editor1, col_editor2 = st.columns(2)
    
    with col_editor1:
        editor_type = st.selectbox("نوع المحرر", ["Python", "JavaScript", "SQL", "Custom"])
        
        if editor_type == "Python":
            equation_code = st.text_area("كود المعادلة", height=200,
                                        value="def calculate_rent(area, rate):\n    return area * rate")
        
        variables = st.text_area("المتغيرات (JSON)", value='{"area": 1000, "rate": 50}')
    
    with col_editor2:
        st.markdown("#### 📊 معاينة النتيجة")
        
        if st.button("▶️ تشغيل المعادلة", use_container_width=True):
            try:
                # محاكاة تنفيذ المعادلة
                vars_dict = json.loads(variables)
                result = vars_dict.get('area', 0) * vars_dict.get('rate', 0)
                st.success(f"✅ نتيجة المعادلة: {result:,.2f}")
            except:
                st.error("❌ خطأ في تنفيذ المعادلة")
        
        st.markdown("#### 📈 الإحصائيات")
        st.metric("عدد المعادلات", equation_manager.get_equation_count())
        st.metric("المعادلات النشطة", equation_manager.get_active_equation_count())
        st.metric("معدل الاستخدام", f"{equation_manager.get_usage_rate():.1f}%")

def render_map_management():
    """إدارة الخرائط"""
    
    map_system = MapSystem()
    
    st.markdown("### 🗺️ إعدادات الخرائط")
    
    col_map1, col_map2 = st.columns(2)
    
    with col_map1:
        st.markdown("#### إعدادات الخريطة الأساسية")
        
        default_map = st.selectbox("الخريطة الافتراضية", 
                                 ["الأساسية", "الستلايت", "الهجينة", "التضاريس"])
        
        default_zoom = st.slider("مستوى التكبير الافتراضي", 1, 20, 12)
        min_zoom = st.slider("الحد الأدنى للتكبير", 1, 10, 3)
        max_zoom = st.slider("الحد الأقصى للتكبير", 10, 20, 18)
        
        show_grid = st.checkbox("عرض الشبكة", value=True)
        show_labels = st.checkbox("عرض التسميات", value=True)
        show_buildings = st.checkbox("عرض المباني 3D", value=False)
    
    with col_map2:
        st.markdown("#### إعدادات الطبقات")
        
        layers = [
            ("حدود العقارات", True),
            ("الطرق والشوارع", True),
            ("الخدمات العامة", True),
            ("المناطق التجارية", False),
            ("المناطق السكنية", False),
            ("الحدائق العامة", True),
            ("المواقف", False)
        ]
        
        for layer_name, default_state in layers:
            state = st.checkbox(layer_name, value=default_state)
            if state:
                st.progress(100)
        
        st.markdown("#### الإحصائيات")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("عدد العلامات", "1,248")
        with col_stat2:
            st.metric("المناطق المغطاة", "85%")
    
    # اختبار الخريطة
    st.markdown("---")
    st.markdown("### 🎮 اختبار الخريطة")
    
    test_location = st.text_input("موقع الاختبار", value="الرياض, المملكة العربية السعودية")
    
    col_test1, col_test2, col_test3 = st.columns(3)
    
    with col_test1:
        test_lat = st.number_input("خط العرض", value=24.7136)
    
    with col_test2:
        test_lng = st.number_input("خط الطول", value=46.6753)
    
    with col_test3:
        test_zoom = st.slider("التكبير", 1, 20, 12)
    
    if st.button("🗺️ عرض الخريطة التجريبية", use_container_width=True):
        map_system.test_map(test_lat, test_lng, test_zoom)
        st.success("✅ تم تحميل الخريطة التجريبية")

def render_system_statistics():
    """إحصائيات النظام"""
    
    st.markdown("### 📈 إحصائيات النظام الشاملة")
    
    # بطاقات الإحصائيات
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("👥 المستخدمين النشطين", "142", "+8")
    
    with col_stat2:
        st.metric("📊 التقييمات اليومية", "24", "+3")
    
    with col_stat3:
        st.metric("💰 القيمة الإجمالية", "4.2M", "+320K")
    
    with col_stat4:
        st.metric("📈 معدل النمو", "18%", "+2%")
    
    # الرسوم البيانية
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### 📊 نشاط المستخدمين")
        
        activity_data = pd.DataFrame({
            'الشهر': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو'],
            'المستخدمون': [120, 135, 142, 150, 165],
            'التقييمات': [450, 520, 600, 680, 720]
        })
        
        fig = px.line(activity_data, x='الشهر', y=['المستخدمون', 'التقييمات'],
                     title='نمو النظام الشهري')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("#### 📈 توزيع التقييمات")
        
        eval_data = pd.DataFrame({
            'النوع': ['سكني', 'تجاري', 'صناعي', 'زراعي', 'سياحي'],
            'التقييمات': [320, 240, 180, 120, 80],
            'القيمة': [1200000, 1800000, 900000, 300000, 800000]
        })
        
        fig = px.bar(eval_data, x='النوع', y='التقييمات',
                    color='القيمة', title='التقييمات حسب النوع')
        st.plotly_chart(fig, use_container_width=True)
    
    # إحصائيات متقدمة
    st.markdown("---")
    st.markdown("### 📊 إحصائيات متقدمة")
    
    tab_adv1, tab_adv2, tab_adv3 = st.tabs(["الأداء", "الاستخدام", "الجودة"])
    
    with tab_adv1:
        col_perf1, col_perf2, col_perf3 = st.columns(3)
        
        with col_perf1:
            st.markdown("**زمن الاستجابة**")
            st.progress(85)
            st.caption("متوسط: 320ms")
        
        with col_perf2:
            st.markdown("**معدل النجاح**")
            st.progress(98)
            st.caption("98.2%")
        
        with col_perf3:
            st.markdown("**إشباع المستخدم**")
            st.progress(92)
            st.caption("4.6/5")
    
    with tab_adv2:
        st.markdown("**توزيع وقت الاستخدام**")
        
        usage_data = pd.DataFrame({
            'المهمة': ['التقييم', 'التقارير', 'الخرائط', 'الإدارة', 'الإعدادات'],
            'الوقت (ساعة)': [45, 28, 32, 15, 8]
        })
        
        fig = px.pie(usage_data, values='الوقت (ساعة)', names='المهمة',
                    title='توزيع وقت الاستخدام')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab_adv3:
        st.markdown("**مؤشرات الجودة**")
        
        quality_metrics = pd.DataFrame({
            'المؤشر': ['الدقة', 'الاكتمال', 'الحداثة', 'الاتساق', 'الموثوقية'],
            'القيمة': [94, 88, 92, 96, 90]
        })
        
        fig = go.Figure(data=go.Scatterpolar(
            r=quality_metrics['القيمة'],
            theta=quality_metrics['المؤشر'],
            fill='toself'
        ))
        
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                         showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def render_audit_logs():
    """سجلات التدقيق"""
    
    st.markdown("### 📋 سجلات النظام")
    
    # تصفية السجلات
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        log_type = st.multiselect("نوع السجل", ["معلومات", "تحذير", "خطأ", "أمان"])
    
    with col_filter2:
        date_range = st.date_input("الفترة الزمنية", [])
    
    with col_filter3:
        user_filter = st.text_input("فلترة بالمستخدم")
    
    # بيانات السجلات (افتراضية)
    logs_data = [
        {"التاريخ": "2024-01-15 10:30", "المستخدم": "أحمد", "النوع": "معلومات", "الحدث": "تسجيل دخول", "التفاصيل": "الدخول من IP 192.168.1.1"},
        {"التاريخ": "2024-01-15 11:15", "المستخدم": "محمد", "النوع": "أمان", "الحدث": "محاولة وصول", "التفاصيل": "محاولة وصول غير مصرح"},
        {"التاريخ": "2024-01-15 12:00", "المستخدم": "سارة", "النوع": "معلومات", "الحدث": "إنشاء تقييم", "التفاصيل": "تقييم عقار رقم 123"},
        {"التاريخ": "2024-01-15 14:30", "المستخدم": "خالد", "النوع": "تحذير", "الحدث": "تعديل بيانات", "التفاصيل": "تعديل بيانات مستخدم"},
        {"التاريخ": "2024-01-15 16:45", "المستخدم": "نورة", "النوع": "معلومات", "الحدث": "تصدير تقرير", "التفاصيل": "تقرير PDF للربع الأول"},
        {"التاريخ": "2024-01-15 18:20", "المستخدم": "فهد", "النوع": "خطأ", "الحدث": "خطأ في المعادلة", "التفاصيل": "خطأ في معادلة التقييم 5"},
    ]
    
    df_logs = pd.DataFrame(logs_data)
    
    # التصفية
    if log_type:
        df_logs = df_logs[df_logs['النوع'].isin(log_type)]
    
    if user_filter:
        df_logs = df_logs[df_logs['المستخدم'].str.contains(user_filter, case=False)]
    
    # عرض السجلات
    st.dataframe(df_logs, use_container_width=True, hide_index=True)
    
    # تحليل السجلات
    st.markdown("---")
    st.markdown("### 📈 تحليل السجلات")
    
    col_anal1, col_anal2 = st.columns(2)
    
    with col_anal1:
        log_counts = df_logs['النوع'].value_counts()
        fig = px.pie(values=log_counts.values, names=log_counts.index,
                    title='توزيع أنواع السجلات')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_anal2:
        hourly_counts = pd.DataFrame({
            'الساعة': ['8-10', '10-12', '12-14', '14-16', '16-18', '18-20'],
            'الأحداث': [45, 68, 52, 41, 38, 22]
        })
        
        fig = px.bar(hourly_counts, x='الساعة', y='الأحداث',
                    title='النشاط حسب الوقت')
        st.plotly_chart(fig, use_container_width=True)
    
    # تصدير السجلات
    st.markdown("---")
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        if st.button("📥 تصدير كـ Excel", use_container_width=True):
            st.success("✅ تم تصدير السجلات")
    
    with col_export2:
        if st.button("📄 تصدير كـ PDF", use_container_width=True):
            st.success("✅ تم تصدير السجلات")
    
    with col_export3:
        if st.button("🗑️ تنظيف السجلات القديمة", use_container_width=True, type="secondary"):
            st.warning("⚠️ سيتم حذف السجلات الأقدم من 90 يوم")

def render_admin_tools():
    """أدوات الإدارة"""
    
    st.markdown("### 🛠️ أدوات الإدارة المتقدمة")
    
    # تبويبات الأدوات
    tab_tool1, tab_tool2, tab_tool3, tab_tool4 = st.tabs([
        "🔄 الصيانة",
        "📦 النسخ الاحتياطي",
        "🔍 الفحص",
        "⚡ الأداء"
    ])
    
    with tab_tool1:
        render_maintenance_tools()
    
    with tab_tool2:
        render_backup_tools()
    
    with tab_tool3:
        render_diagnostic_tools()
    
    with tab_tool4:
        render_performance_tools()

def render_maintenance_tools():
    """أدوات الصيانة"""
    
    st.markdown("#### 🔧 أدوات صيانة النظام")
    
    col_maint1, col_maint2 = st.columns(2)
    
    with col_maint1:
        if st.button("🔄 إعادة بناء الفهرس", use_container_width=True):
            st.info("جاري إعادة بناء الفهرس...")
            st.success("✅ تمت إعادة بناء الفهرس")
        
        if st.button("🧹 تنظيف الذاكرة المؤقتة", use_container_width=True):
            st.info("جاري تنظيف الذاكرة المؤقتة...")
            st.success("✅ تم تنظيف الذاكرة المؤقتة")
        
        if st.button("📊 تحديث الإحصائيات", use_container_width=True):
            st.info("جاري تحديث الإحصائيات...")
            st.success("✅ تم تحديث الإحصائيات")
    
    with col_maint2:
        if st.button("🔍 فحص سلامة البيانات", use_container_width=True):
            with st.spinner("جاري فحص البيانات..."):
                # محاكاة فحص البيانات
                issues = ["لا توجد مشاكل", "جميع البيانات سليمة"]
                for issue in issues:
                    st.success(f"✓ {issue}")
        
        if st.button("🔄 مزامنة البيانات", use_container_width=True):
            with st.spinner("جاري مزامنة البيانات..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                st.success("✅ تمت مزامنة البيانات بنجاح")
        
        maintenance_mode = st.checkbox("تفعيل وضع الصيانة")
        if maintenance_mode:
            st.warning("⚠️ النظام في وضع الصيانة - قد لا يكون متاحاً للمستخدمين")

def render_backup_tools():
    """أدوات النسخ الاحتياطي"""
    
    st.markdown("#### 💾 أدوات النسخ الاحتياطي")
    
    # إنشاء نسخة احتياطية
    col_backup1, col_backup2 = st.columns(2)
    
    with col_backup1:
        backup_name = st.text_input("اسم النسخة الاحتياطية", 
                                  value=f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}")
        
        backup_type = st.selectbox("نوع النسخة", ["كاملة", "مختارة", "تزايدية"])
        
        if st.button("💾 إنشاء نسخة احتياطية", use_container_width=True):
            with st.spinner("جاري إنشاء النسخة الاحتياطية..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                st.success(f"✅ تم إنشاء النسخة الاحتياطية: {backup_name}")
    
    with col_backup2:
        st.markdown("**النسخ الاحتياطية المتاحة:**")
        
        backups = [
            {"الاسم": "backup_20240115", "التاريخ": "2024-01-15", "الحجم": "245 MB"},
            {"الاسم": "backup_20240108", "التاريخ": "2024-01-08", "الحجم": "230 MB"},
            {"الاسم": "backup_20240101", "التاريخ": "2024-01-01", "الحجم": "215 MB"},
        ]
        
        for backup in backups:
            col_restore, col_delete = st.columns([3, 1])
            
            with col_restore:
                if st.button(f"📥 {backup['الاسم']}", key=f"restore_{backup['الاسم']}"):
                    st.info(f"جاري استعادة {backup['الاسم']}...")
            
            with col_delete:
                if st.button("🗑️", key=f"delete_{backup['الاسم']}"):
                    st.warning(f"تم حذف {backup['الاسم']}")
    
    # جدولة النسخ الاحتياطية
    st.markdown("---")
    st.markdown("#### 📅 جدولة النسخ الاحتياطية")
    
    col_sched1, col_sched2, col_sched3 = st.columns(3)
    
    with col_sched1:
        schedule_enabled = st.checkbox("تفعيل الجدولة", value=True)
    
    with col_sched2:
        schedule_frequency = st.selectbox("التردد", ["يومياً", "أسبوعياً", "شهرياً"])
    
    with col_sched3:
        schedule_time = st.time_input("الوقت", value=datetime.now().time())
    
    if st.button("💾 حفظ الجدولة", use_container_width=True):
        st.success("✅ تم حفظ جدولة النسخ الاحتياطية")

def render_diagnostic_tools():
    """أدوات التشخيص"""
    
    st.markdown("#### 🔍 أدوات تشخيص النظام")
    
    # فحوصات النظام
    diagnostics = [
        ("قاعدة البيانات", "فحص الاتصال وسلامة البيانات", "success"),
        ("الملفات والمجلدات", "فحص الصلاحيات والمساحات", "warning"),
        ("الشبكة والاتصال", "فحص سرعة الاتصال واستقراره", "success"),
        ("الذاكرة والمعالج", "فحص استخدام الموارد", "error"),
        ("الأمان والحماية", "فحص الثغرات الأمنية", "warning"),
        ("التحديثات", "فحص التحديثات المتاحة", "success"),
    ]
    
    for diag_name, diag_desc, diag_status in diagnostics:
        col_diag1, col_diag2, col_diag3 = st.columns([2, 2, 1])
        
        with col_diag1:
            st.write(f"**{diag_name}**")
            st.caption(diag_desc)
        
        with col_diag2:
            if diag_status == "success":
                st.success("✓ جيد")
            elif diag_status == "warning":
                st.warning("⚠️ يحتاج انتباه")
            else:
                st.error("❌ خطأ")
        
        with col_diag3:
            if st.button("فحص", key=f"check_{diag_name}"):
                st.info(f"جاري فحص {diag_name}...")
    
    # تقرير التشخيص
    st.markdown("---")
    
    if st.button("📋 إنشاء تقرير تشخيص كامل", use_container_width=True):
        with st.spinner("جاري إنشاء تقرير التشخيص..."):
            # محاكاة إنشاء التقرير
            report_data = {
                "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "الحالة العامة": "جيدة",
                "المشاكل المكتشفة": 2,
                "التوصيات": ["تحديث النظام", "توسعة مساحة التخزين"]
            }
            
            st.json(report_data)
            
            col_report1, col_report2 = st.columns(2)
            
            with col_report1:
                if st.button("📥 تحميل التقرير", use_container_width=True):
                    st.success("✅ تم تحميل التقرير")
            
            with col_report2:
                if st.button("📧 إرسال للإدارة", use_container_width=True):
                    st.success("✅ تم إرسال التقرير")

def render_performance_tools():
    """أدوات تحسين الأداء"""
    
    st.markdown("#### ⚡ أدوات تحسين الأداء")
    
    # مراقبة الأداء في الوقت الحقيقي
    st.markdown("##### 📊 مراقبة الأداء الحي")
    
    col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
    
    with col_perf1:
        st.metric("استخدام المعالج", "45%", "-2%")
    
    with col_perf2:
        st.metric("استخدام الذاكرة", "68%", "+3%")
    
    with col_perf3:
        st.metric("استخدام التخزين", "82%", "+1%")
    
    with col_perf4:
        st.metric("زمن الاستجابة", "320ms", "-15ms")
    
    # تحسينات مقترحة
    st.markdown("---")
    st.markdown("##### 🚀 تحسينات مقترحة")
    
    optimizations = [
        ("🗃️ تنظيف قاعدة البيانات", "حذف السجلات القديمة", "عالي", "30% تحسين"),
        ("🧹 تنظيف الذاكرة المؤقتة", "تحرير ذاكرة التخزين المؤقت", "متوسط", "15% تحسين"),
        ("📊 تحديث الإحصائيات", "إعادة حساب الإحصائيات", "منخفض", "5% تحسين"),
        ("🔧 إعادة بناء الفهرس", "تحسين سرعة البحث", "عالي", "40% تحسين"),
    ]
    
    for opt_name, opt_desc, opt_impact, opt_gain in optimizations:
        col_opt1, col_opt2, col_opt3, col_opt4 = st.columns([2, 2, 1, 2])
        
        with col_opt1:
            st.write(f"**{opt_name}**")
            st.caption(opt_desc)
        
        with col_opt2:
            if opt_impact == "عالي":
                st.error(opt_impact)
            elif opt_impact == "متوسط":
                st.warning(opt_impact)
            else:
                st.info(opt_impact)
        
        with col_opt3:
            st.write(opt_gain)
        
        with col_opt4:
            if st.button("تطبيق", key=f"apply_{opt_name}"):
                st.info(f"جاري تطبيق {opt_name}...")
                st.success(f"✅ تم تطبيق {opt_name}")
    
    # إعدادات متقدمة للأداء
    st.markdown("---")
    st.markdown("##### ⚙️ إعدادات الأداء المتقدمة")
    
    with st.form("performance_settings"):
        col_set1, col_set2 = st.columns(2)
        
        with col_set1:
            cache_size = st.slider("حجم الذاكرة المؤقتة (MB)", 50, 1000, 200)
            query_cache = st.checkbox("تفعيل ذاكرة الاستعلامات", value=True)
            compression = st.checkbox("ضغط البيانات", value=True)
        
        with col_set2:
            max_connections = st.slider("الحد الأقصى للاتصالات", 10, 500, 100)
            timeout = st.slider("مهلة الاتصال (ثواني)", 5, 300, 30)
            retry_attempts = st.slider("محاولات إعادة الاتصال", 1, 10, 3)
        
        if st.form_submit_button("💾 حفظ إعدادات الأداء", use_container_width=True):
            st.success("✅ تم حفظ إعدادات الأداء")

def render_profile_page():
    """صفحة الملف الشخصي"""
    
    st.markdown("""
    <div class="page-header">
        <h1>👤 الملف الشخصي</h1>
        <p>إدارة معلومات حسابك وإعداداتك الشخصية</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_prof1, col_prof2 = st.columns([1, 2])
    
    with col_prof1:
        # صورة الملف الشخصي
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white;">
            <div style="font-size: 80px; margin-bottom: 20px;">👤</div>
            <h3>{user_name}</h3>
            <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; 
                        display: inline-block; margin: 10px 0;">
                {user_role}
            </div>
            <p style="margin: 10px 0;">عضو منذ: يناير 2024</p>
        </div>
        """.format(user_name=st.session_state.user_name, 
                  user_role=st.session_state.user_role.upper()), unsafe_allow_html=True)
        
        # إحصائيات شخصية
        st.markdown("---")
        st.markdown("#### 📊 إحصائياتي")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("التقييمات", "24")
        with col_stat2:
            st.metric("الساعات", "45")
        
        col_stat3, col_stat4 = st.columns(2)
        with col_stat3:
            st.metric("المشاريع", "8")
        with col_stat4:
            st.metric("التقارير", "12")
    
    with col_prof2:
        # معلومات الحساب
        with st.container():
            st.subheader("📝 معلومات الحساب")
            
            tabs = st.tabs(["المعلومات الأساسية", "التخصصات", "الإشعارات", "الخصوصية"])
            
            with tabs[0]:
                with st.form("basic_info_form"):
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        full_name = st.text_input("الاسم الكامل", value=st.session_state.user_name)
                        email = st.text_input("البريد الإلكتروني", value="user@example.com")
                        phone = st.text_input("رقم الهاتف", value="+966 5X XXX XXXX")
                    
                    with col_info2:
                        department = st.selectbox("القسم", ["التقييم العقاري", "الإدارة المالية", "تخطيط المدن", "التطوير العقاري"])
                        position = st.text_input("المنصب", value="مقيم عقاري")
                        join_date = st.date_input("تاريخ الانضمام", value=datetime(2024, 1, 1))
                    
                    bio = st.text_area("نبذة عني", placeholder="اكتب نبذة مختصرة عن نفسك...", height=100)
                    
                    if st.form_submit_button("💾 حفظ التغييرات", use_container_width=True):
                        st.success("✅ تم حفظ المعلومات بنجاح")
            
            with tabs[1]:
                st.markdown("#### 🎯 التخصصات والمهارات")
                
                specializations = [
                    "التقييم العقاري",
                    "التحليل المالي",
                    "إدارة المشاريع",
                    "الخرائط والGIS",
                    "التحليل الإحصائي",
                    "التخطيط الحضري"
                ]
                
                selected_specializations = st.multiselect("التخصصات", specializations, default=["التقييم العقاري"])
                
                skill_level = st.slider("مستوى الخبرة", 1, 10, 7)
                certifications = st.text_area("الشهادات والتدريبات")
                
                if st.button("💾 حفظ التخصصات", use_container_width=True):
                    st.success("✅ تم حفظ التخصصات")
            
            with tabs[2]:
                st.markdown("#### 🔔 إعدادات الإشعارات")
                
                col_notif1, col_notif2 = st.columns(2)
                
                with col_notif1:
                    st.markdown("**الإشعارات العامة:**")
                    notify_evaluations = st.checkbox("التقييمات الجديدة", value=True)
                    notify_reports = st.checkbox("التقارير الجاهزة", value=True)
                    notify_system = st.checkbox("تحديثات النظام", value=True)
                    notify_news = st.checkbox("الأخبار والتحديثات", value=False)
                
                with col_notif2:
                    st.markdown("**طرق الإرسال:**")
                    email_notifications = st.checkbox("البريد الإلكتروني", value=True)
                    sms_notifications = st.checkbox("رسائل SMS", value=False)
                    push_notifications = st.checkbox("إشعارات التطبيق", value=True)
                    
                    frequency = st.selectbox("تكرار الإشعارات", ["فورية", "يومياً", "أسبوعياً"])
                
                if st.button("💾 حفظ إعدادات الإشعارات", use_container_width=True):
                    st.success("✅ تم حفظ إعدادات الإشعارات")
            
            with tabs[3]:
                st.markdown("#### 🔒 إعدادات الخصوصية")
                
                col_privacy1, col_privacy2 = st.columns(2)
                
                with col_privacy1:
                    st.markdown("**الخصوصية:**")
                    profile_public = st.checkbox("الملف الشخصي عام", value=False)
                    show_email = st.checkbox("عرض البريد الإلكتروني", value=False)
                    show_activity = st.checkbox("عرض النشاط الأخير", value=True)
                    data_collection = st.checkbox("السماح بجمع البيانات", value=True)
                
                with col_privacy2:
                    st.markdown("**الأمان:**")
                    two_factor = st.checkbox("المصادقة الثنائية", value=False)
                    session_timeout = st.number_input("انتهاء الجلسة (دقائق)", 5, 240, 30)
                    login_alerts = st.checkbox("تنبيهات تسجيل الدخول", value=True)
                
                # إدارة الجلسات
                st.markdown("##### 📱 الجلسات النشطة")
                sessions = [
                    {"الجهاز": "كمبيوتر المكتب", "الموقع": "الرياض", "النشطة منذ": "2 ساعة"},
                    {"الجهاز": "هاتف أندرويد", "الموقع": "جدة", "النشطة منذ": "5 دقائق"},
                ]
                
                for session in sessions:
                    col_sess1, col_sess2, col_sess3 = st.columns([2, 2, 1])
                    with col_sess1:
                        st.write(f"**{session['الجهاز']}**")
                    with col_sess2:
                        st.write(session['الموقع'])
                    with col_sess3:
                        if st.button("إنهاء", key=f"end_{session['الجهاز']}"):
                            st.success(f"تم إنهاء جلسة {session['الجهاز']}")
                
                if st.button("💾 حفظ إعدادات الخصوصية", use_container_width=True):
                    st.success("✅ تم حفظ إعدادات الخصوصية")

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
