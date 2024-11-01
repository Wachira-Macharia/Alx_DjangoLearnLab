# Create Operation
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Expected Output:
# <Book: 1984 by George Orwell (1949)>


# Retrieve Operation
from bookshelf.models import Book
retrieved_book = Book.objects.get(id=book.id)
# Expected Output:
# <Book: 1984 by George Orwell (1949)>


# Update Operation
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
# Expected Output:
# <Book: Nineteen Eighty-Four by George Orwell (1949)>


# Delete Operation
retrieved_book.delete()
# Expected Output:
# (1, {'bookshelf.Book': 1})

Book.objects.all()
# Expected Output:
# <QuerySet []>  # No books remaining
