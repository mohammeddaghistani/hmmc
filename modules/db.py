import sqlite3
import streamlit as st

@st.cache_data(ttl=600) # تخزين البيانات لمدة 10 دقائق لتسريع العرض
def get_recent_deals_cached(limit=10):
    conn = sqlite3.connect('rental_evaluation.db')
    # ... كود جلب البيانات الأصلي ...
    conn.close()
    return df
