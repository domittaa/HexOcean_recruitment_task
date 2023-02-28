# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tier
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'account_tier')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Account Tier', {'fields': ('account_tier',)}),
    )
    add_fieldsets = (
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()


class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail_size', 'link_present', 'allow_expiring_link', 'expiring_link_expiration')


admin.site.register(Tier, TierAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
