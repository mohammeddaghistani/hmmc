import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st

def init_db():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    # جدول الصفقات المحدث لدعم الإحداثيات
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
    )''')
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit()
    conn.close()

def ensure_settings():
    """تثبيت الإعدادات الافتراضية لمنع أخطاء النظام"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    defaults = [('system_name', 'نظام التقييم الإيجاري'), ('default_currency', 'ريال سعودي')]
    for key, val in defaults:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, val))
    conn.commit()
    conn.close()

def add_deal(deal_data):
    """إضافة صفقة جديدة مع الإحداثيات"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO deals (property_type, location, area, price, deal_date, latitude, longitude, activity_type, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    (deal_data['property_type'], deal_data['location'], deal_data['area'], 
     deal_data['price'], deal_date['deal_date'], deal_data['latitude'], 
     deal_data['longitude'], deal_data['activity_type'], deal_data['notes']))
    deal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    st.cache_data.clear() # تحديث البيانات في لوحة التحكم
    return deal_id
