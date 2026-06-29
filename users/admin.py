from django.contrib import admin

# Register your models here.
# from rest_framework.authtoken.admin import TokenAdmin
# from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

# Register your models here.

class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name')
    list_filter = ('email', 'user_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ( 'email', 'user_name', 'is_active', 'is_staff')
    fieldsets=(
        (None, {'fields': ('email', 'user_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',"groups",
        "user_permissions",)}),
        ("Important dates", {
        "fields": (
            "last_login",
            "start_date",
        )
    }),
    )
    add_fieldsets=(
        (None, {
            "classes": ('wide',),
            "fields": ('email', 'user_name', 'password1', 'password2', 'is_active', 'is_staff')}),
    )
    
    
admin.site.register(NewUser, UserAdminConfig)


