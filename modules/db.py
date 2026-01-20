import sqlite3
import pandas as pd
from datetime import datetime
import json

def init_db():
    """تهيئة قاعدة البيانات"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    # جدول الصفقات
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
    
    # جدول التقييمات
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
    
    # جدول الملفات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evaluation_id INTEGER,
        file_name TEXT,
        file_type TEXT,
        file_path TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (evaluation_id) REFERENCES evaluations (id)
    )
    ''')
    
    # جدول الإعدادات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # جدول المستخدمين
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
    """ضمان وجود الإعدادات الأساسية"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    # إعدادات النظام الأساسية
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

def get_setting(key):
    """الحصول على إعداد"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result[0] if result else None

def add_deal(deal_data):
    """إضافة صفقة جديدة"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO deals (property_type, location, area, price, deal_date, latitude, longitude, activity_type, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        deal_data['property_type'],
        deal_data['location'],
        deal_data['area'],
        deal_data['price'],
        deal_data['deal_date'],
        deal_data.get('latitude'),
        deal_data.get('longitude'),
        deal_data['activity_type'],
        deal_data.get('notes', '')
    ))
    
    deal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return deal_id

def get_recent_deals(limit=10):
    """الحصول على أحدث الصفقات"""
    conn = sqlite3.connect('rental_evaluation.db')
    df = pd.read_sql_query(f'''
    SELECT * FROM deals 
    ORDER BY deal_date DESC 
    LIMIT {limit}
    ''', conn)
    conn.close()
    
    return df

def add_evaluation(evaluation_data):
    """إضافة تقييم جديد"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO evaluations (
        deal_id, property_address, property_type, estimated_value, 
        confidence_score, confidence_level, evaluation_method, 
        similar_deals, notes, created_by, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        evaluation_data.get('deal_id'),
        evaluation_data['property_address'],
        evaluation_data['property_type'],
        evaluation_data['estimated_value'],
        evaluation_data['confidence_score'],
        evaluation_data['confidence_level'],
        evaluation_data['evaluation_method'],
        json.dumps(evaluation_data.get('similar_deals', [])),
        evaluation_data.get('notes', ''),
        evaluation_data['created_by'],
        evaluation_data.get('status', 'pending')
    ))
    
    evaluation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return evaluation_id
