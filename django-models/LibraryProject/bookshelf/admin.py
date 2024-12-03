from django.contrib import admin
from .models import Book

# Custom admin configuration for the Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year',)
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)
