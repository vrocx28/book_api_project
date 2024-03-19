from rest_framework import serializers
from .models import Book, Author, Language, Subject, BookShelf, Format


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'birth_year', 'death_year')

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    subject = serializers.StringRelatedField(many=True, source='subjects')
    languages = serializers.StringRelatedField(many=True, source='book_languages')
    bookshelves = serializers.StringRelatedField(many=True)
    download_links = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'subject', 'languages', 'bookshelves', 'download_links')

    def get_authors(self, obj):
        authors = obj.author.all()
        return AuthorSerializer(authors, many=True).data

    def get_download_links(self, obj):
        formats = Format.objects.filter(book=obj)
        return [{'mime_type': format.mime_type, 'url': format.url} for format in formats]
