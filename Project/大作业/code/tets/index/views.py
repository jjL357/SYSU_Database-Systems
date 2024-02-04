from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Book, AuthorTable, AuthorBook
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Booklist
from django import forms
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import os
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404
from django.db.models import Max
from django.shortcuts import get_list_or_404
@login_required
def read_preview(request, book_id):
    # 获取书籍
    book = get_object_or_404(Book, book_id=book_id)
    
    # 试读内容的相对路径
    preview_path = book.datas

    if preview_path:
        # 构建试读内容的完整路径
        diretory = os.getcwd()
        full_path = f'\\index\\static\\content\\{preview_path}'
        full_path = diretory + full_path
        # 读取试读内容
        with open(full_path, 'r', encoding='utf-8') as file:
            preview_content = file.read()

        # 渲染模板并返回响应
        context = {'preview_content': preview_content}
        return render(request, 'read_preview.html', context)

    return HttpResponse("Preview not available.")

@login_required
def view_user_booklist(request, user_id):
    try:
        user_booklist = get_list_or_404(Booklist, user_id=user_id)
        
        books_in_booklist = []
        for user_booklist_tmp in user_booklist:
            # 对于每个符合条件的Booklist，获取其关联的图书
            books_in_booklist.append(user_booklist_tmp.book_id)

    except Http404:
        user_booklist = None
        books_in_booklist = []

    if request.method == 'POST':
        # 处理删除书的逻辑
        book_id_to_delete = request.POST.get('delete_book_id')
        if book_id_to_delete:
            book_to_delete = get_object_or_404(Booklist, user_id=user_id,book_id=book_id_to_delete)
            
            book_to_delete.delete()
            
            messages.success(request, 'Book deleted successfully.')

        try:
            user_booklist = get_list_or_404(Booklist, user_id=user_id)
            
            books_in_booklist = []
            for user_booklist_tmp in user_booklist:
                # 对于每个符合条件的Booklist，获取其关联的图书
                books_in_booklist.append(user_booklist_tmp.book_id)

        except Http404:
            user_booklist = None
            books_in_booklist = []
            
            
    book = get_list_or_404(Book)
    context = {'user_booklist': user_booklist, 'books_in_booklist': books_in_booklist,'book':book,'user_id': user_id}

    
    if user_booklist is None:
        messages.info(request, 'Your booklist is empty.')

    return render(request, 'view_user_booklist.html', context)

@login_required
def add_to_booklist(request, user_id):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')

        # 获取当前书单的最大 bid，如果没有记录，则默认为 0
        max_bid = Booklist.objects.aggregate(max_bid=Max('b_id'))['max_bid']
        bid = max_bid + 1 if max_bid is not None else 0

        try:
            user_booklist = Booklist.objects.get(user_id=user_id, book_id=book_id)
        except Booklist.DoesNotExist:
            user_booklist = None

        if book_id:
            if user_booklist is not None:
                messages.warning(request, 'This book is already in your booklist.')
            else:
                Booklist.objects.create(user_id=user_id, book_id=book_id, b_id=bid)
                messages.success(request, 'Book added to your booklist.')
                return redirect('add_to_booklist', user_id=user_id)  # 重定向，显示成功消息

    return render(request, 'add_to_booklist.html')

@login_required
def author_list(request):
    if 'author_search' in request.GET:
        author_query = request.GET['author_search']
        authors = AuthorTable.objects.filter(author_name__icontains=author_query)
        author_books = AuthorBook.objects.filter(author_id__in=authors)
        # 修改这里，使用 book_id 而不是 id
        books = Book.objects.filter(book_id__in=author_books.values('book_id'))
    else:
        authors = AuthorTable.objects.all()
        author_books = AuthorBook.objects.all()
        # 修改这里，使用 book_id 而不是 id
        books = Book.objects.filter(book_id__in=author_books.values('book_id'))

    return render(request, 'author_list.html', {'authors': authors, 'author_books': author_books, 'books': books})

@login_required(login_url='/login/')
def book_list(request):
    # 获取书籍列表
    books = Book.objects.all()

    # 获取书籍搜索关键词
    book_search_query = request.GET.get('book_search')

    # 如果有搜索关键词，则过滤书籍列表
    if book_search_query:
        books = books.filter(book_name__icontains=book_search_query)

    # 获取作者搜索关键词
    author_search_query = request.GET.get('author_search')

    # 如果有搜索关键词，则过滤作者列表
    if author_search_query:
        authors = AuthorTable.objects.filter(author_name__icontains=author_search_query)

        # 通过作者书籍表获取作者写过的书
        author_books = AuthorBook.objects.filter(author_id__in=authors.values_list('author_id', flat=True))
        book_ids = author_books.values_list('book_id', flat=True)

        # 通过书籍表获取与作者关联的书籍
        related_books = Book.objects.filter(book_id__in=book_ids)

        return render(request, 'book_list.html', {'books': books, 'authors': authors, 'related_books': related_books, 'author_books': author_books})

    return render(request, 'book_list.html', {'books': books})


def index(request):
    return HttpResponse("Hello World!")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        post_data = request.POST
        username = post_data.get("user")
        password = post_data.get("pwd")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("http://127.0.0.1:8000/book_list")
        else:
            return render(request, "login.html", {"tip": "用户名或密码错误!"})
        
def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        post_data = request.POST
        username = post_data.get("user")
        password = post_data.get("pwd")
        first_name = post_data.get("first_name", "")  # 提供一个默认值，或者从表单中获取
        last_name = post_data.get("last_name", "")  # 提供一个默认值，或者从表单中获取
        email = post_data.get("email", "")  # 提供一个默认值，或者从表单中获取

        # 创建用户并提供 email
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        # 进行用户认证
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 登录用户
            auth_login(request, user)
            return redirect("http://127.0.0.1:8000/book_list")
        else:
            return render(request, "register.html", {"tip": "注册失败，请重试"})

@login_required        
def search_books(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')  # 获取用户输入的查询关键字，默认为空字符串

        # 使用模型的 filter 方法进行查询
        books = Book.objects.filter(book_name__icontains=query)

        return render(request, 'search_results.html', {'books': books, 'query': query})