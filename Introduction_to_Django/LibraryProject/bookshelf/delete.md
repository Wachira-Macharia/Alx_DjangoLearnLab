# Delete Operation
from bookshelf.models import Book
retrieved_book.delete()
# Expected Output:
# (1, {'bookshelf.Book': 1})

Book.objects.all()
# Expected Output:
# <QuerySet []>  # No books remaining
