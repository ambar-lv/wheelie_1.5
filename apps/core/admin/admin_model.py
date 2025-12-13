from django.contrib import admin
from apps.core.models import (
    Country, City,
    Invoice, Project, ProjectVersion,
    ProjectImage, ReferalPercent
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "country", "name"]
    search_fields = ["name"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


class ReferalPercentInline(admin.StackedInline):
    model = ReferalPercent
    extra = 0
    max_num = 1


class ProjectVersionInline(admin.StackedInline):
    model = ProjectVersion
    extra = 0


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 0
    max_num = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    inlines = (ProjectVersionInline, ProjectImageInline, ReferalPercentInline)


@admin.register(ProjectVersion)
class ProjectVersionAdmin(admin.ModelAdmin):
    list_display = ['id', 'apple_version', 'android_version']


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferalPercent)
class ReferalPercentAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'new', 'sharing']

