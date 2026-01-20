import sqlite3
import pandas as pd
from datetime import datetime
import json
import streamlit as st

def init_db():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    # الجداول الأصلية
    cursor.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, 
        area REAL, price REAL, deal_date DATE, latitude REAL, longitude REAL, 
        activity_type TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, deal_id INTEGER, property_address TEXT, 
        property_type TEXT, estimated_value REAL, confidence_score REAL, 
        confidence_level TEXT, evaluation_method TEXT, similar_deals TEXT, 
        notes TEXT, status TEXT DEFAULT 'pending', created_by TEXT, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit(); conn.close()

def ensure_settings():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    defaults = [('system_name', 'نظام التقييم الإيجاري'), ('default_currency', 'ريال سعودي')]
    for key, value in defaults:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit(); conn.close()

def add_deal(deal_data):
    """إضافة صفقة جديدة (المطلوبة في app.py)"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO deals (property_type, location, area, price, deal_date, latitude, longitude, activity_type) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (deal_data['property_type'], deal_data['location'], deal_data['area'], 
                    deal_data['price'], deal_data['deal_date'], deal_data.get('latitude'), 
                    deal_data.get('longitude'), deal_data['activity_type']))
    deal_id = cursor.lastrowid
    conn.commit(); conn.close()
    st.cache_data.clear()
    return deal_id

def add_evaluation(evaluation_data):
    """إضافة تقييم جديد"""
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO evaluations (deal_id, property_address, property_type, estimated_value, 
                      confidence_score, confidence_level, evaluation_method, similar_deals, notes, created_by, status) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (evaluation_data.get('deal_id'), evaluation_data['property_address'], evaluation_data['property_type'],
                    evaluation_data['estimated_value'], evaluation_data['confidence_score'], evaluation_data['confidence_level'],
                    evaluation_data['evaluation_method'], json.dumps(evaluation_data.get('similar_deals', [])),
                    evaluation_data.get('notes', ''), evaluation_data['created_by'], evaluation_data.get('status', 'pending')))
    conn.commit(); conn.close()
