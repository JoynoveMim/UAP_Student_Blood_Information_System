# In bloodbank/admin.py - ADD THIS CODE:

from django.contrib import admin
from .models import UserProfile, BloodRequest, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'is_available', 'is_donor']
    list_filter = ['blood_group', 'is_available', 'is_donor']

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'blood_group', 'status', 'urgency', 'created_at']
    list_filter = ['status', 'blood_group', 'urgency']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']