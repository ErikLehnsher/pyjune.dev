# posts/admin.py
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
    list_display = ['title', 'author', 'category', 'is_published', 'created_at', 'featured_image_tag']
    list_filter = ['is_published', 'category', 'tags', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['tags']
    readonly_fields = ['featured_image_tag']  # Đổi thành tên hàm mới

    fieldsets = (
    (None, {
        'fields': ('title', 'slug', 'author', 'content', 'excerpt', 'featured_image', 'featured_image_tag', 'category', 'tags', 'is_published')
    }),
)

    def featured_image_tag(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover; border-radius: 4px;" />', obj.featured_image.url)
        return "No Image"
    featured_image_tag.short_description = 'Ảnh đại diện'