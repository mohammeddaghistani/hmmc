import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

class MapSystem:
    """نظام خرائط متكامل"""
    
    def __init__(self):
        self.map_types = {
            'basic': 'خرائط جوجل الأساسية',
            'satellite': 'خرائط الأقمار الصناعية',
            'hybrid': 'خرائط هجينة',
            'terrain': 'خرائط التضاريس',
            'dark': 'خرائط داكنة'
        }
        
        # مواقع افتراضية
        self.default_locations = [
            {"name": "الرياض", "lat": 24.7136, "lng": 46.6753, "type": "capital"},
            {"name": "جدة", "lat": 21.4858, "lng": 39.1925, "type": "commercial"},
            {"name": "الدمام", "lat": 26.4207, "lng": 50.0888, "type": "industrial"},
            {"name": "مكة", "lat": 21.3891, "lng": 39.8579, "type": "religious"},
            {"name": "المدينة", "lat": 24.4709, "lng": 39.6122, "type": "religious"},
        ]
        
        self.current_map = None
    
    def render_map(self, map_type='basic', center_lat=24.7136, center_lng=46.6753, 
                   zoom=12, show_markers=True, show_heatmap=False):
        """عرض الخريطة التفاعلية"""
        
        # إنشاء الخريطة الأساسية
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=zoom,
            tiles=self.get_tile_layer(map_type),
            control_scale=True
        )
        
        # إضافة العلامات
        if show_markers:
            self.add_markers(m)
        
        # إضافة خريطة الحرارة
        if show_heatmap:
            self.add_heatmap(m)
        
        # إضافة عناصر التحكم
        self.add_controls(m)
        
        # عرض الخريطة
        st_folium(m, width=800, height=600)
        
        self.current_map = m
        
        return m
    
    def get_tile_layer(self, map_type):
        """الحصول على طبقة الخريطة المناسبة"""
        
        tile_layers = {
            'basic': 'OpenStreetMap',
            'satellite': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            'hybrid': 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            'terrain': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            'dark': 'CartoDB dark_matter'
        }
        
        return tile_layers.get(map_type, 'OpenStreetMap')
    
    def add_markers(self, map_obj):
        """إضافة علامات للمواقع"""
        
        for location in self.default_locations:
            # اختيار لون حسب النوع
            color_map = {
                'capital': 'red',
                'commercial': 'blue',
                'industrial': 'green',
                'religious': 'purple'
            }
            
            color = color_map.get(location['type'], 'gray')
            
            # إنشاء العلامة
            folium.Marker(
                location=[location['lat'], location['lng']],
                popup=f"<b>{location['name']}</b><br>نوع: {location['type']}",
                tooltip=location['name'],
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(map_obj)
    
    def add_heatmap(self, map_obj):
        """إضافة خريطة حرارة"""
        
        # بيانات افتراضية للكثافة
        heat_data = []
        for loc in self.default_locations:
            # إضافة نقاط حول الموقع الرئيسي
            for _ in range(10):
                lat = loc['lat'] + np.random.uniform(-0.05, 0.05)
                lng = loc['lng'] + np.random.uniform(-0.05, 0.05)
                heat_data.append([lat, lng])
        
        # إضافة خريطة الحرارة
        from folium.plugins import HeatMap
        
        HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(map_obj)
    
    def add_controls(self, map_obj):
        """إضافة عناصر تحكم للخريطة"""
        
        from folium.plugins import MeasureControl, Fullscreen, Draw
        
        # أداة القياس
        measure = MeasureControl()
        measure.add_to(map_obj)
        
        # وضع ملء الشاشة
        fullscreen = Fullscreen()
        fullscreen.add_to(map_obj)
        
        # أدوات الرسم
        draw = Draw()
        draw.add_to(map_obj)
        
        # البحث عن موقع
        from folium.plugins import Geocoder
        geocoder = Geocoder()
        geocoder.add_to(map_obj)
    
    def update_map(self, lat, lng, zoom):
        """تحديث إعدادات الخريطة"""
        self.render_map(center_lat=lat, center_lng=lng, zoom=zoom)
    
    def test_map(self, lat, lng, zoom):
        """اختبار الخريطة"""
        st.info(f"جاري تحميل الخريطة للموقع: {lat}, {lng}")
        self.render_map(center_lat=lat, center_lng=lng, zoom=zoom)
    
    def export_map(self, format_type='html'):
        """تصدير الخريطة"""
        if self.current_map:
            if format_type == 'html':
                return self.current_map._repr_html_()
            elif format_type == 'image':
                # حفظ كصورة
                import io
                img_data = self.current_map._to_png()
                return io.BytesIO(img_data)
        return None
