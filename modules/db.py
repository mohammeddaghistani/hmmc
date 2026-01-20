import sqlite3
import pandas as pd
import streamlit as st

def init_db():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS deals (id INTEGER PRIMARY KEY AUTOINCREMENT, property_type TEXT, location TEXT, area REAL, price REAL, latitude REAL, longitude REAL)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    conn.commit(); conn.close()

def ensure_settings():
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    defaults = [('mult_temp', '0.85'), ('mult_long', '1.60'), ('mult_direct', '1.25'), ('const_cost', '3500')]
    for k, v in defaults:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))
    conn.commit(); conn.close()

def get_setting(key, default=None):
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else default

def update_setting(key, value):
    conn = sqlite3.connect('rental_evaluation.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
    conn.commit(); conn.close()
