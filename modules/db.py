import sqlite3
import pandas as pd
from datetime import datetime
import json
import streamlit as st

def init_db():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    # جدول الصفقات
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # جدول الإعدادات
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

def ensure_settings():
    """ضمان وجود الإعدادات الأساسية للنظام"""
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
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

@st.cache_data(ttl=600)
def get_recent_deals(limit=10):
    """جلب الصفقات بسرعة عالية مع تخزين مؤقت"""
    conn = sqlite3.connect('rental_evaluation.db')
    df = pd.read_sql_query(f'SELECT * FROM deals ORDER BY deal_date DESC LIMIT {limit}', conn)
    conn.close()
    return df

def get_setting(key):
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
