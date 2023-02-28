# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser, Image, Thumbnail, Tier


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "account_tier")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
        ("Account Tier", {"fields": ("account_tier",)}),
    )
    add_fieldsets = (
        (
            "Personal Info",
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
    ordering = ("email",)
    filter_horizontal = ()


class TierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "thumbnail_sizes",
        "link_present",
        "allow_expiring_link",
    )


class ImageAdmin(admin.ModelAdmin):
    list_display = ("user", "original_image")


class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ("path", "size", "image")


admin.site.register(Tier, TierAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
admin.site.unregister(Group)
