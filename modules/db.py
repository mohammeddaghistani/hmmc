import sqlite3
import pandas as pd
from datetime import datetime
import json
import streamlit as st

def init_db():
    """تهيئة قاعدة البيانات بكافة الجداول الأصلية والمحدثة"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    # جدول الصفقات (يدعم الإحداثيات)
    cursor.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, 
        area REAL, price REAL, deal_date DATE, latitude REAL, longitude REAL, 
        activity_type TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # جدول التقييمات
    cursor.execute('''CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, deal_id INTEGER, property_address TEXT, 
        property_type TEXT, estimated_value REAL, confidence_score REAL, 
        confidence_level TEXT, evaluation_method TEXT, similar_deals TEXT, 
        notes TEXT, status TEXT DEFAULT 'pending', created_by TEXT, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (deal_id) REFERENCES deals (id))''')
    # جدول الإعدادات للتحكم في المعدلات
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit()
    conn.close()

def ensure_settings():
    """تثبيت معدلات النظام الأصلية في قاعدة البيانات للتحكم بها من واجهة الإدارة"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    defaults = [
        ('system_name', 'نظام التقييم الإيجاري البلدي'),
        ('mult_temp', '0.85'),  # معامل التأجير المؤقت
        ('mult_long', '1.60'),  # معامل الاستثمار طويل الأجل
        ('mult_direct', '1.25'), # معامل التأجير المباشر
        ('const_cost', '3500'), # تكلفة البناء للمتر
        ('discount_rate', '0.10') # معدل الخصم DCF
    ]
    for key, value in defaults:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else default

def update_setting(key, value):
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
    conn.commit()
    conn.close()

def add_deal(deal_data):
    """إضافة صفقة مع الإحداثيات الجغرافية"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO deals (property_type, location, area, price, deal_date, latitude, longitude, activity_type, notes) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (deal_data['property_type'], deal_data['location'], deal_data['area'], 
                    deal_data['price'], deal_data['deal_date'], deal_data.get('latitude'), 
                    deal_data.get('longitude'), deal_data['activity_type'], deal_data.get('notes', '')))
    deal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    st.cache_data.clear()
    return deal_id

@st.cache_data(ttl=600)
def get_recent_deals(limit=10):
    conn = sqlite3.connect('rental_evaluation.db')
    df = pd.read_sql_query(f'SELECT * FROM deals ORDER BY deal_date DESC LIMIT {limit}', conn)
    conn.close()
    return df
