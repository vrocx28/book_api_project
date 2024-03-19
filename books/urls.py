from django.urls import path
from .views import BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='all_books'),
    # Add more URL patterns as needed
]
