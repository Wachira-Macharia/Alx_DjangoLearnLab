from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User
from django.urls import reverse

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()

        # Authenticate the test client
        self.client.force_authenticate(user=self.user)

        # Create test data (authors, books, etc.)
        self.author = Author.objects.create(name="Author Name")
        self.book = Book.objects.create(
            title="Sample Book", publication_year=2020, author=self.author
        )

        # Endpoints
        self.book_list_url = "/api/books/"
        self.book_detail_url = lambda pk: f"/api/books/{pk}/"

    def test_list_books(self):
        """
        Test retrieving the list of books.
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_detail(self):
        """
        Test retrieving a single book by ID.
        """
        response = self.client.get(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book(self):
        # Prepare the payload
        payload = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id,
        }
        response = self.client.post(reverse('book-list'), data=payload)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """
        Test updating an existing book.
        """
        data = {"title": "Updated Book One", "publication_year": 2020}
        response = self.client.put(self.book_detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    def test_delete_book(self):
        response = self.client.delete(reverse('book-detail', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        """
        Test filtering books by author name.
        """
        response = self.client.get(self.book_list_url, {"author__name": "John Doe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books(self):
        """
        Test searching books by title.
        """
        response = self.client.get(self.book_list_url, {"search": "Book One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book One")

    def test_order_books_by_year(self):
        """
        Test ordering books by publication year.
        """
        response = self.client.get(self.book_list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2020)

    def test_create_book_requires_authentication(self):
        # Unauthenticated client
        unauthenticated_client = APIClient()
        payload = {
            "title": "Unauthorized Book",
            "publication_year": 2023,
            "author": self.author.id,
        }
        response = unauthenticated_client.post(reverse('book-list'), data=payload)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)