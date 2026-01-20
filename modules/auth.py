import hashlib
import sqlite3
from datetime import datetime

def hash_password(password):
    """تشفير كلمة المرور"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(username, password):
    """المصادقة"""
    conn = sqlite3.connect('data/system.db')
    c = conn.cursor()
    
    hashed_password = hash_password(password)
    
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
              (username, hashed_password))
    user = c.fetchone()
    
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'name': user[3],
            'email': user[4],
            'role': user[5]
        }
    return None

def register_user(username, password, name, email, role='user'):
    """تسجيل مستخدم جديد"""
    try:
        conn = sqlite3.connect('data/system.db')
        c = conn.cursor()
        
        hashed_password = hash_password(password)
        
        c.execute('INSERT INTO users (username, password, name, email, role) VALUES (?, ?, ?, ?, ?)',
                  (username, hashed_password, name, email, role))
        
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_all_users():
    """الحصول على جميع المستخدمين"""
    conn = sqlite3.connect('data/system.db')
    c = conn.cursor()
    
    c.execute('SELECT username, name, email, role, created_at FROM users ORDER BY created_at DESC')
    users = c.fetchall()
    
    conn.close()
    
    return [{
        'username': u[0],
        'name': u[1],
        'email': u[2],
        'role': u[3],
        'created_at': u[4]
    } for u in users]

def logout():
    """تسجيل الخروج"""
    return True
