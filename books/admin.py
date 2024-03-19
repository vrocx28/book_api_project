from django.contrib import admin
from .models import Author, Language, Subject, Book

# Register your models here.


class Books(admin.ModelAdmin):
    list_display = [
        "title",
        "download_count",
        "gutenberg_id",
        "media_type",
    ]
    readonly_fields = ["id"]


admin.site.register(Book, Books)
# admin.site.register(Author, Language, Subject, Bookshelf,
