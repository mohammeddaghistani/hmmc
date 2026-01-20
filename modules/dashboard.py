import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def render_dashboard(user_role):
    """عرض لوحة التحكم الرئيسية"""
    
    st.markdown("""
    <div class="section-header">
        <h2>📊 لوحة تحكم النظام</h2>
        <p>نظرة عامة على أداء النظام والإحصائيات الرئيسية</p>
    </div>
    """, unsafe_allow_html=True)
    
    # مؤشرات الأداء الرئيسية
    render_kpi_cards()
    
    st.markdown("---")
    
    # المخططات والرسوم البيانية
    col1, col2 = st.columns(2)
    
    with col1:
        render_evaluation_chart()
    
    with col2:
        render_deals_by_region()
    
    st.markdown("---")
    
    # آخر التقييمات والصفقات
    col3, col4 = st.columns(2)
    
    with col3:
        render_recent_evaluations()
    
    with col4:
        render_upcoming_tasks()

def render_kpi_cards():
    """عرض مؤشرات الأداء الرئيسية"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div class="card-icon">🏢</div>
                <div>
                    <h3 class="card-title">إجمالي الصفقات</h3>
                    <p class="card-subtitle">+12% عن الشهر الماضي</p>
                </div>
            </div>
            <div class="card-value">1,245</div>
            <div class="card-progress">
                <div style="background: #10B981; height: 6px; border-radius: 3px; width: 75%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div class="card-icon">📈</div>
                <div>
                    <h3 class="card-title">التقييمات المكتملة</h3>
                    <p class="card-subtitle">+8% عن الشهر الماضي</p>
                </div>
            </div>
            <div class="card-value">892</div>
            <div class="card-progress">
                <div style="background: #3B82F6; height: 6px; border-radius: 3px; width: 60%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div class="card-icon">⭐</div>
                <div>
                    <h3 class="card-title">متوسط الثقة</h3>
                    <p class="card-subtitle">+5% عن الشهر الماضي</p>
                </div>
            </div>
            <div class="card-value">87%</div>
            <div class="card-progress">
                <div style="background: #F59E0B; height: 6px; border-radius: 3px; width: 87%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div class="card-icon">💰</div>
                <div>
                    <h3 class="card-title">متوسط القيمة</h3>
                    <p class="card-subtitle">+3% عن الشهر الماضي</p>
                </div>
            </div>
            <div class="card-value">425K</div>
            <div class="card-progress">
                <div style="background: #8B5CF6; height: 6px; border-radius: 3px; width: 45%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_evaluation_chart():
    """عرض مخطط التقييمات"""
    
    st.markdown("""
    <div class="chart-container">
        <h3>📈 توزيع التقييمات الشهري</h3>
    """, unsafe_allow_html=True)
    
    # بيانات نموذجية
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو']
    evaluations = [120, 145, 180, 165, 210, 195]
    confidence = [82, 85, 87, 84, 89, 87]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=evaluations,
        name='عدد التقييمات',
        marker_color='#1E3A8A',
        opacity=0.8
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=confidence,
        name='نسبة الثقة %',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='#F59E0B', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            title="عدد التقييمات",
            gridcolor='#E2E8F0'
        ),
        yaxis2=dict(
            title="نسبة الثقة %",
            overlaying='y',
            side='right',
            range=[75, 95],
            gridcolor='#E2E8F0'
        ),
        xaxis=dict(
            gridcolor='#E2E8F0'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_deals_by_region():
    """عرض الصفقات حسب المنطقة"""
    
    st.markdown("""
    <div class="chart-container">
        <h3>🗺️ توزيع الصفقات حسب المنطقة</h3>
    """, unsafe_allow_html=True)
    
    # بيانات نموذجية
    regions = ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة', 'الشرقية']
    deals = [320, 280, 210, 180, 150, 105]
    colors = ['#1E3A8A', '#2563EB', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE']
    
    fig = go.Figure(data=[go.Pie(
        labels=regions,
        values=deals,
        hole=.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='inside'
    )])
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        showlegend=False,
        annotations=[dict(
            text='المناطق',
            x=0.5,
            y=0.5,
            font_size=14,
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_recent_evaluations():
    """عرض آخر التقييمات"""
    
    st.markdown("""
    <div class="chart-container">
        <h3>🕒 آخر التقييمات</h3>
    """, unsafe_allow_html=True)
    
    # بيانات نموذجية
    data = {
        'العنوان': ['حي النخيل - الرياض', 'حي الياسمين - جدة', 'حي الربيع - الدمام'],
        'النوع': ['سكني', 'تجاري', 'مكتبي'],
        'القيمة': ['450,000 ر.س', '320,000 ر.س', '280,000 ر.س'],
        'الثقة': ['92%', '85%', '88%'],
        'التاريخ': ['2024-01-15', '2024-01-14', '2024-01-13']
    }
    
    df = pd.DataFrame(data)
    
    # تنسيق الجدول
    st.dataframe(
        df,
        column_config={
            "العنوان": st.column_config.TextColumn("العنوان", width="medium"),
            "النوع": st.column_config.TextColumn("النوع", width="small"),
            "القيمة": st.column_config.TextColumn("القيمة", width="small"),
            "الثقة": st.column_config.ProgressColumn(
                "الثقة",
                format="%f%%",
                min_value=0,
                max_value=100,
                width="small"
            ),
            "التاريخ": st.column_config.DateColumn("التاريخ")
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_upcoming_tasks():
    """عرض المهام القادمة"""
    
    st.markdown("""
    <div class="chart-container">
        <h3>📅 المهام القادمة</h3>
    """, unsafe_allow_html=True)
    
    # بيانات نموذجية
    tasks = [
        {"المهمة": "مراجعة تقييم #245", "النوع": "مراجعة", "الأولوية": "عالية", "الموعد": "غداً"},
        {"المهمة": "تقييم عقار جديد", "النوع": "تقييم", "الأولوية": "متوسطة", "الموعد": "بعد غد"},
        {"المهمة": "تقرير شهري", "النوع": "تقرير", "الأولوية": "منخفضة", "الموعد": "نهاية الأسبوع"},
        {"المهمة": "تحديث قاعدة البيانات", "النوع": "صيانة", "الأولوية": "متوسطة", "الموعد": "الأسبوع القادم"}
    ]
    
    for task in tasks:
        priority_color = {
            "عالية": "#EF4444",
            "متوسطة": "#F59E0B",
            "منخفضة": "#10B981"
        }[task["الأولوية"]]
        
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #E2E8F0;
            border-left: 4px solid {priority_color};
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <strong>{task["المهمة"]}</strong>
                <div style="font-size: 0.9rem; color: #64748B;">
                    {task["النوع"]} • <span style="color: {priority_color}">{task["الأولوية"]}</span>
                </div>
            </div>
            <div style="
                background: #F8FAFC;
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 0.9rem;
                color: #475569;
            ">
                {task["الموعد"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
