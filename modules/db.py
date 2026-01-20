import sqlite3
import pandas as pd
import streamlit as st
import json

def init_db():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    # جدول الصفقات
    cursor.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, area REAL, 
        price REAL, deal_date DATE, latitude REAL, longitude REAL, activity_type TEXT, 
        notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # جدول الإعدادات
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit()
    conn.close()

def ensure_settings():
    """تثبيت كافة معدلات النظام في قاعدة البيانات للتحكم بها من الإدارة"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    defaults = [
        ('system_name', 'نظام التقييم الإيجاري البلدي'),
        ('mult_temporary', '0.85'),
        ('mult_long_term', '1.60'),
        ('mult_direct', '1.25'),
        ('mult_exempt', '1.10'),
        ('construction_cost_m2', '3500'),
        ('default_discount_rate', '0.10'),
        ('default_yield', '0.08')
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
