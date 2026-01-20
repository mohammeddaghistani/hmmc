import streamlit as st
import pandas as pd
from datetime import datetime

class UserManager:
    """مدير المستخدمين والصلاحيات"""
    
    def __init__(self):
        self.permissions_file = 'data/user_permissions.json'
        self.permissions = self.load_permissions()
    
    def load_permissions(self):
        """تحميل الصلاحيات"""
        try:
            with open(self.permissions_file, 'r', encoding='utf-8') as f:
                import json
                return json.load(f)
        except:
            return {}
    
    def save_permissions(self):
        """حفظ الصلاحيات"""
        with open(self.permissions_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(self.permissions, f, ensure_ascii=False, indent=2)
    
    def get_user_permissions(self, username):
        """الحصول على صلاحيات مستخدم"""
        return self.permissions.get(username, {
            "create_evaluation": False,
            "edit_evaluation": False,
            "delete_evaluation": False,
            "view_reports": False,
            "export_data": False,
            "manage_users": False,
            "system_settings": False
        })
    
    def update_permission(self, username, permission, value):
        """تحديث صلاحية معينة"""
        if username not in self.permissions:
            self.permissions[username] = {}
        
        self.permissions[username][permission] = value
        self.save_permissions()
    
    def update_user_role(self, username, new_role):
        """تحديث دور المستخدم"""
        # في الواقع، ستكون هذه العملية على قاعدة البيانات
        st.success(f"تم تحديث دور {username} إلى {new_role}")
        return True
    
    def delete_user(self, username):
        """حذف مستخدم"""
        # في الواقع، ستكون هذه العملية على قاعدة البيانات
        if username in self.permissions:
            del self.permissions[username]
            self.save_permissions()
        return True
    
    def get_all_permissions(self):
        """الحصول على جميع الصلاحيات"""
        return {
            "create_evaluation": "إنشاء تقييمات",
            "edit_evaluation": "تعديل تقييمات",
            "delete_evaluation": "حذف تقييمات",
            "view_reports": "عرض التقارير",
            "export_data": "تصدير البيانات",
            "manage_users": "إدارة المستخدمين",
            "system_settings": "إعدادات النظام",
            "manage_equations": "إدارة المعادلات",
            "manage_maps": "إدارة الخرائط",
            "view_audit_logs": "عرض سجلات التدقيق",
            "backup_restore": "النسخ الاحتياطي",
            "system_maintenance": "صيانة النظام"
        }
    
    def get_role_permissions(self, role):
        """الحصول على صلاحيات الدور"""
        role_permissions = {
            "admin": {
                "create_evaluation": True,
                "edit_evaluation": True,
                "delete_evaluation": True,
                "view_reports": True,
                "export_data": True,
                "manage_users": True,
                "system_settings": True,
                "manage_equations": True,
                "manage_maps": True,
                "view_audit_logs": True,
                "backup_restore": True,
                "system_maintenance": True
            },
            "manager": {
                "create_evaluation": True,
                "edit_evaluation": True,
                "delete_evaluation": True,
                "view_reports": True,
                "export_data": True,
                "manage_users": False,
                "system_settings": False,
                "manage_equations": False,
                "manage_maps": True,
                "view_audit_logs": True,
                "backup_restore": False,
                "system_maintenance": False
            },
            "evaluator": {
                "create_evaluation": True,
                "edit_evaluation": True,
                "delete_evaluation": False,
                "view_reports": True,
                "export_data": True,
                "manage_users": False,
                "system_settings": False,
                "manage_equations": False,
                "manage_maps": True,
                "view_audit_logs": False,
                "backup_restore": False,
                "system_maintenance": False
            },
            "viewer": {
                "create_evaluation": False,
                "edit_evaluation": False,
                "delete_evaluation": False,
                "view_reports": True,
                "export_data": False,
                "manage_users": False,
                "system_settings": False,
                "manage_equations": False,
                "manage_maps": True,
                "view_audit_logs": False,
                "backup_restore": False,
                "system_maintenance": False
            }
        }
        
        return role_permissions.get(role, role_permissions["viewer"])
    
    def check_permission(self, username, permission):
        """التحقق من صلاحية معينة"""
        user_perms = self.get_user_permissions(username)
        return user_perms.get(permission, False)
