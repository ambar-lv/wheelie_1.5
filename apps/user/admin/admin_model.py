from django.contrib import admin
from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["phone", "is_active"]
    search_fields = ["phone"]
