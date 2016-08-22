from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
# from models import User, Message, Comment
import bcrypt

def index(request):
    return render(request, 'book_review/index.html')

def add(request):
    return render(request, 'book_review/add.html')

def user(request):
    return render(request, 'book_review/user.html')

def books(request):

    return render(request, 'book_review/books.html')

def specific(request):
    # user = User.objects.get(id = user_id)
    # context = {'user':user}
    return render(request, 'book_review/specific.html')
