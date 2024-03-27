from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_superuser", "is_active", "created_date")
    list_filter = ("email", "is_superuser", "is_active")
    fieldsets = (
        (
            "Authenticaion",
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", )
