from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Redactor


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = (
        "username",
        "full_name",
        "email",
        "years_of_experience",
        "is_active_redactor",
        "created",
    )
    list_filter = ("is_active_redactor", "department", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "email")
    readonly_fields = ("created",)
    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "bio",
                    "avatar",
                    "phone",
                    "years_of_experience",
                )
            },
        ),
        ("Department", {"fields": ("department",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active_redactor",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "created")}),
    )
    ordering = ("username",)


# створити views та urls; розібратися з crud операціями і автентифікацією користувачів (6, 7, 8 пункти)
