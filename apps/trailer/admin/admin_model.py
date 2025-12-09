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


class TrailerTypeSEOInline(admin.TabularInline):
    model = TrailerTypeSEO
    extra = 0
    max_num = 1


@admin.register(TrailerCategory)
class TrailerCategoryAdmin(TranslatableAdmin):
    list_display = ('title', 'project', 'status')


@admin.register(TrailerType)
class TrailerTypeAdmin(TranslatableAdmin):
    inlines = [
        TrailerTypePriceInline,
        TrailerTypeImageInline,
        TrailerTypeSEOInline
    ]
    list_display = ('topic', 'position', 'code', 'status')


@admin.register(TrailerTypeImage)
class TrailerTypeImageAdmin(admin.ModelAdmin):
    list_display = ('trailer_type', 'number')


@admin.register(TrailerTypePrice)
class TrailerTypePriceAdmin(admin.ModelAdmin):
    list_display = ('trailer_type', 'hour', 'one_day')


@admin.register(TrailerTypeSEO)
class TrailerTypeSEOAdmin(TranslatableAdmin):
    list_display = ('trailer_type', 'url')


@admin.register(Trailer)
class TrailerAdmin(TranslatableAdmin):
    list_display = ('id', )
