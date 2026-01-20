import streamlit as st

def apply_custom_style():
    """تطبيق التصميم المخصص على التطبيق"""
    
    st.set_page_config(
        page_title="نظام التقييم الإيجاري",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # إخفاء عناصر Streamlit الافتراضية
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def get_custom_css():
    """إرجاع CSS المخصص للهوية البصرية"""
    
    return """
    <style>
    /* الأساسيات */
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #FBBF24;
        --accent-color: #10B981;
        --danger-color: #EF4444;
        --warning-color: #F59E0B;
        --info-color: #3B82F6;
        --light-bg: #F8FAFC;
        --dark-text: #1E293B;
        --gray-border: #E2E8F0;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --radius: 12px;
    }
    
    /* الهيكل الرئيسي */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        min-height: 100vh;
    }
    
    /* الرأس الرئيسي */
    .main-header {
        background: linear-gradient(90deg, var(--primary-color) 0%, #2563EB 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 0 0 var(--radius) var(--radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    
    .header-content {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .header-status {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .status-badge {
        background: rgba(255, 255, 255, 0.15);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        backdrop-filter: blur(10px);
    }
    
    /* بطاقات */
    .dashboard-card {
        background: white;
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--gray-border);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .card-icon {
        background: var(--primary-color);
        color: white;
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--dark-text);
        margin: 0;
    }
    
    .card-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary-color);
        margin: 1rem 0;
    }
    
    /* أزرار */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color) 0%, #2563EB 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: var(--radius);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow);
    }
    
    /* تسجيل الدخول */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 70vh;
        padding: 2rem;
    }
    
    .login-card {
        background: white;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        padding: 2.5rem;
        width: 100%;
        max-width: 450px;
        border: 1px solid var(--gray-border);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-header h2 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .login-footer {
        margin-top: 2rem;
        text-align: center;
        color: #64748B;
        font-size: 0.9rem;
    }
    
    /* معلومات المستخدم */
    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.5rem 0;
    }
    
    .user-role {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .user-role.admin { background: #FEF3C7; color: #92400E; }
    .user-role.committee { background: #D1FAE5; color: #065F46; }
    .user-role.valuer { background: #DBEAFE; color: #1E40AF; }
    .user-role.dataentry { background: #F3E8FF; color: #5B21B6; }
    
    .user-name {
        font-weight: 600;
        color: var(--dark-text);
    }
    
    /* الأقسام */
    .section-header {
        background: white;
        padding: 1.5rem;
        border-radius: var(--radius);
        margin-bottom: 2rem;
        border-left: 5px solid var(--primary-color);
    }
    
    .section-header h2 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    /* الجداول */
    .dataframe {
        border-radius: var(--radius);
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* المؤشرات */
    .metric-card {
        text-align: center;
        padding: 1.5rem;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #64748B;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* الملف الشخصي */
    .profile-card {
        background: white;
        border-radius: var(--radius);
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    .profile-avatar {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, var(--primary-color), #60A5FA);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
    }
    
    .avatar-icon {
        font-size: 3rem;
        color: white;
    }
    
    .role-badge {
        display: inline-block;
        padding: 0.25rem 1rem;
        background: var(--secondary-color);
        color: #92400E;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    /* التلميحات */
    .hint-text {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        color: #0369A1;
        padding: 1rem;
        border-radius: var(--radius);
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    
    /* الرسوم البيانية */
    .chart-container {
        background: white;
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
    }
    
    /* الوسائط */
    @media (max-width: 768px) {
        .app-title { font-size: 1.8rem; }
        .header-status { flex-direction: column; align-items: center; }
        .dashboard-card { margin-bottom: 1rem; }
    }
    </style>
    """
