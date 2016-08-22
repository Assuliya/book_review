from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import User, Book, Review
import bcrypt

def index(request):
    return render(request, 'book_review/index.html')

def add(request):
    return render(request, 'book_review/add.html')

def user(request, user_id):
    user = User.objects.get(id = user_id)
    context = {'user':user}
    return render(request, 'book_review/user.html', context)

def books(request):

    return render(request, 'book_review/books.html')

def specific(request):

    return render(request, 'book_review/specific.html')



def register_process(request):
    result = User.manager.validateReg(request)
    resultPass = User.manager.validateRegPass(request)
    if result[0] == False or resultPass[0] == False:
        errors = result[1]+resultPass[1]
        print_messages(request, errors)
        return redirect(reverse('index'))
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.manager.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], pw_hash=pw_hash)
    return log_user_in(request, user)

def login_process(request):
    result = User.manager.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('login'))
    return log_user_in(request, result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def log_user_in(request, user):
    request.session['user'] = user.id
    return redirect(reverse('user', kwargs={'user_id':request.session['user']}))

def logout(request):
    user = User.manager.get(id=request.session['user'])
    user.user_level = 0
    user.save(update_fields=None)
    request.session.pop('user')
    return redirect(reverse('index'))
