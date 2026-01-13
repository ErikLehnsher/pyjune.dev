from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html

# Register your models here.

@admin.register(UserProfile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_author', 'created_at', 'display_avatar', 'role']
    search_fields = ['user__username', 'user__email']
    list_filter  = ['is_author', 'is_admin', 'created_at']
    
    def display_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover; border-radius: 4px;" />', obj.avatar.url)
        return "-"
    display_avatar.short_description = 'Avatar'