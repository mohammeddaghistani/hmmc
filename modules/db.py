import sqlite3
import pandas as pd
import streamlit as st

def init_db():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, 
        area REAL, price REAL, deal_date DATE, latitude REAL, longitude REAL, 
        activity_type TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit(); conn.close()

def ensure_settings():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    defaults = [('system_name', 'نظام التقييم الإيجاري'), ('default_currency', 'ريال سعودي')]
    for k, v in defaults:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))
    conn.commit(); conn.close()

def add_deal(data):
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO deals (property_type, location, area, price, deal_date, latitude, longitude, activity_type) 
                      VALUES (?,?,?,?,?,?,?,?)''', 
                   (data['property_type'], data['location'], data['area'], data['price'], data['deal_date'], data['latitude'], data['longitude'], data['activity_type']))
    deal_id = cursor.lastrowid
    conn.commit(); conn.close()
    st.cache_data.clear()
    return deal_id

@st.cache_data(ttl=600)
def get_recent_deals(limit=10):
    conn = sqlite3.connect('rental_evaluation.db')
    df = pd.read_sql_query(f'SELECT * FROM deals ORDER BY deal_date DESC LIMIT {limit}', conn)
    conn.close()
    return df
