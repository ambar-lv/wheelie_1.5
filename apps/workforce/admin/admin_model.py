from django.contrib import admin
from apps.workforce.models import Company, Employer, Owner


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", 'name', 'owner']
    list_filter = ['owner']
    search_fields = ['name']


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ["id", 'name']


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ["id", 'user', 'percent', 'status']

