from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Fields to display in the user list
    list_display = ('email', 'username', 'user_type', 'phone', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    
    # Fields in the edit user form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'user_type')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'phone', 'password1', 'password2'),
        }),
    )
    
    # Search and ordering
    search_fields = ('email', 'username', 'phone', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register your custom User model with the custom admin class
admin.site.register(User, CustomUserAdmin)