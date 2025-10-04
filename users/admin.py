from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # What to display in the user list
    list_display = ('username', 'email', 'role', 'is_active', 'last_login', 'date_joined')

    # Add filters to the right sidebar
    list_filter = ('role', 'is_active')

    # Add search functionality
    search_fields = ('username', 'email')

    # Organize the fields in the user edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Make the role field editable
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
