import sqlite3
import pandas as pd
import streamlit as st

@st.cache_data(ttl=600) # تخزين مؤقت لمدة 10 دقائق لتسريع النظام
def get_recent_deals_fast(limit=10):
    """جلب الصفقات بسرعة عالية """
    try:
        conn = sqlite3.connect('rental_evaluation.db')
        df = pd.read_sql_query(f'SELECT * FROM deals ORDER BY deal_date DESC LIMIT {limit}', conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def init_db():
    """تهيئة الجداول (الكود الأصلي دون تغيير) """
    conn = sqlite3.connect('rental_evaluation.db')
    # ... بقية كود إنشاء الجداول كما أرسلته سابقاً ...
    conn.commit()
    conn.close()
