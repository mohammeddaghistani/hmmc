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
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  name TEXT,
                  email TEXT,
                  role TEXT DEFAULT 'user',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # جدول الإعدادات
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY,
                  value TEXT,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    ensure_settings() # التأكد من وجود القيم الافتراضية بعد إنشاء الجدول

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
