from django.contrib import admin
from .models import Category, Tag, Post, FriendLink


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "post_count", "description"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "post_count"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "is_top", "views", "created_at", "updated_at"]
    list_filter = ["status", "category", "tags", "is_top"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "body"]
    date_hierarchy = "created_at"
    filter_horizontal = ["tags"]
    fieldsets = [
        (None, {"fields": ["title", "slug", "author", "image", "body"]}),
        ("分类与标签", {"fields": ["category", "tags"]}),
        ("发布设置", {"fields": ["status", "is_top", "summary"]}),
    ]


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "is_active"]
    list_filter = ["is_active"]
