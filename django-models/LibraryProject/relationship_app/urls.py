"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from relationship_app.views import list_books, LibraryDetailView, admin_view, librarian_view, member_view, add_book, edit_book, delete_book, login_view, logout_view, register_view  # Importing the views explicitly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', list_books, name='list_books'),  # Function-based view for listing books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view for library details
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/', edit_book, name='edit_book'),
    path('delete_book//', delete_book, name='delete_book'),
    path('register/', register_view.register_view, name='register'),
    path('login/', login_view.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', logout_view.as_view(template_name='relationship_app/logout.html'), name='logout'),
]

