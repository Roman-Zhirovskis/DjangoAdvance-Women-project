from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Women, Category


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'time_create', 'photo', 'get_mini_photo', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create',)
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_mini_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_mini_photo')

    def get_mini_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_mini_photo.short_description = "Отображение"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах 2'
