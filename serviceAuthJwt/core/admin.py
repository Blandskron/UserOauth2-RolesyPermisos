from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Document, Log

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'identification', 'status', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'identification', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'identification', 'status')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Document)
admin.site.register(Log)
