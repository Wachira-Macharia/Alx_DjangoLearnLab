from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# Create your views here.

# ListView: Retrieve all books
class BookListView(generics.ListAPIView):
    """
    Handles GET requests to list all books.
    Accessible to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year', 'title']
    ordering = ['title']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']

# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    Handles GET requests for retrieving a specific book by ID.
    Accessible to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    Handles POST requests to create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Example: Add additional fields or logic
        serializer.save()

# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    Handles PUT/PATCH requests to update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    Handles DELETE requests to remove a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

