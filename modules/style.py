import streamlit as st

def apply_custom_style():
    """تطبيق التصميم المخصص"""
    pass  # يتم تطبيق CSS عبر get_custom_css()

def get_custom_css():
    """الحصول على CSS المخصص"""
    return """
    <style>
    /* التصميم الأساسي */
    :root {
        --primary-color: #1e3c72;
        --secondary-color: #2a5298;
        --accent-color: #4CAF50;
        --danger-color: #f44336;
        --warning-color: #FF9800;
        --info-color: #2196F3;
        --light-color: #f8f9fa;
        --dark-color: #343a40;
        --border-radius: 10px;
        --box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        --transition: all 0.3s ease;
    }
    
    /* تصميم متجاوب */
    @media (max-width: 768px) {
        .stApp {
            padding: 10px !important;
        }
        
        .element-container {
            margin-bottom: 15px !important;
        }
        
        .stButton > button {
            width: 100% !important;
            margin: 5px 0 !important;
        }
        
        .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
            width: 100% !important;
        }
    }
    
    @media (max-width: 480px) {
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1 0 auto;
            min-width: 100px;
        }
    }
    
    /* تصميم البطاقات */
    .custom-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 20px;
        margin: 15px 0;
        box-shadow: var(--box-shadow);
        transition: var(--transition);
        border: 1px solid #e0e0e0;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--primary-color);
    }
    
    .card-title {
        color: var(--primary-color);
        margin: 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* أزرار مخصصة */
    .btn-primary {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: var(--border-radius);
        font-weight: bold;
        cursor: pointer;
        transition: var(--transition);
        text-align: center;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 60, 114, 0.3);
    }
    
    .btn-secondary {
        background: white;
        color: var(--primary-color);
        border: 2px solid var(--primary-color);
        padding: 10px 22px;
        border-radius: var(--border-radius);
        font-weight: bold;
        cursor: pointer;
        transition: var(--transition);
    }
    
    .btn-secondary:hover {
        background: var(--primary-color);
        color: white;
    }
    
    /* النماذج */
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-label {
        display: block;
        margin-bottom: 8px;
        font-weight: bold;
        color: var(--dark-color);
    }
    
    .form-control {
        width: 100%;
        padding: 12px;
        border: 2px solid #e0e0e0;
        border-radius: var(--border-radius);
        transition: var(--transition);
        font-size: 16px;
    }
    
    .form-control:focus {
        border-color: var(--primary-color);
        outline: none;
        box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.1);
    }
    
    /* الجداول */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background: var(--primary-color);
        color: white;
        padding: 12px;
        text-align: right;
        font-weight: bold;
    }
    
    .dataframe td {
        padding: 10px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .dataframe tr:hover {
        background: #f5f5f5;
    }
    
    /* العناوين */
    .page-header {
        text-align: center;
        padding: 30px 0;
        margin-bottom: 30px;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border-radius: var(--border-radius);
    }
    
    .page-header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    
    .page-header p {
        margin: 10px 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* التبويبات */
    .custom-tabs {
        margin: 20px 0;
    }
    
    .tab-content {
        padding: 20px;
        background: white;
        border-radius: 0 0 var(--border-radius) var(--border-radius);
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    
    /* التنبيهات */
    .alert {
        padding: 15px;
        border-radius: var(--border-radius);
        margin: 15px 0;
        border-left: 5px solid;
    }
    
    .alert-success {
        background: #d4edda;
        border-left-color: #28a745;
        color: #155724;
    }
    
    .alert-warning {
        background: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }
    
    .alert-danger {
        background: #f8d7da;
        border-left-color: #dc3545;
        color: #721c24;
    }
    
    .alert-info {
        background: #d1ecf1;
        border-left-color: #17a2b8;
        color: #0c5460;
    }
    
    /* الشارات */
    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    
    .badge-primary {
        background: var(--primary-color);
        color: white;
    }
    
    .badge-secondary {
        background: var(--secondary-color);
        color: white;
    }
    
    .badge-success {
        background: var(--accent-color);
        color: white;
    }
    
    .badge-danger {
        background: var(--danger-color);
        color: white;
    }
    
    /* التحسينات للأجهزة المتنقلة */
    .mobile-hidden {
        display: none;
    }
    
    @media (min-width: 769px) {
        .mobile-only {
            display: none;
        }
    }
    
    @media (max-width: 768px) {
        .desktop-only {
            display: none;
        }
        
        .mobile-hidden {
            display: block;
        }
    }
    
    /* تحسينات للقراءة */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        line-height: 1.3;
    }
    
    /* تأثيرات التحميل */
    .loading {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* تخصيص شريط التقدم */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }
    </style>
    """

def get_responsive_css():
    """الحصول على CSS للمجاوبة"""
    return """
    <style>
    /* تحسينات للأجهزة المتنقلة */
    @media (max-width: 768px) {
        /* تحسين الحاويات */
        .main .block-container {
            padding: 1rem !important;
        }
        
        /* تحسين النصوص */
        h1 {
            font-size: 1.8rem !important;
            line-height: 1.2 !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        h3 {
            font-size: 1.3rem !important;
        }
        
        /* تحسين الجداول */
        .dataframe {
            font-size: 12px !important;
        }
        
        .dataframe th,
        .dataframe td {
            padding: 6px !important;
        }
        
        /* تحسين النماذج */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea {
            font-size: 16px !important; /* منع التكبير في iOS */
        }
        
        /* تحسين الأزرار */
        .stButton > button {
            font-size: 16px !important;
            padding: 12px !important;
            margin: 8px 0 !important;
        }
        
        /* تحسين التبويبات */
        .stTabs [data-baseweb="tab-list"] {
            gap: 5px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px !important;
            font-size: 14px !important;
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div {
            font-size: 16px !important;
        }
        
        /* تحسين الشرائح */
        .stSlider > div > div > div {
            padding: 10px 0 !important;
        }
    }
    
    @media (max-width: 480px) {
        /* تحسينات إضافية للشاشات الصغيرة */
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        .stMetric {
            padding: 10px !important;
        }
        
        .stMetric > div {
            font-size: 14px !important;
        }
        
        .stMetric > div > div {
            font-size: 24px !important;
        }
    }
    
    /* تحسينات للوضع الأفقي */
    @media (orientation: landscape) and (max-height: 500px) {
        .main .block-container {
            padding: 0.5rem !important;
        }
        
        .stButton > button {
            padding: 8px !important;
            margin: 4px 0 !important;
        }
    }
    
    /* تحسينات للأجهزة التي تدعم اللمس */
    @media (hover: none) and (pointer: coarse) {
        /* زيادة مساحة اللمس */
        .stButton > button,
        .stCheckbox > label,
        .stRadio > label {
            min-height: 44px !important;
        }
        
        .stSelectbox > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div {
            min-height: 44px !important;
        }
        
        /* تحسين المسافات بين العناصر */
        .element-container {
            margin-bottom: 20px !important;
        }
    }
    
    /* تحسينات للألوان العالية الدقة */
    @media (min-resolution: 192dpi) {
        /* تحسين الحواف */
        .stButton > button,
        .stSelectbox > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div {
            border-width: 1px !important;
        }
    }
    
    /* تحسينات للوضع الداكن */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #64b5f6;
            --secondary-color: #2196f3;
            --light-color: #1e1e1e;
            --dark-color: #ffffff;
        }
        
        body {
            background-color: #121212;
            color: #ffffff;
        }
        
        .custom-card {
            background-color: #1e1e1e;
            border-color: #333;
        }
    }
    </style>
    """
