import sqlite3
import pandas as pd
from datetime import datetime
import json
import streamlit as st

def init_db():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    # جدول الصفقات المحدث
    cursor.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, 
        area REAL, price REAL, deal_date DATE, latitude REAL, longitude REAL, 
        activity_type TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # جدول الإعدادات
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit(); conn.close()

def ensure_settings():
    """ضمان وجود الإعدادات لمنع أخطاء التشغيل"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    defaults = [
        ('system_name', 'نظام التقييم الإيجاري'),
        ('company_name', 'شركة التقييم العقاري'),
        ('default_currency', 'ريال سعودي'),
        ('confidence_threshold', '0.7')
    ]
    for key, value in defaults:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit(); conn.close()

def add_deal(deal_data):
    """إضافة صفقة جديدة مع الإحداثيات الجغرافية"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO deals (property_type, location, area, price, deal_date, latitude, longitude, activity_type) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (deal_data['property_type'], deal_data['location'], deal_data['area'], 
                    deal_data['price'], deal_data['deal_date'], deal_data.get('latitude'), 
                    deal_data.get('longitude'), deal_data['activity_type']))
    deal_id = cursor.lastrowid
    conn.commit(); conn.close()
    st.cache_data.clear() # تحديث التخزين المؤقت
    return deal_id

@st.cache_data(ttl=600)
def get_recent_deals(limit=10):
    conn = sqlite3.connect('rental_evaluation.db')
    df = pd.read_sql_query(f'SELECT * FROM deals ORDER BY deal_date DESC LIMIT {limit}', conn)
    conn.close()
    return df
