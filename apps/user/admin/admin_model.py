from django.contrib import admin
from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["full_phone", "email", "is_active"]
    search_fields = ["phone", "email"]

    @admin.display(description="Phone", ordering="phone")
    def full_phone(self, obj: User):
        return f"{obj.phone_code}{obj.phone}"
