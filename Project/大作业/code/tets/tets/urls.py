"""
URL configuration for tets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from index import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('home/', views.home),
    path('register/',views.register),
    path('book_list/', views.book_list, name='book_list'),
    path('search/', views.search_books, name='search_books'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/', views.author_list, name='author_list'),
    path('add_to_booklist/<int:user_id>/', views.add_to_booklist, name='add_to_booklist'),
    path('view_user_booklist/<int:user_id>/', views.view_user_booklist, name='view_user_booklist'),
    path('read_preview/<int:book_id>/', views.read_preview, name='read_preview'),
]
