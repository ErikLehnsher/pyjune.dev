from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'category',
        'status',
        'is_published',
        'created_at'
    ]
    list_filter = ['status', 'is_published', 'category', 'created_at']
    search_fields = ['title', 'excerpt', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['tags']
    readonly_fields = ['html_preview', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic info', {
            'fields': (
                'title',
                'slug',
                'author',
                'excerpt',
                'category',
                'tags',
            )
        }),
        ('Content (Tiptap)', {
            'fields': (
                'content_json',
                'html_preview',
            )
        }),
        ('Publish', {
            'fields': (
                'status',
                'is_published',
            )
        }),
        ('Meta', {
            'fields': (
                'odoo_version',
                'module',
                'error_keyword',
            )
        }),
        ('System', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def html_preview(self, obj):
        if not obj.html_content:
            return "-"
        return format_html(
            '<div style="max-width:800px; border:1px solid #ddd; padding:12px;">{}</div>',
            obj.html_content
        )

    html_preview.short_description = "Content Preview (HTML)"
