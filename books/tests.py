from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book, Format
from .serializers import BookSerializer


class BookListViewTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.book1 = Book.objects.create(
            title="Book 1", download_count=100, gutenberg_id=1, media_type="text"
        )
        self.book2 = Book.objects.create(
            title="Book 2", download_count=50, gutenberg_id=2, media_type="text"
        )
        self.book3 = Book.objects.create(
            title="Book 3", download_count=200, gutenberg_id=3, media_type="text"
        )

        # Create sample formats with MIME types
        self.format1 = Format.objects.create(
            book=self.book1, mime_type="application/pdf", url="http://example.com/pdf"
        )
        self.format2 = Format.objects.create(
            book=self.book2, mime_type="text/plain", url="http://example.com/txt"
        )
        self.format3 = Format.objects.create(
            book=self.book3,
            mime_type="application/epub+zip",
            url="http://example.com/epub",
        )

    def test_filter_books_by_media_type(self):
        # Test filtering books by MIME type
        url = reverse("all_books")
        client = APIClient()
        response = client.get(
            url, {"mime_type": "application/pdf"}
        )  # Filter books with PDF format

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 1
        )  # Assuming only one book has PDF format
        self.assertEqual(response.data["results"][0]["title"], "Book 1")

    def test_get_books(self):
        # Test retrieving list of books
        url = reverse(
            "all_books"
        )
        client = APIClient()
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 3
        )  # Assuming pagination is used and page_size is 20

    def test_filter_books_by_author(self):
        # Test filtering books by author name
        url = reverse(
            "all_books"
        )
        client = APIClient()
        response = client.get(
            url, {"author": "Author Name"}
        )  # Update 'authors' to 'author'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 0
        )  # Assuming no book with the provided author name in the test data

    def test_filter_books_by_title(self):
        # Test filtering books by title
        url = reverse("all_books")
        client = APIClient()
        response = client.get(url, {"title": "Book 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Book 1")

    def test_filter_books_by_language(self):
        # Test filtering books by language
        url = reverse("all_books")
        client = APIClient()
        response = client.get(
            url, {"language": "en"}
        )  # Assuming 'en' is the code for English language

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 0
        )  # Assuming all books are in English

    def test_filter_books_by_topic(self):
        # Test filtering books by topic (subject or bookshelf)
        url = reverse("all_books")
        client = APIClient()
        response = client.get(url, {"topic": "Topic"})  # Provide a topic name

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 0
        )  # Assuming no book with the provided topic in the test data

    def test_filter_books_by_gutenberg_id(self):
        # Test filtering books by Gutenberg ID
        url = reverse("all_books")
        client = APIClient()

        # Filter by the gutenberg_id of book1
        response = client.get(url, {"gutenberg_id": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Book 1")

        # Filter by the gutenberg_id of book3
        response = client.get(url, {"gutenberg_id": 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Book 3")

        # Filter by a gutenberg_id that doesn't exist
        response = client.get(url, {"gutenberg_id": 100})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
