def detect_device_type():
    """كشف نوع الجهاز بشكل آمن دون التسبب في تعطل التطبيق"""
    try:
        # الحصول على User-Agent من ترويسات الطلب (متاحة في إصدارات Streamlit الحديثة)
        # نستخدم .get للحماية في حال لم يكن المفتاح موجوداً
        headers = st.context.headers
        user_agent = headers.get("User-Agent", "")
    except Exception:
        # في حال حدوث أي خطأ في الوصول للترويسات، نضع قيمة فارغة
        user_agent = ""

    mobile_keywords = ['Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone']
    
    # التحقق مما إذا كان المستخدم يدخل من جوال
    is_mobile = any(keyword.lower() in user_agent.lower() for keyword in mobile_keywords)
    
    # حفظ النتيجة في جلسة العمل (Session State) لاستخدامها في التصميم المتجاوب
    if is_mobile:
        st.session_state['device_type'] = 'mobile'
    else:
        st.session_state['device_type'] = 'desktop'

    return st.session_state['device_type']
