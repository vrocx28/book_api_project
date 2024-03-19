from django.urls import path
from .views import BookListView

urlpatterns = [
    path('all_books', BookListView.as_view(), name='all_books'),
    # Add more URL patterns as needed
]
