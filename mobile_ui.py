import streamlit as st
import pandas as pd
from datetime import datetime

class MobileUI:
    """واجهة المستخدم المخصصة للأجهزة المتنقلة"""
    
    def __init__(self):
        self.pages = {
            'dashboard': self.render_mobile_dashboard,
            'evaluation': self.render_mobile_evaluation,
            'site_rental': self.render_mobile_site_rental,
            'lease_types': self.render_mobile_lease_types,
            'committee': self.render_mobile_committee,
            'maps': self.render_mobile_maps,
            'reports': self.render_mobile_reports,
            'settings': self.render_mobile_settings,
            'admin': self.render_mobile_admin,
            'profile': self.render_mobile_profile
        }
    
    def render_page(self, page_name):
        """عرض الصفحة المطلوبة"""
        if page_name in self.pages:
            self.pages[page_name]()
        else:
            self.render_mobile_dashboard()
    
    def render_mobile_dashboard(self):
        """لوحة تحكم الموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>📱 لوحة التحكم</h1>
            <p>مرحباً بك في النسخة المتنقلة</p>
        </div>
        """, unsafe_allow_html=True)
        
        # بطاقات سريعة
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_mobile_card("📊 التقييمات", "24", "#4CAF50", "هذا الشهر")
        
        with col2:
            self.render_mobile_card("💰 القيمة", "4.2M", "#2196F3", "إجمالي")
        
        col3, col4 = st.columns(2)
        
        with col3:
            self.render_mobile_card("👥 المستخدمين", "18", "#FF9800", "نشطين")
        
        with col4:
            self.render_mobile_card("📈 النمو", "18%", "#9C27B0", "هذا العام")
        
        # الإجراءات السريعة
        st.markdown("### 🚀 إجراءات سريعة")
        
        quick_actions = [
            ("➕ تقييم جديد", "evaluation"),
            ("📋 تقرير سريع", "reports"),
            ("🗺️ عرض الخريطة", "maps"),
            ("⚙️ الإعدادات", "settings")
        ]
        
        cols = st.columns(2)
        for i, (label, page) in enumerate(quick_actions):
            with cols[i % 2]:
                if st.button(label, use_container_width=True):
                    st.session_state.current_page = page
                    st.rerun()
        
        # النشاط الأخير
        st.markdown("### 📝 النشاط الأخير")
        
        activities = [
            {"النشاط": "تقييم عقار", "الوقت": "قبل 10 دقائق", "المستخدم": "أنت"},
            {"النشاط": "تقرير مالي", "الوقت": "قبل 30 دقيقة", "المستخدم": "أحمد"},
            {"النشاط": "تعديل إعدادات", "الوقت": "قبل ساعة", "المستخدم": "أنت"},
            {"النشاط": "إضافة مستخدم", "الوقت": "قبل ساعتين", "المستخدم": "مدير"},
        ]
        
        for activity in activities:
            with st.container():
                st.write(f"**{activity['النشاط']}**")
                st.caption(f"{activity['الوقت']} | بواسطة {activity['المستخدم']}")
                st.markdown("---")
    
    def render_mobile_card(self, title, value, color, subtitle):
        """عرض بطاقة متنقلة"""
        
        st.markdown(f"""
        <div style="background: {color}; color: white; padding: 20px; border-radius: 15px; 
                    text-align: center; margin: 5px 0;">
            <div style="font-size: 24px; margin-bottom: 10px;">{title}</div>
            <div style="font-size: 32px; font-weight: bold; margin: 10px 0;">{value}</div>
            <div style="font-size: 14px; opacity: 0.8;">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_mobile_evaluation(self):
        """تقييم الموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>📈 التقييم العقاري</h1>
            <p>تقييم سريع ومبسط للعقارات</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("mobile_evaluation_form"):
            st.markdown("#### 📋 معلومات العقار")
            
            property_type = st.selectbox("نوع العقار", ["سكني", "تجاري", "صناعي", "زراعي"])
            area = st.number_input("المساحة (م²)", min_value=1, value=100)
            location = st.text_input("الموقع", placeholder="أدخل العنوان")
            
            st.markdown("#### 💰 معلومات التقييم")
            
            col_val1, col_val2 = st.columns(2)
            with col_val1:
                market_rate = st.number_input("سعر السوق", value=1000)
            with col_val2:
                condition = st.slider("الحالة %", 0, 100, 80)
            
            if st.form_submit_button("📊 حساب التقييم", use_container_width=True):
                valuation = area * market_rate * (condition / 100)
                st.success(f"✅ التقييم المقدر: {valuation:,.0f} ريال")
    
    def render_mobile_site_rental(self):
        """القيمة الإيجارية للموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>📍 القيمة الإيجارية</h1>
            <p>حساب سريع للإيجارات</p>
        </div>
        """, unsafe_allow_html=True)
        
        lease_type = st.selectbox("نوع التأجير", [
            "مؤقت (6 أشهر)",
            "طويل الأجل",
            "مباشر",
            "مستثنى"
        ])
        
        with st.form("mobile_rental_form"):
            area = st.number_input("مساحة الموقع (م²)", min_value=1, value=100)
            location_class = st.select_slider("فئة الموقع", ["منخفض", "متوسط", "مرتفع", "متميز"])
            services = st.multiselect("الخدمات", ["كهرباء", "ماء", "صرف صحي", "إنترنت", "حراسة"])
            
            if st.form_submit_button("💰 حساب الإيجار", use_container_width=True):
                # حساب مبسط
                base_rate = 50
                location_multiplier = {"منخفض": 0.7, "متوسط": 1.0, "مرتفع": 1.3, "متميز": 1.7}
                services_bonus = len(services) * 10
                
                monthly_rent = area * base_rate * location_multiplier[location_class] + services_bonus
                st.success(f"✅ الإيجار الشهري المقدر: {monthly_rent:,.0f} ريال")
    
    def render_mobile_lease_types(self):
        """أنواع التأجير للموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>🏛️ أنواع التأجير</h1>
            <p>اختر النوع المناسب للعقار</p>
        </div>
        """, unsafe_allow_html=True)
        
        lease_types = [
            ("🎪 مؤقت", "6 أشهر للأنشطة المؤقتة", "المادة 3"),
            ("🏗️ طويل الأجل", "10-50 سنة للمشاريع", "المادة 21"),
            ("🎯 مباشر", "بعد إعلانات متكررة", "المادة 27"),
            ("⚖️ مستثنى", "من المنافسة العامة", "المادة 10")
        ]
        
        for lease_name, lease_desc, regulation in lease_types:
            with st.expander(f"{lease_name} - {regulation}", expanded=False):
                st.write(lease_desc)
                if st.button(f"اختيار {lease_name}", key=f"mobile_{lease_name}", use_container_width=True):
                    st.success(f"تم اختيار {lease_name}")
    
    def render_mobile_committee(self):
        """لجنة الاستثمار للموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>👥 لجنة الاستثمار</h1>
            <p>إدارة مبسطة للجنة</p>
        </div>
        """, unsafe_allow_html=True)
        
        action = st.selectbox("الإجراء", [
            "تشكيل لجنة جديدة",
            "تحديد قيمة إيجارية",
            "عرض القرارات",
            "الإحصائيات"
        ])
        
        if action == "تشكيل لجنة جديدة":
            if st.button("👥 تشكيل اللجنة", use_container_width=True):
                st.success("✅ تم تشكيل لجنة الاستثمار")
        
        elif action == "تحديد قيمة إيجارية":
            value = st.number_input("القيمة المقترحة", value=10000)
            if st.button("💰 تقديم للجنة", use_container_width=True):
                st.success(f"✅ تم تقديم القيمة {value:,.0f} ريال")
    
    def render_mobile_maps(self):
        """الخرائط للموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>🗺️ الخرائط</h1>
            <p>عرض المواقع على الخريطة</p>
        </div>
        """, unsafe_allow_html=True)
        
        map_type = st.radio("نوع الخريطة", ["أساسية", "ستلايت", "هجينة"], horizontal=True)
        
        # خريطة افتراضية
        st.markdown("""
        <div style="background: #f0f0f0; border-radius: 10px; padding: 20px; text-align: center; height: 300px;">
            <div style="padding-top: 100px;">
                <h3>📍 خريطة تفاعلية</h3>
                <p>هذه منطقة الخريطة التفاعلية</p>
                <p style="color: #666;">{map_type} - جاري التحميل...</p>
            </div>
        </div>
        """.format(map_type=map_type), unsafe_allow_html=True)
        
        # عناصر تحكم
        col_ctrl1, col_ctrl2 = st.columns(2)
        with col_ctrl1:
            if st.button("📍 تحديد موقعي", use_container_width=True):
                st.info("جاري تحديد الموقع...")
        with col_ctrl2:
            if st.button("🔍 بحث عن موقع", use_container_width=True):
                st.info("جاري البحث...")
    
    def render_mobile_reports(self):
        """التقارير للموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>📑 التقارير</h1>
            <p>تقارير سريعة ومختصرة</p>
        </div>
        """, unsafe_allow_html=True)
        
        report_type = st.selectbox("نوع التقرير", [
            "تقرير التقييمات",
            "تقرير الإيجارات",
            "تقرير المستخدمين",
            "تقرير الإحصائيات"
        ])
        
        period = st.selectbox("الفترة", ["أسبوع", "شهر", "ربع سنة", "سنة"])
        
        if st.button("📊 إنشاء التقرير", use_container_width=True):
            with st.spinner("جاري إنشاء التقرير..."):
                st.success(f"✅ تم إنشاء تقرير {report_type} للفترة {period}")
                
                # معاينة التقرير
                st.markdown("#### 📄 معاينة التقرير")
                st.write(f"**التقرير:** {report_type}")
                st.write(f"**الفترة:** {period}")
                st.write(f"**التاريخ:** {datetime.now().strftime('%Y-%m-%d')}")
                
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    if st.button("📥 تحميل PDF", use_container_width=True):
                        st.success("✅ تم التحميل")
                with col_dl2:
                    if st.button("📧 مشاركة", use_container_width=True):
                        st.success("✅ تم الإرسال")
    
    def render_mobile_settings(self):
        """إعدادات الموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>⚙️ الإعدادات</h1>
            <p>تخصيص تطبيق الموبايل</p>
        </div>
        """, unsafe_allow_html=True)
        
        tabs = st.tabs(["عام", "المظهر", "الإشعارات", "حول"])
        
        with tabs[0]:
            language = st.selectbox("اللغة", ["العربية", "الإنجليزية"])
            dark_mode = st.toggle("الوضع الداكن", value=False)
            auto_save = st.toggle("حفظ تلقائي", value=True)
            
            if st.button("💾 حفظ الإعدادات", use_container_width=True):
                st.success("✅ تم حفظ الإعدادات")
        
        with tabs[1]:
            theme = st.selectbox("السمة", ["افتراضي", "أزرق", "أخضر", "بنفسجي"])
            font_size = st.select_slider("حجم الخط", ["صغير", "متوسط", "كبير"])
            animations = st.toggle("الحركات", value=True)
        
        with tabs[2]:
            notifications = st.toggle("الإشعارات", value=True)
            sound = st.toggle("الصوت", value=False)
            vibration = st.toggle("الاهتزاز", value=True)
        
        with tabs[3]:
            st.write("**إصدار التطبيق:** 2.0.0")
            st.write("**تاريخ البناء:** 2024-01-15")
            st.write("**المطور:** فريق العقارات البلدية")
            
            if st.button("🔄 التحقق من التحديثات", use_container_width=True):
                st.info("✅ أنت تستخدم أحدث إصدار")
    
    def render_mobile_admin(self):
        """إدارة الموبايل (للإدمن فقط)"""
        
        if st.session_state.user_role != "admin":
            st.error("⛔ ليس لديك صلاحية الوصول")
            return
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>👑 لوحة التحكم</h1>
            <p>إدارة النظام من الموبايل</p>
        </div>
        """, unsafe_allow_html=True)
        
        admin_actions = [
            ("👥 إدارة المستخدمين", "users"),
            ("⚙️ إعدادات النظام", "system"),
            ("📊 الإحصائيات", "stats"),
            ("📋 السجلات", "logs")
        ]
        
        cols = st.columns(2)
        for i, (label, action) in enumerate(admin_actions):
            with cols[i % 2]:
                if st.button(label, use_container_width=True):
                    st.info(f"جاري فتح {label}...")
        
        # إجراءات سريعة للإدمن
        st.markdown("### 🚀 إجراءات فورية")
        
        col_quick1, col_quick2 = st.columns(2)
        with col_quick1:
            if st.button("🔄 إعادة تشغيل", use_container_width=True):
                st.warning("⚠️ سيتم إعادة تشغيل النظام")
        with col_quick2:
            if st.button("🧹 تنظيف", use_container_width=True):
                st.success("✅ تم تنظيف النظام")
    
    def render_mobile_profile(self):
        """الملف الشخصي للموبايل"""
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>👤 ملفي الشخصي</h1>
            <p>معلوماتي وإعداداتي</p>
        </div>
        """, unsafe_allow_html=True)
        
        # صورة الملف الشخصي
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div style="font-size: 60px; margin-bottom: 10px;">👤</div>
            <h3>{st.session_state.user_name}</h3>
            <p style="color: #666;">{st.session_state.user_role.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # معلومات سريعة
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("التقييمات", "24")
        with col_info2:
            st.metric("المشاريع", "8")
        
        # تحرير المعلومات
        with st.form("mobile_profile_form"):
            name = st.text_input("الاسم", value=st.session_state.user_name)
            email = st.text_input("البريد الإلكتروني", placeholder="example@domain.com")
            phone = st.text_input("الهاتف", placeholder="+966 XXXXXXXX")
            
            if st.form_submit_button("💾 حفظ التغييرات", use_container_width=True):
                st.success("✅ تم تحديث الملف الشخصي")
        
        # إجراءات سريعة
        st.markdown("### ⚡ إجراءات سريعة")
        
        if st.button("🔐 تغيير كلمة المرور", use_container_width=True):
            st.info("جاري فتح صفحة تغيير كلمة المرور...")
        
        if st.button("📧 تغيير البريد", use_container_width=True):
            st.info("جاري فتح صفحة تغيير البريد...")
        
        if st.button("🚪 تسجيل الخروج", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.rerun()
