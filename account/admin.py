
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "is_staff", "is_student", "is_teacher", "is_tutor"]
    list_filter = ["is_staff", "is_student", "is_teacher", "is_tutor", "is_active"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_student",
                "is_teacher",
                "is_tutor",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "is_active",
                "is_staff",
                "is_superuser",
                "is_student",
                "is_teacher",
                "is_tutor",
            ),
        }),
    )

    search_fields = ["email", "first_name", "last_name"]
