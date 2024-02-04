from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100)
    categories = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    picture = models.URLField()
    introduction = models.TextField()
    datas = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'book'
        
class AuthorTable(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'author_table'

class AuthorBook(models.Model):
    w_id = models.AutoField(primary_key=True)
    author_id = models.CharField(max_length=100)
    book_id = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'author_book'

class Booklist(models.Model):
    b_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    class Meta:
        db_table = 'booklistnew_table'
