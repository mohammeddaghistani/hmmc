import streamlit as st
import hashlib
import time

# قاعدة بيانات المستخدمين (في بيئة حقيقية تستخدم قاعدة بيانات)
USERS = {
    "admin": {
        "password": "admin123",  # في بيئة حقيقية تستخدم التجزئة
        "role": "admin",
        "name": "المسؤول العام"
    },
    "committee": {
        "password": "committee123",
        "role": "committee",
        "name": "لجنة المراجعة"
    },
    "valuer": {
        "password": "valuer123",
        "role": "valuer",
        "name": "المقيّم العقاري"
    },
    "dataentry": {
        "password": "data123",
        "role": "dataentry",
        "name": "مدخل البيانات"
    }
}

def hash_password(password):
    """تجزئة كلمة المرور"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """المصادقة على المستخدم"""
    if username in USERS:
        # في بيئة حقيقية تقارن كلمات المرور المشفرة
        if USERS[username]["password"] == password:
            return {
                "username": username,
                "role": USERS[username]["role"],
                "name": USERS[username]["name"]
            }
    return None

def login_required(username=None, password=None):
    """التحقق من تسجيل الدخول"""
    if username and password:
        return authenticate(username, password)
    
    # التحقق من حالة الجلسة
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return {
            "username": st.session_state.get('user_name', ''),
            "role": st.session_state.get('user_role', 'guest'),
            "name": st.session_state.get('user_name', 'مستخدم')
        }
    
    return None

def logout():
    """تسجيل الخروج"""
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_name = ""

def check_permission(required_role):
    """التحقق من صلاحية المستخدم"""
    current_role = st.session_state.get('user_role', 'guest')
    
    # ترتيب الأدوار (من الأعلى صلاحية إلى الأقل)
    role_hierarchy = {
        'admin': 4,
        'committee': 3,
        'valuer': 2,
        'dataentry': 1,
        'guest': 0
    }
    
    current_level = role_hierarchy.get(current_role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return current_level >= required_level
