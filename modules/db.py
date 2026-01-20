import sqlite3
import json
from datetime import datetime

def init_db():
    """تهيئة قاعدة البيانات"""
    conn = sqlite3.connect('data/system.db')
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

def ensure_settings():
    """تأكيد وجود الإعدادات الأساسية"""
    conn = sqlite3.connect('data/system.db')
    c = conn.cursor()
    
    default_settings = [
        ('system_name', 'نظام العقارات البلدية'),
        ('version', '2.0.0'),
        ('default_language', 'ar'),
        ('currency', 'ريال سعودي'),
        ('area_unit', 'متر مربع')
    ]
    
    for key, value in default_settings:
        c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    
    conn.commit()
    conn.close()
