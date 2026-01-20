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
from modules.site_rental_value import SiteRentalValuation
from modules.municipal_lease_types import MunicipalLeaseTypes  # ⬅️ الجديد
from modules.investment_committee import InvestmentCommitteeSystem  # ⬅️ الجديد

# تطبيق التصميم المخصص
apply_custom_style()

# تهيئة حالة الجلسة
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"
if 'selected_lease_type' not in st.session_state:  # ⬅️ الجديد
    st.session_state.selected_lease_type = None
if 'selected_subtype' not in st.session_state:     # ⬅️ الجديد
    st.session_state.selected_subtype = None

def main():
    """الدالة الرئيسية للتطبيق"""
    
    # تطبيق CSS المخصص مع تحسين RTL
    custom_css = get_custom_css() + """
    <style>
    /* تحسينات RTL إضافية */
    .rtl-text {
        direction: rtl;
        text-align: right;
    }
    .lease-type-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: white;
        text-align: right;
    }
    .committee-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .regulation-badge {
        background: #10b981;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin-left: 10px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # شريط العنوان مع الشعار
    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <h1 class="app-title">🏛️ نظام تأجير العقارات البلدية</h1>
            <p class="app-subtitle">نظام متوافق مع لوائح وزارة الشؤون البلدية والقروية والإسكان</p>
        </div>
        <div class="header-status">
            <span class="status-badge">📍 الرياض، المملكة العربية السعودية</span>
            <span class="status-badge">📅 {datetime.now().strftime("%Y-%m-%د")}</span>
            <span class="regulation-badge">📋 متوافق مع اللوائح</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # شريط التنقل العلوي المحسن
    render_enhanced_navigation_bar()
    
    # عرض المحتوى بناءً على الصفحة المختارة
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard':
        render_dashboard(st.session_state.user_role)
    elif page == 'evaluation':
        render_evaluation_module(st.session_state.user_role)
    elif page == 'site_rental':
        render_enhanced_site_rental_page()
    elif page == 'lease_types':  # ⬅️ الصفحة الجديدة
        render_lease_types_page()
    elif page == 'committee':  # ⬅️ الصفحة الجديدة
        render_committee_page()
    elif page == 'reports':
        render_report_module(st.session_state.user_role)
    elif page == 'admin':
        render_admin_panel(st.session_state.user_role)
    elif page == 'profile':
        render_profile_page()
    elif page == 'regulations':  # ⬅️ الصفحة الجديدة
        render_regulations_page()

def render_enhanced_navigation_bar():
    """شريط التنقل العلوي المحسن"""
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 1, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="user-info">
            <span class="user-role {st.session_state.user_role}">{st.session_state.user_role.upper()}</span>
            <span class="user-name">👋 مرحباً، {st.session_state.user_name}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # أزرار التنقل المحسنة
    with col2:
        if st.button("📊 لوحة التحكم", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col3:
        if st.button("📈 التقييم", use_container_width=True):
            st.session_state.current_page = 'evaluation'
            st.rerun()
    
    with col4:
        if st.button("🏛️ أنواع التأجير", use_container_width=True):  # ⬅️ الزر الجديد
            st.session_state.current_page = 'lease_types'
            st.rerun()
    
    with col5:
        if st.button("👥 لجنة الاستثمار", use_container_width=True):  # ⬅️ الزر الجديد
            st.session_state.current_page = 'committee'
            st.rerun()
    
    with col6:
        if st.button("📑 التقارير", use_container_width=True):
            st.session_state.current_page = 'reports'
            st.rerun()
    
    with col7:
        menu_options = ["الملف الشخصي", "اللوائح والضوابط", "تسجيل الخروج"]
        selected_option = st.selectbox("⚙️", menu_options, label_visibility="collapsed")
        
        if selected_option == "الملف الشخصي":
            st.session_state.current_page = 'profile'
            st.rerun()
        elif selected_option == "اللوائح والضوابط":
            st.session_state.current_page = 'regulations'
            st.rerun()
        elif selected_option == "تسجيل الخروج":
            logout()
            st.session_state.authenticated = False
            st.rerun()

def render_enhanced_site_rental_page():
    """صفحة تحديد القيمة الإيجارية المحسنة"""
    
    st.markdown("""
    <div class="section-header">
        <h2>📍 نظام تحديد القيمة الإيجارية للموقع - الإصدار المتوافق</h2>
        <p>تقييم متوافق مع لوائح التصرف بالعقارات البلدية</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تحذير إذا لم يتم اختيار نوع التأجير
    if not st.session_state.selected_lease_type:
        st.warning("""
        ⚠️ **يرجى اختيار نوع التأجير أولاً**
        
        قبل البدء في التقييم، يجب تحديد نوع التأجير المناسب حسب اللوائح البلدية.
        
        [🏛️ انتقل إلى صفحة أنواع التأجير](#)
        """)
        
        if st.button("🏛️ اختيار نوع التأجير", use_container_width=True):
            st.session_state.current_page = 'lease_types'
            st.rerun()
        return
    
    # عرض نوع التأجير المختار
    lease_types = MunicipalLeaseTypes()
    details = lease_types.get_lease_type_details(
        st.session_state.selected_lease_type,
        st.session_state.selected_subtype
    )
    
    if details:
        col_info, col_duration = st.columns([3, 1])
        
        with col_info:
            st.markdown(f"""
            <div class="lease-type-card">
                <h3>{details.get('name', 'غير محدد')}</h3>
                <p><strong>المصدر القانوني:</strong> {details.get('source', 'غير محدد')}</p>
                <p><strong>متوافق مع:</strong> {details.get('regulation_reference', 'اللوائح البلدية')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_duration:
            if 'max_duration_months' in details:
                st.metric("المدة القصوى", f"{details['max_duration_months']} شهر")
            elif 'max_years' in details:
                st.metric("المدة القصوى", f"{details['max_years']} سنة")
    
    # استدعاء نظام التقييم المحسن
    rental_valuator = EnhancedSiteRentalValuation()
    rental_valuator.render_enhanced_valuation()

def render_lease_types_page():
    """صفحة أنواع التأجير حسب اللوائح"""
    
    st.markdown("""
    <div class="section-header">
        <h2>🏛️ أنواع التأجير البلدية حسب اللوائح</h2>
        <p>اختر نوع التأجير المناسب حسب اللوائح والضوابط البلدية</p>
    </div>
    """, unsafe_allow_html=True)
    
    lease_types = MunicipalLeaseTypes()
    
    # تبويبات لأنواع التأجير
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 تأجير مؤقت",
        "🏗️ تأجير طويل الأجل",
        "🎯 تأجير مباشر",
        "⚖️ عقارات مستثناة"
    ])
    
    with tab1:
        render_temporary_lease_types(lease_types)
    
    with tab2:
        render_long_term_lease_types(lease_types)
    
    with tab3:
        render_direct_lease_types(lease_types)
    
    with tab4:
        render_exempted_lease_types(lease_types)
    
    # عرض النوع المختار حالياً
    if st.session_state.selected_lease_type:
        st.markdown("---")
        st.subheader("📌 النوع المحدد حالياً")
        
        details = lease_types.get_lease_type_details(
            st.session_state.selected_lease_type,
            st.session_state.selected_subtype
        )
        
        if details:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.info(f"""
                **النوع:** {details.get('name', 'غير محدد')}
                
                **المدة القصوى:** {details.get('max_duration_months', details.get('max_years', 'غير محدد'))} {'شهر' if 'max_duration_months' in details else 'سنة'}
                
                **المصدر:** {details.get('source', 'غير محدد')}
                """)
            
            with col2:
                if st.button("🚀 المتابعة للتقييم", use_container_width=True):
                    st.session_state.current_page = 'site_rental'
                    st.rerun()
                
                if st.button("🗑️ إلغاء الاختيار", use_container_width=True, type="secondary"):
                    st.session_state.selected_lease_type = None
                    st.session_state.selected_subtype = None
                    st.rerun()

def render_temporary_lease_types(lease_types):
    """عرض أنواع التأجير المؤقت"""
    
    st.markdown("""
    ### 🎪 تأجير مؤقت للأنشطة والفعاليات
    
    **المصدر:** المادة 3 من الضوابط، المادة 10/3 من اللائحة
    """)
    
    details = lease_types.get_lease_type_details('TEMPORARY_ACTIVITY')
    
    if details:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **الخصائص:**
            - المدة القصوى: 6 أشهر
            - قابلة للتمديد لمدة إضافية
            - أقصى عدد للتمديد: 3 طلبات
            - المدة الإجمالية القصوى: 12 شهراً
            """)
        
        with col2:
            st.markdown("""
            **الأنشطة المشمولة:**
            - الفعاليات والمهرجانات
            - المؤتمرات والمناسبات
            - الفعاليات الترويجية
            - الأنشطة الموسمية
            """)
        
        st.markdown("---")
        
        if st.button("✅ اختيار هذا النوع", key="select_temp", use_container_width=True):
            st.session_state.selected_lease_type = 'TEMPORARY_ACTIVITY'
            st.session_state.selected_subtype = None
            st.success("تم اختيار نوع التأجير المؤقت")
            st.rerun()

def render_long_term_lease_types(lease_types):
    """عرض أنواع التأجير طويل الأجل"""
    
    st.markdown("""
    ### 🏗️ تأجير طويل الأجل (استثماري)
    
    **المصدر:** المادة 21 من اللائحة
    """)
    
    details = lease_types.get_lease_type_details('LONG_TERM_INVESTMENT')
    
    if details and 'subtypes' in details:
        # اختيار النوع الفرعي
        subtype_options = list(details['subtypes'].keys())
        subtype_names = {k: v['name'] for k, v in details['subtypes'].items()}
        
        selected_subtype = st.selectbox(
            "اختر النوع الفرعي:",
            subtype_options,
            format_func=lambda x: subtype_names[x]
        )
        
        subtype_details = details['subtypes'][selected_subtype]
        
        # عرض التفاصيل
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **الخصائص:**
            - المدة القصوى: {subtype_details['max_years']} سنة
            - الشروط: {subtype_details['conditions']}
            - اللجنة المطلوبة: نعم
            """)
        
        with col2:
            st.markdown(f"""
            **الضوابط:**
            - حسب المادة 21 من اللائحة
            - تحتاج موافقة لجنة الاستثمار
            - قد تحتاج موافقة الوزير
            """)
        
        st.markdown("---")
        
        if st.button("✅ اختيار هذا النوع", key="select_long", use_container_width=True):
            st.session_state.selected_lease_type = 'LONG_TERM_INVESTMENT'
            st.session_state.selected_subtype = selected_subtype
            st.success(f"تم اختيار نوع التأجير: {subtype_details['name']}")
            st.rerun()

def render_direct_lease_types(lease_types):
    """عرض أنواع التأجير المباشر"""
    
    st.markdown("""
    ### 🎯 تأجير مباشر
    
    **المصدر:** المادة 27 من اللائحة
    """)
    
    details = lease_types.get_lease_type_details('DIRECT_LEASE')
    
    if details:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **الشروط:**
            - بعد إعلان واحد للحدائق العامة وعدم وجود مستثمرين
            - بعد إعلانين لأي عقار آخر وعدم وجود مستثمرين
            - المدة: سنة واحدة من تاريخ تسلم العروض
            - السعر: لا يقل عن 75% من السعر الاسترشادي
            """)
        
        with col2:
            st.markdown("""
            **الإجراءات:**
            - تحتاج موافقة لجنة الاستثمار
            - قد تحتاج موافقة الوزير
            - السعر الاسترشادي +25%
            """)
        
        st.markdown("---")
        
        if st.button("✅ اختيار هذا النوع", key="select_direct", use_container_width=True):
            st.session_state.selected_lease_type = 'DIRECT_LEASE'
            st.session_state.selected_subtype = None
            st.success("تم اختيار نوع التأجير المباشر")
            st.rerun()

def render_exempted_lease_types(lease_types):
    """عرض العقارات المستثناة من المنافسة"""
    
    st.markdown("""
    ### ⚖️ عقارات مستثناة من المنافسة
    
    **المصدر:** المادة 10 من اللائحة، المادة 34 من التعليمات
    """)
    
    details = lease_types.get_lease_type_details('EXEMPTED_FROM_COMPETITION')
    
    if details:
        st.markdown("""
        **الفئات المستثناة:**
        1. عقارات مع جهات حكومية
        2. عقارات مع شركات امتياز عام
        3. عقارات مع شركات تساهم فيها الدولة
        4. عقارات لمنفذي المشروعات (≤3 سنوات)
        5. عقارات لمعالجة أوضاع قائمة
        6. حدائق في مخططات خاصة (≤سنتين)
        7. **أنشطة مؤقتة** ⬅️ مرتبط بالنوع الأول
        8. مشروعات مبتكرة/رائدة/مميزة
        9. عقارات للمنافسة العلنية المفتوحة
        """)
        
        st.markdown("---")
        
        if st.button("✅ اختيار هذا النوع", key="select_exempt", use_container_width=True):
            st.session_state.selected_lease_type = 'EXEMPTED_FROM_COMPETITION'
            st.session_state.selected_subtype = None
            st.success("تم اختيار نوع العقارات المستثناة")
            st.rerun()

def render_committee_page():
    """صفحة لجنة الاستثمار"""
    
    st.markdown("""
    <div class="section-header">
        <h2>👥 نظام لجنة الاستثمار البلدية</h2>
        <p>إدارة لجان الاستثمار وتحديد القيم الإيجارية حسب اللوائح</p>
    </div>
    """, unsafe_allow_html=True)
    
    committee_system = InvestmentCommitteeSystem()
    
    # تبويبات اللجنة
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 تشكيل اللجنة",
        "💰 تحديد القيمة",
        "📊 قرارات اللجنة",
        "📈 الإحصائيات"
    ])
    
    with tab1:
        render_committee_formation(committee_system)
    
    with tab2:
        render_rental_valuation(committee_system)
    
    with tab3:
        render_committee_decisions(committee_system)
    
    with tab4:
        render_committee_statistics(committee_system)

def render_committee_formation(committee_system):
    """تشكيل لجنة استثمار"""
    
    st.markdown("""
    ### 📋 تشكيل لجنة الاستثمار
    
    **المصدر:** المادة 17 من اللائحة
    """)
    
    with st.form("committee_formation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            municipality = st.text_input("اسم البلدية", value="بلدية المثال")
            site_code = st.text_input("رقم الموقع")
        
        with col2:
            formation_date = st.date_input("تاريخ التشكيل", datetime.now())
            committee_type = st.selectbox("نوع اللجنة", ["لجنة استثمار", "لجنة تقدير", "لجنة فتح المظاريف"])
        
        if st.form_submit_button("👥 تشكيل اللجنة", use_container_width=True):
            # بيانات افتراضية للموقع
            site_data = {
                'site_code': site_code,
                'municipality': municipality
            }
            
            committee = committee_system.form_committee(municipality, site_data)
            st.session_state.active_committee = committee
            
            st.success(f"✅ تم تشكيل لجنة الاستثمار برقم: {committee['id']}")
            
            # عرض تفاصيل اللجنة
            with st.expander("📄 تفاصيل تشكيل اللجنة", expanded=True):
                st.write(f"**رقم اللجنة:** {committee['id']}")
                st.write(f"**تاريخ التشكيل:** {committee['formation_date']}")
                st.write(f"**البلدية:** {committee['municipality']}")
                
                st.markdown("**أعضاء اللجنة:**")
                for member in committee['members']:
                    st.write(f"- {member['name']} ({member['role']})")

def render_rental_valuation(committee_system):
    """تحديد القيمة الإيجارية"""
    
    st.markdown("""
    ### 💰 تحديد القيمة الإيجارية
    
    **المصدر:** المادة 17 من اللائحة
    """)
    
    if 'active_committee' not in st.session_state:
        st.warning("⚠️ يرجى تشكيل لجنة استثمار أولاً")
        return
    
    with st.form("rental_valuation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            site_name = st.text_input("اسم الموقع")
            site_area = st.number_input("المساحة (م²)", min_value=1.0, value=1000.0)
            city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة"])
        
        with col2:
            lease_type = st.selectbox("نوع التأجير", [
                "تأجير مؤقت",
                "تأجير طويل الأجل",
                "تأجير مباشر",
                "عقار مستثنى"
            ])
            
            market_rate = st.number_input("متوسط سعر السوق (ريال/م²/شهر)", min_value=0.0, value=50.0)
        
        if st.form_submit_button("💰 تحديد القيمة", use_container_width=True):
            # بيانات الموقع
            site_data = {
                'name': site_name,
                'area': site_area,
                'city': city,
                'lease_type': lease_type
            }
            
            # تحويل نوع التأجير للرمز الداخلي
            lease_type_map = {
                "تأجير مؤقت": "TEMPORARY_ACTIVITY",
                "تأجير طويل الأجل": "LONG_TERM_INVESTMENT",
                "تأجير مباشر": "DIRECT_LEASE",
                "عقار مستثنى": "EXEMPTED_FROM_COMPETITION"
            }
            
            internal_type = lease_type_map.get(lease_type, "TEMPORARY_ACTIVITY")
            
            # تحديد القيمة
            decision = committee_system.determine_rental_value(
                st.session_state.active_committee['id'],
                site_data,
                internal_type
            )
            
            st.session_state.committee_decision = decision
            
            st.success("✅ اتخذت اللجنة قراراً بالقيمة الإيجارية")
            
            # عرض القرار
            if decision.get('proposed_rent'):
                st.metric("الإيجار المقترح", f"{decision['proposed_rent']['monthly_total']:,.0f} ريال/شهر")
                st.metric("السعر الاسترشادي", f"{decision['guide_price']:,.0f} ريال/شهر")
                
                if decision.get('requires_minister_approval'):
                    st.warning("⚠️ هذا القرار يحتاج موافقة الوزير")

def render_committee_decisions(committee_system):
    """قرارات لجنة الاستثمار"""
    
    st.markdown("""
    ### 📊 قرارات لجنة الاستثمار
    """)
    
    # عرض القرارات السابقة (بيانات افتراضية)
    decisions_data = [
        {"القرار": "2024/001", "التاريخ": "2024-01-15", "المبلغ": "85,000", "الحالة": "معتمد"},
        {"القرار": "2024/002", "التاريخ": "2024-02-20", "المبلغ": "120,000", "الحالة": "قيد المراجعة"},
        {"القرار": "2024/003", "التاريخ": "2024-03-10", "المبلغ": "95,500", "الحالة": "معتمد"},
        {"القرار": "2024/004", "التاريخ": "2024-03-25", "المبلغ": "150,000", "الحالة": "يحتاج موافقة الوزير"},
    ]
    
    df = pd.DataFrame(decisions_data)
    st.dataframe(df, use_container_width=True)
    
    # عرض القرار الحالي إذا وجد
    if 'committee_decision' in st.session_state:
        st.markdown("---")
        st.subheader("📜 القرار الحالي")
        
        decision = st.session_state.committee_decision
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**رقم القرار:** {decision.get('id', 'غير محدد')}")
            st.write(f"**تاريخ القرار:** {decision.get('decision_date', 'غير محدد')[:10]}")
            st.write(f"**نوع التأجير:** {decision.get('lease_type', 'غير محدد')}")
        
        with col2:
            if decision.get('proposed_rent'):
                st.write(f"**الإيجار الشهري:** {decision['proposed_rent']['monthly_total']:,.0f} ريال")
                st.write(f"**ريال/م²/شهر:** {decision['proposed_rent']['monthly_per_m2']:,.1f} ريال")
            
            if decision.get('requires_minister_approval'):
                st.error("**يتطلب موافقة الوزير**")

def render_committee_statistics(committee_system):
    """إحصائيات لجنة الاستثمار"""
    
    st.markdown("""
    ### 📈 إحصائيات لجنة الاستثمار
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("عدد القرارات", "24")
    
    with col2:
        st.metric("متوسط الإيجار", "92,500")
    
    with col3:
        st.metric("أعلى قرار", "150,000")
    
    with col4:
        st.metric("قرارات تحتاج وزير", "3")
    
    # رسم بياني افتراضي
    st.markdown("---")
    st.subheader("📊 توزيع القرارات حسب الشهر")
    
    chart_data = pd.DataFrame({
        'الشهر': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو'],
        'عدد القرارات': [4, 6, 8, 3, 3],
        'متوسط القيمة': [85000, 92000, 105000, 78000, 95000]
    })
    
    fig = px.bar(chart_data, x='الشهر', y='عدد القرارات', 
                 title='عدد القرارات الشهرية',
                 color='عدد القرارات')
    st.plotly_chart(fig, use_container_width=True)

def render_regulations_page():
    """صفحة اللوائح والضوابط"""
    
    st.markdown("""
    <div class="section-header">
        <h2>📋 اللوائح والضوابط البلدية</h2>
        <p>مرجع شامل للوائح والضوابط المعمول بها</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات اللوائح
    tab1, tab2, tab3 = st.tabs([
        "📄 لائحة التصرف بالعقارات",
        "⚖️ ضوابط التأجير المؤقت",
        "📝 التعليمات التنفيذية"
    ])
    
    with tab1:
        render_main_regulations()
    
    with tab2:
        render_temporary_lease_regulations()
    
    with tab3:
        render_executive_instructions()

def render_main_regulations():
    """عرض اللائحة الرئيسية"""
    
    st.markdown("""
    ### 📄 لائحة التصرف بالعقارات البلدية
    
    **رقم اللائحة:** الصادرة بالأمر السامي الكريم رقم (40152)
    **تاريخ الإصدار:** 29/6/1441هـ
    """)
    
    regulations = [
        ("المادة 10", "العقارات المستثناة من المنافسة العامة", "تحدد العقارات التي لا تخضع للمنافسة العامة"),
        ("المادة 21", "مدد عقود الاستثمار", "تحدد المدد القصوى لأنواع العقود المختلفة"),
        ("المادة 27", "التأجير المباشر", "شروط وإجراءات التأجير المباشر"),
        ("المادة 31", "العقود الموحدة", "إلزامية استخدام النماذج المعتمدة"),
    ]
    
    for reg in regulations:
        with st.expander(f"{reg[0]}: {reg[1]}", expanded=False):
            st.write(reg[2])
            st.info(f"للتفاصيل الكاملة، راجع {reg[0]} من اللائحة")

def render_temporary_lease_regulations():
    """عرض ضوابط التأجير المؤقت"""
    
    st.markdown("""
    ### ⚖️ ضوابط تأجير العقارات البلدية لغرض إقامة أنشطة أو فعاليات مؤقتة
    
    **رقم القرار:** قرار وزاري
    **تاريخ الإصدار:** 2023
    """)
    
    st.markdown("""
    **الضوابط الرئيسية:**
    
    1. **المادة 3:** لا تزيد مدة التأجير المؤقت عن 6 أشهر
    2. **المادة 4:** يجوز التمديد لمدد لا تتعدى في مجموعها 6 أشهر
    3. **المادة 5:** الأولوية للمستثمر الذي لم يسبق له الاستئجار المؤقت
    4. **المادة 13:** استخدام نموذج العقد الموحد
    
    **الأنشطة المشمولة:**
    - الفعاليات والمهرجانات
    - المؤتمرات والمناسبات
    - الفعاليات الترويجية
    - الأنشطة الموسمية
    """)

def render_executive_instructions():
    """عرض التعليمات التنفيذية"""
    
    st.markdown("""
    ### 📝 التعليمات التنفيذية للائحة التصرف بالعقارات البلدية
    
    **رقم القرار:** 4100561883
    **تاريخ الإصدار:** 22/12/1441هـ
    """)
    
    instructions = [
        ("المادة 34", "العقارات المستثناة من المنافسة", "تفصيل العقارات المعفاة من المنافسة العامة"),
        ("المادة 46", "السعر الاسترشادي", "تحديد السعر الأدنى للتأجير المباشر"),
        ("المادة 20", "لجنة الاستثمار", "تكوين واختصاصات لجنة الاستثمار"),
    ]
    
    for inst in instructions:
        with st.expander(f"{inst[0]}: {inst[1]}", expanded=False):
            st.write(inst[2])

class EnhancedSiteRentalValuation(SiteRentalValuation):
    """نسخة محسنة من نظام التقييم تتوافق مع اللوائح"""
    
    def render_enhanced_valuation(self):
        """واجهة التقييم المحسنة"""
        
        # تبويبات النظام المحسن
        tab1, tab2, tab3 = st.tabs([
            "📋 معلومات الموقع",
            "💰 التقييم الإيجاري",
            "📄 العقد والموافقات"
        ])
        
        with tab1:
            self.render_site_info_tab()
        
        with tab2:
            self.render_valuation_tab()
        
        with tab3:
            self.render_contract_tab()
    
    def render_site_info_tab(self):
        """تبويب معلومات الموقع"""
        
        st.subheader("📍 معلومات الموقع الأساسية")
        
        with st.form("site_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                site_name = st.text_input("اسم الموقع الرسمي")
                site_code = st.text_input("رقم الموقع (إن وجد)")
                site_area = st.number_input("مساحة الموقع (م²)", min_value=1.0, value=1000.0)
                frontage = st.number_input("طول الواجهة (م)", min_value=0.0, value=20.0)
            
            with col2:
                city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الشرقية"])
                district = st.text_input("الحي / المنطقة")
                zoning = st.selectbox("التصنيف البلدي", ["سكني", "تجاري", "صناعي", "زراعي", "سياحي", "مختلط"])
                allowed_uses = st.text_area("الاستخدامات المسموحة")
            
            if st.form_submit_button("💾 حفظ معلومات الموقع", use_container_width=True):
                st.session_state.site_info = {
                    'name': site_name,
                    'code': site_code,
                    'area': site_area,
                    'frontage': frontage,
                    'city': city,
                    'district': district,
                    'zoning': zoning,
                    'allowed_uses': allowed_uses
                }
                st.success("✅ تم حفظ معلومات الموقع")
    
    def render_valuation_tab(self):
        """تبويب التقييم الإيجاري"""
        
        st.subheader("💰 التقييم الإيجاري المتوافق")
        
        if 'site_info' not in st.session_state:
            st.warning("⚠️ يرجى إدخال معلومات الموقع أولاً")
            return
        
        site_info = st.session_state.site_info
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            **معلومات الموقع:**
            - الاسم: {site_info.get('name', 'غير محدد')}
            - الموقع: {site_info.get('city', '')} - {site_info.get('district', '')}
            - المساحة: {site_info.get('area', 0):,.0f} م²
            - التصنيف: {site_info.get('zoning', 'غير محدد')}
            """)
        
        with col2:
            lease_type = st.session_state.selected_lease_type
            details = MunicipalLeaseTypes().get_lease_type_details(
                lease_type,
                st.session_state.selected_subtype
            )
            
            if details:
                if 'max_duration_months' in details:
                    st.metric("المدة المسموحة", f"{details['max_duration_months']} شهر")
                elif 'max_years' in details:
                    st.metric("المدة المسموحة", f"{details['max_years']} سنة")
        
        # تقدير الإيجار
        st.markdown("---")
        st.subheader("📊 تقدير القيمة الإيجارية")
        
        col_val1, col_val2 = st.columns(2)
        
        with col_val1:
            market_rate = st.number_input("متوسط سعر السوق (ريال/م²/شهر)", 
                                         min_value=0.0, value=50.0)
            adjustment = st.slider("تعديل القيمة %", -30, 50, 0)
        
        with col_val2:
            base_rent = market_rate * site_info.get('area', 0)
            adjusted_rent = base_rent * (1 + adjustment/100)
            
            st.metric("الإيجار الأساسي", f"{base_rent:,.0f} ريال/شهر")
            st.metric("بعد التعديل", f"{adjusted_rent:,.0f} ريال/شهر")
        
        # زر التقديم للجنة
        st.markdown("---")
        if st.button("📥 تقديم للجنة الاستثمار", use_container_width=True, type="primary"):
            st.session_state.valuation_submitted = {
                'site_info': site_info,
                'proposed_rent': adjusted_rent,
                'submission_date': datetime.now().isoformat()
            }
            st.success("✅ تم تقديم التقييم للجنة الاستثمار")
    
    def render_contract_tab(self):
        """تبويب العقد والموافقات"""
        
        st.subheader("📄 العقد والموافقات النظامية")
        
        if 'valuation_submitted' not in st.session_state:
            st.info("📭 لم يتم تقديم أي تقييم بعد")
            return
        
        submission = st.session_state.valuation_submitted
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **حالة التقييم:**
            - ✅ تم تقديم التقييم
            - ⏳ بانتظار لجنة الاستثمار
            - 📋 يتبع اللوائح البلدية
            """)
        
        with col2:
            st.metric("القيمة المقترحة", 
                     f"{submission['proposed_rent']:,.0f} ريال/شهر")
            st.caption(f"التقديم: {submission['submission_date'][:10]}")
        
        # معلومات العقد
        st.markdown("---")
        st.subheader("📋 معلومات العقد")
        
        with st.expander("نموذج العقد حسب اللوائح", expanded=True):
            st.markdown(f"""
            **عقد تأجير عقار بلدي - النموذج الموحد**
            
            **رقم العقد:** CONTRACT-{datetime.now().strftime('%Y%m%d')}
            **تاريخ العقد:** {datetime.now().strftime('%Y-%m-%د')}
            
            **أطراف العقد:**
            1. **المؤجر:** البلدية
            2. **المستأجر:** [اسم المستأجر]
            
            **موضوع العقد:** {submission['site_info'].get('name', 'موقع بلدي')}
            
            **المساحة:** {submission['site_info'].get('area', 0):,.0f} م²
            **المدة:** حسب نوع التأجير المحدد
            **القيمة الإيجارية:** {submission['proposed_rent']:,.0f} ريال/شهر
            
            **شروط خاصة:**
            - يخضع العقد لأحكام لائحة التصرف بالعقارات البلدية
            - يتم استخدام النموذج الموحد المعتمد
            """)
        
        # خيارات التوقيع
        st.markdown("---")
        col_sign1, col_sign2, col_sign3 = st.columns(3)
        
        with col_sign1:
            if st.button("🖋️ إعداد للتوقيع", use_container_width=True):
                st.info("جاري إعداد العقد للتوقيع...")
        
        with col_sign2:
            if st.button("📥 تحميل المسودة", use_container_width=True):
                st.success("تم تحميل مسودة العقد")
        
        with col_sign3:
            if st.button("📧 إرسال للموافقة", use_container_width=True):
                st.success("تم إرسال العقد لإجراءات الموافقة")

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
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-avatar">
                <span class="avatar-icon">👤</span>
            </div>
            <h3>{st.session_state.user_name}</h3>
            <p class="role-badge">{st.session_state.user_role.upper()}</p>
            <p class="profile-stats">📍 عضو منذ: يناير 2024</p>
            <p class="profile-stats">📋 صلاحية: {st.session_state.user_role}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.subheader("🛠️ إعدادات الحساب")
            
            tabs = st.tabs(["معلوماتي", "الأمان", "التفضيلات", "الصلاحيات"])
            
            with tabs[0]:
                with st.form("profile_form"):
                    name = st.text_input("الاسم الكامل", value=st.session_state.user_name)
                    email = st.text_input("البريد الإلكتروني", placeholder="example@domain.com")
                    phone = st.text_input("رقم الهاتف", placeholder="+966 5X XXX XXXX")
                    department = st.text_input("القسم / الإدارة", placeholder="قسم التقييم العقاري")
                    
                    if st.form_submit_button("💾 حفظ التغييرات"):
                        st.success("✅ تم حفظ التغييرات بنجاح")
            
            with tabs[1]:
                st.info("🔒 ميزات الأمان قريباً...")
            
            with tabs[2]:
                st.info("🎨 تخصيص الواجهة قريباً...")
            
            with tabs[3]:
                if st.session_state.user_role == 'admin':
                    st.success("✅ لديك صلاحيات مدير النظام")
                elif st.session_state.user_role == 'evaluator':
                    st.info("👨‍💼 لديك صلاحيات مقيم عقاري")
                else:
                    st.warning("👀 لديك صلاحيات محدودة للعرض فقط")

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
