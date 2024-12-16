from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test database and API client for testing.
        """
        # Create API client
        self.client = APIClient()
        self.client.login(user=self.user)

        # Create Author and Books
        self.author = Author.objects.create(name="John Doe")
        self.book1 = Book.objects.create(
            title="Book One", publication_year=2020, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Book Two", publication_year=2021, author=self.author
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
        """
        Test creating a new book.
        """
        data = {
            "title": "Book Three",
            "publication_year": 2022,
            "author": self.author.id,
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

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
        """
        Test deleting a book.
        """
        response = self.client.delete(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

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
        """
        Test that creating a book is restricted to authenticated users.
        """
        self.client.force_authenticate(user=None)  # Unauthenticated
        data = {
            "title": "Book Four",
            "publication_year": 2023,
            "author": self.author.id,
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
