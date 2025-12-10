from django.contrib import admin
from apps.trailer.models import (
    TrailerCategory, Trailer, TrailerType, TrailerTypeImage, TrailerTypePrice, TrailerTypeSEO
)
from parler.admin import TranslatableAdmin


class TrailerTypePriceInline(admin.TabularInline):
    model = TrailerTypePrice
    extra = 0
    max_num = 1


class TrailerTypeImageInline(admin.TabularInline):
    model = TrailerTypeImage
    extra = 0
    max_num = 10


@admin.register(TrailerCategory)
class TrailerCategoryAdmin(TranslatableAdmin):
    search_fields = ['title']
    list_filter = ['status']
    list_display = ['title', 'project', 'status']


@admin.register(TrailerType)
class TrailerTypeAdmin(TranslatableAdmin):
    search_fields = ['title']
    inlines = [
        TrailerTypePriceInline,
        TrailerTypeImageInline,
    ]
    list_filter = ['status']
    list_display = ('title', 'topic', 'position', 'code', 'status')


@admin.register(TrailerTypeImage)
class TrailerTypeImageAdmin(admin.ModelAdmin):
    search_fields = ['trailer_type__translations__title']
    list_display = ('trailer_type', 'number')


@admin.register(TrailerTypePrice)
class TrailerTypePriceAdmin(admin.ModelAdmin):
    search_fields = ['trailer_type__translations__title']
    list_display = ['trailer_type', 'hour', 'one_day', 'two_days']


@admin.register(TrailerTypeSEO)
class TrailerTypeSEOAdmin(TranslatableAdmin):
    search_fields = ['trailer_type__translations__title']
    list_display = ['id', 'trailer_type', 'url']


@admin.register(Trailer)
class TrailerAdmin(TranslatableAdmin):
    list_display = ('id', )
