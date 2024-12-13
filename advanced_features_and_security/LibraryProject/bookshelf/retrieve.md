# Retrieve Operation
from bookshelf.models import Book
retrieved_book = Book.objects.get(id=book.id)
# Expected Output:
# <Book: 1984 by George Orwell (1949)>
