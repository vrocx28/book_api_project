from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import BookSerializer

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        # Get query parameters from the request
        filters = self.request.query_params

        # Start with all books
        books = Book.objects.all()

        # Filter books based on query parameters
        for key, value in filters.items():
            if key == 'author':
                books = books.filter(author__name__icontains=value)
            elif key == 'title':
                books = books.filter(title__icontains=value)
            elif key == 'language':
                languages = value.split(',')
                books = books.filter(book_languages__code__in=languages)
            elif key == 'topic':
                topic_query = Q(subjects__name__icontains=value) | Q(bookshelves__name__icontains=value)
                books = books.filter(topic_query)
            elif key == 'mime_type':
                mime_types = value.split(',')
                books = books.filter(format__mime_type__in=mime_types)
            elif key == 'gutenberg_id':
                gutenberg_ids = value.split(',')
                books = books.filter(gutenberg_id__in=gutenberg_ids)

        # Order books by download_count in descending order (popularity)
        books = books.order_by('-download_count')

        # Paginate the queryset
        paginator = CustomPagination()
        paginated_books = paginator.paginate_queryset(books, request)

        # Serialize the queryset
        serializer = BookSerializer(paginated_books, many=True)

        return paginator.get_paginated_response(serializer.data)
