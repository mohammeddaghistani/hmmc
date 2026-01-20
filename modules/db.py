import sqlite3
import pandas as pd
from datetime import datetime
import json
import streamlit as st

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول إذا لم تكن موجودة"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    # 1. جدول الصفقات (يدعم الإحداثيات الجغرافية) 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_type TEXT,
        location TEXT,
        area REAL,
        price REAL,
        deal_date DATE,
        latitude REAL,
        longitude REAL,
        activity_type TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 2. جدول التقييمات 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER,
        property_address TEXT,
        property_type TEXT,
        estimated_value REAL,
        confidence_score REAL,
        confidence_level TEXT,
        evaluation_method TEXT,
        similar_deals TEXT,
        notes TEXT,
        status TEXT DEFAULT 'pending',
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (deal_id) REFERENCES deals (id)
    )
    ''')
    
    # 3. جدول الإعدادات (ضروري لعمل النظام) 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 4. جدول المستخدمين 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT,
        full_name TEXT,
        email TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def ensure_settings():
    """
    إضافة الإعدادات الافتراضية للنظام في حال عدم وجودها.
    هذه الدالة تحل مشكلة ImportError التي ظهرت لك سابقا. 
    """
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    default_settings = [
        ('system_name', 'نظام التقييم الإيجاري'),
        ('company_name', 'شركة التقييم العقاري'),
        ('default_currency', 'ريال سعودي'),
        ('confidence_threshold', '0.7'),
        ('max_similar_deals', '10')
    ]
    
    for key, value in default_settings:
        cursor.execute('''
        INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
    
    conn.commit()
    conn.close()

def add_deal(deal_data):
    """
    إضافة صفقة جديدة مع حفظ الإحداثيات الجغرافية المستخرجة من الخريطة. 
    """
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO deals (
        property_type, location, area, price, deal_date, 
        latitude, longitude, activity_type, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        deal_data.get('property_type'),
        deal_data.get('location'),
        deal_data.get('area'),
        deal_data.get('price'),
        deal_data.get('deal_date'),
        deal_data.get('latitude'), # حفظ خط العرض 
        deal_data.get('longitude'), # حفظ خط الطول 
        deal_data.get('activity_type'),
        deal_data.get('notes', '')
    ))
    
    deal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # مسح التخزين المؤقت لتحديث البيانات في لوحة التحكم
    st.cache_data.clear()
    return deal_id

@st.cache_data(ttl=600)
def get_recent_deals(limit=10):
    """جلب أحدث الصفقات مع تفعيل التخزين المؤقت لتسريع الأداء."""
    conn = sqlite3.connect('rental_evaluation.db')
    df = pd.read_sql_query(f'''
    SELECT * FROM deals 
    ORDER BY deal_date DESC 
    LIMIT {limit}
    ''', conn)
    conn.close()
    return df

def get_setting(key):
    """الحصول على قيمة إعداد معين من الجدول."""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
