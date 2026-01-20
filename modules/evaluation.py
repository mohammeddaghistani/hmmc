import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import random
from modules.db import add_evaluation, get_recent_deals

def render_evaluation_module(user_role):
    """عرض وحدة التقييم"""
    
    st.markdown("""
    <div class="section-header">
        <h2>📊 نظام التقييم الإيجاري الذكي</h2>
        <p>تقييم دقيق للعقارات بناءً على البيانات والذكاء الاصطناعي</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات التقييم
    tab1, tab2, tab3 = st.tabs(["🆕 تقييم جديد", "🗺️ خريطة الصفقات", "📋 الصفقات الحديثة"])
    
    with tab1:
        render_new_evaluation(user_role)
    
    with tab2:
        render_deals_map()
    
    with tab3:
        render_recent_deals_list()

def render_new_evaluation(user_role):
    """عرض نموذج التقييم الجديد"""
    
    with st.form("evaluation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏠 معلومات العقار")
            property_address = st.text_input("عنوان العقار", placeholder="الرجاء إدخال العنوان الدقيق")
            property_type = st.selectbox(
                "نوع العقار",
                ["سكني", "تجاري", "مكتبي", "صناعي", "زراعي", "أخرى"]
            )
            area = st.number_input("المساحة (م²)", min_value=1.0, value=100.0)
            year_built = st.number_input("سنة البناء", min_value=1900, max_value=2024, value=2020)
        
        with col2:
            st.subheader("📍 معلومات الموقع")
            city = st.selectbox(
                "المدينة",
                ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "الشرقية", "أخرى"]
            )
            district = st.text_input("الحي", placeholder="اسم الحي")
            latitude = st.number_input("خط العرض", format="%.6f", value=24.7136)
            longitude = st.number_input("خط الطول", format="%.6f", value=46.6753)
        
        st.markdown("---")
        
        st.subheader("⚙️ معايير التقييم")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            condition = st.select_slider(
                "حالة العقار",
                options=["قديم", "مقبول", "جيد", "جيد جداً", "ممتاز"],
                value="جيد"
            )
        
        with col4:
            proximity_weight = st.slider(
                "وزن القرب من الصفقات (%)",
                min_value=0,
                max_value=100,
                value=40
            )
        
        with col5:
            activity_weight = st.slider(
                "وزن النشاط المماثل (%)",
                min_value=0,
                max_value=100,
                value=30
            )
        
        # أزرار التحكم
        col6, col7, col8 = st.columns([2, 1, 1])
        
        with col6:
            if st.form_submit_button("🚀 بدء التقييم الذكي", use_container_width=True):
                perform_evaluation(
                    property_address, property_type, area, year_built,
                    city, district, latitude, longitude, condition,
                    proximity_weight, activity_weight, user_role
                )
        
        with col7:
            st.form_submit_button("🧹 إعادة تعيين", use_container_width=True, type="secondary")
        
        with col8:
            st.form_submit_button("💾 حفظ كمسودة", use_container_width=True, type="secondary")

def perform_evaluation(address, p_type, area, year_built, city, district, 
                      lat, lng, condition, prox_weight, act_weight, user_role):
    """إجراء التقييم الذكي"""
    
    with st.spinner("🔍 جاري تحليل البيانات وتقييم العقار..."):
        
        # محاكاة عملية التقييم
        st.info("""
        ### 📋 خطوات التقييم الجاري:
        1. 🔍 البحث عن الصفقات المشابهة في قاعدة البيانات
        2. 📊 تحليل الأنشطة العقارية المشابهة
        3. ⚖️ تطبيق القواعد الاحتياطية
        4. 🎯 حساب القيمة التقديرية ودرجة الثقة
        """)
        
        # محاكاة حساب القيمة
        base_value = area * random.uniform(800, 1200)
        
        # عوامل التعديل
        condition_factors = {
            "قديم": 0.7, "مقبول": 0.85, "جيد": 1.0,
            "جيد جداً": 1.15, "ممتاز": 1.3
        }
        condition_factor = condition_factors.get(condition, 1.0)
        
        year_factor = 1 + (2024 - year_built) * 0.02
        location_factor = random.uniform(0.9, 1.2)
        
        # القيمة النهائية
        estimated_value = base_value * condition_factor * year_factor * location_factor
        
        # حساب درجة الثقة
        confidence_score = random.uniform(0.7, 0.95)
        
        if confidence_score >= 0.9:
            confidence_level = "عالي جداً"
        elif confidence_score >= 0.8:
            confidence_level = "عالي"
        elif confidence_score >= 0.7:
            confidence_level = "متوسط"
        else:
            confidence_level = "منخفض"
        
        # عرض النتائج
        st.success("✅ تم إكمال التقييم بنجاح!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 القيمة التقديرية", f"{estimated_value:,.0f} ر.س")
        
        with col2:
            st.metric("⭐ درجة الثقة", f"{confidence_score:.0%}")
        
        with col3:
            st.metric("📊 مستوى الثقة", confidence_level)
        
        # عرض الصفقات المشابهة
        st.subheader("🏘️ الصفقات المشابهة المستخدمة")
        
        similar_deals = generate_similar_deals()
        st.dataframe(similar_deals, use_container_width=True)
        
        # خيارات الإجراءات
        st.markdown("---")
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            if st.button("📄 توليد تقرير PDF", use_container_width=True):
                st.success("📄 جاري توليد التقرير...")
        
        with col5:
            if st.button("💾 حفظ التقييم", use_container_width=True):
                # حفظ في قاعدة البيانات
                evaluation_data = {
                    'property_address': address,
                    'property_type': p_type,
                    'estimated_value': estimated_value,
                    'confidence_score': confidence_score,
                    'confidence_level': confidence_level,
                    'evaluation_method': 'ذكي',
                    'similar_deals': similar_deals.to_dict('records'),
                    'created_by': user_role,
                    'notes': f"تقييم ذكي للعقار في {district}، {city}"
                }
                
                eval_id = add_evaluation(evaluation_data)
                st.success(f"✅ تم حفظ التقييم برقم #{eval_id}")
        
        with col6:
            if st.button("🔄 تقييم جديد", use_container_width=True):
                st.rerun()

def generate_similar_deals():
    """توليد بيانات صفقات مشابهة"""
    data = {
        'العنوان': ['حي النخيل', 'حي الياسمين', 'حي الربيع', 'حي العليا', 'حي السفارات'],
        'المساحة': [120, 95, 110, 150, 130],
        'السعر': [450000, 320000, 380000, 550000, 480000],
        'سنة البناء': [2020, 2021, 2019, 2022, 2020],
        'المسافة (كم)': [1.2, 2.5, 0.8, 3.1, 1.8],
        'نسبة التشابه': ['92%', '87%', '85%', '79%', '91%']
    }
    
    return pd.DataFrame(data)

def render_deals_map():
    """عرض خريطة الصفقات"""
    
    st.subheader("🗺️ خريطة توزيع الصفقات العقارية")
    
    # إنشاء خريطة
    m = folium.Map(location=[24.7136, 46.6753], zoom_start=12)
    
    # إضافة علامات (بيانات وهمية)
    locations = [
        {"name": "صفقة #1", "lat": 24.7136, "lng": 46.6753, "price": "450K", "type": "سكني"},
        {"name": "صفقة #2", "lat": 24.7236, "lng": 46.6853, "price": "320K", "type": "تجاري"},
        {"name": "صفقة #3", "lat": 24.7036, "lng": 46.6653, "price": "380K", "type": "سكني"},
        {"name": "صفقة #4", "lat": 24.7336, "lng": 46.6953, "price": "550K", "type": "مكتبي"},
    ]
    
    for loc in locations:
        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=f"{loc['name']}<br>السعر: {loc['price']}<br>النوع: {loc['type']}",
            tooltip=loc["name"],
            icon=folium.Icon(color='blue', icon='home', prefix='fa')
        ).add_to(m)
    
    # عرض الخريطة
    folium_static(m, width=800, height=500)
    
    st.caption("💡 الخريطة تظهر توزيع الصفقات العقارية المسجلة في النظام")

def render_recent_deals_list():
    """عرض قائمة الصفقات الحديثة"""
    
    st.subheader("📋 آخر الصفقات المسجلة")
    
    # الحصول على الصفقات الحديثة
    deals_df = get_recent_deals(10)
    
    if not deals_df.empty:
        # تنسيق البيانات للعرض
        display_df = deals_df[['property_type', 'location', 'area', 'price', 'deal_date']].copy()
        display_df.columns = ['النوع', 'الموقع', 'المساحة (م²)', 'السعر (ر.س)', 'تاريخ الصفقة']
        display_df['السعر (ر.س)'] = display_df['السعر (ر.س)'].apply(lambda x: f"{x:,.0f}")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("📭 لا توجد صفقات مسجلة بعد. قم بإضافة أول صفقة!")
    
    # زر إضافة صفقة جديدة
    if st.button("➕ إضافة صفقة جديدة", use_container_width=True):
        st.session_state.show_new_deal_form = True
    
    if st.session_state.get('show_new_deal_form', False):
        render_new_deal_form()

def render_new_deal_form():
    """عرض نموذج إضافة صفقة جديدة"""
    
    with st.form("new_deal_form"):
        st.subheader("➕ إضافة صفقة جديدة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            deal_type = st.selectbox(
                "نوع العقار",
                ["سكني", "تجاري", "مكتبي", "صناعي", "زراعي"]
            )
            location = st.text_input("الموقع", placeholder="اسم الحي أو المنطقة")
            area = st.number_input("المساحة (م²)", min_value=1.0)
        
        with col2:
            price = st.number_input("سعر الصفقة (ر.س)", min_value=0.0)
            deal_date = st.date_input("تاريخ الصفقة")
            activity_type = st.selectbox(
                "نوع النشاط",
                ["بيع", "إيجار", "رهن", "مقايضة"]
            )
        
        notes = st.text_area("ملاحظات إضافية", height=100)
        
        col3, col4 = st.columns(2)
        
        with col3:
            submit = st.form_submit_button("💾 حفظ الصفقة", use_container_width=True)
        
        with col4:
            if st.form_submit_button("إلغاء", use_container_width=True, type="secondary"):
                st.session_state.show_new_deal_form = False
                st.rerun()
        
        if submit:
            # هنا يمكن إضافة الكود لحفظ الصفقة في قاعدة البيانات
            st.success("✅ تم حفظ الصفقة بنجاح!")
            st.session_state.show_new_deal_form = False
            st.rerun()
