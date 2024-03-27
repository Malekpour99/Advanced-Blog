from django.contrib import admin
from blog.models import Post, Category


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "published",
        "category",
        "created_date",
        "published_date",
    )
    list_filter = ("author", "published")
    empty_value_display = "-empty-"
    date_hierarchy = "created_date"
    search_fields = ["title", "content"]


admin.site.register(Category)
