import sqlite3
import json
import os
from datetime import datetime

# التأكد من وجود مجلد البيانات لتجنب الأخطاء
if not os.path.exists('data'):
    os.makedirs('data')

DB_PATH = 'data/system.db'

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  name TEXT,
                  email TEXT,
                  role TEXT DEFAULT 'user',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 2. جدول الإعدادات
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY,
                  value TEXT,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # 3. جدول الصفقات/المواقع (الجدول الجديد المطلوب لعمل وظيفة الخريطة)
    c.execute('''CREATE TABLE IF NOT EXISTS deals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  property_type TEXT,
                  location TEXT,
                  area REAL,
                  price REAL,
                  deal_date DATE,
                  latitude REAL,
                  longitude REAL,
                  activity_type TEXT,
                  notes TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    ensure_settings() # التأكد من وجود القيم الافتراضية

def ensure_settings():
    """تأكيد وجود الإعدادات الأساسية"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    default_settings = [
        ('system_name', 'نظام العقارات البلدية'),
        ('version', '2.0.0'),
        ('default_language', 'ar'),
        ('currency', 'ريال سعودي'),
        ('area_unit', 'متر مربع'),
        ('mult_temp', '0.85'),
        ('mult_long', '1.60'),
        ('construction_cost_m2', '3500')
    ]
    
    for key, value in default_settings:
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    
    conn.commit()
    conn.close()

def add_deal(deal_data):
    """إضافة صفقة أو موقع جديد من الخريطة إلى قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        query = '''INSERT INTO deals 
                   (property_type, location, area, price, deal_date, latitude, longitude, activity_type, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        params = (
            deal_data.get('property_type'),
            deal_data.get('location'),
            deal_data.get('area'),
            deal_data.get('price', 0.0),
            deal_data.get('deal_date'),
            deal_data.get('latitude'),
            deal_data.get('longitude'),
            deal_data.get('activity_type'),
            deal_data.get('notes')
        )
        
        c.execute(query, params)
        deal_id = c.lastrowid
        conn.commit()
        conn.close()
        return deal_id
    except Exception as e:
        print(f"Error in add_deal: {e}")
        return None

# --- الدوال المطلوبة لعمل صفحة الإدارة (Admin Panel) ---

def get_setting(key, default=None):
    """جلب قيمة إعداد معين من قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else default
    except Exception as e:
        return default

def update_setting(key, value):
    """تحديث أو إضافة إعداد جديد"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''INSERT OR REPLACE INTO settings (key, value, updated_at) 
                     VALUES (?, ?, ?)''', (key, str(value), now))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating setting: {e}")
        return False
