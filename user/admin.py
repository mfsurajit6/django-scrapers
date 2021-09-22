from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


class CustomUserAdmin(admin.ModelAdmin):
    """Custom display of User in Django Admin"""
    exclude = ('groups', 'user_permissions', )
    list_display = (
        'id', 'name', 'email', 'is_active', 'is_superuser'
    )
    list_display_links = ('name', )
    list_editable = ('is_active', 'is_superuser', )
    search_fields = ('name', 'email', )
    fieldsets = (
        ('Login Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', )}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', )})
    )
    ordering = ('name', )
    list_filter = ()


admin.site.register(User, CustomUserAdmin)
