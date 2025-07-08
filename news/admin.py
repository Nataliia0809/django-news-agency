from django.contrib import admin
from .models import Topic, Newspaper, Tag, Comment, NewspaperRating, Department


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created", "updated")
    list_filter = ("is_active", "created")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "published_date",
        "priority",
        "is_published",
        "is_featured",
        "views_count",
    )
    list_filter = ("is_published", "is_featured", "published_date", "priority")
    search_fields = ("title", "except", "content")
    date_hierarchy = "published_date"
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("publishers", "tags")
    readonly_fields = ("views_count", "created", "updated")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "created")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("newspaper", "author", "is_approved", "created", "updated")
    list_filter = ("is_approved", "created")
    search_fields = ("content", "author__username")
    readonly_fields = ("created", "updated")


@admin.register(NewspaperRating)
class NewspaperRatingAdmin(admin.ModelAdmin):
    list_display = ("newspaper", "user", "rating", "created")
    list_filter = ("rating", "created")
    search_fields = ("user__username", "newspaper__title")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "head", "created")
    search_fields = ("name", "head__username")
