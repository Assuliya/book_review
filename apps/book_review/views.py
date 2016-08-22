from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import User, Book, Review
import bcrypt
from collections import Counter

def index(request):
    return render(request, 'book_review/index.html')

def add(request):
    books = Book.objects.all()
    context = {'books':books}
    return render(request, 'book_review/add.html', context)

def user(request, user_id):
    user = User.objects.get(id = user_id)
    reviews = Review.objects.filter(user_id = user_id)
    repeat = []
    for y in (0,len(reviews)-1):
        if any(reviews[y].book_id.title in s for s in repeat):
            reviews[y].book_id.title=''
        repeat.append(reviews[y].book_id.title)
        print reviews[y].book_id.title
    total = Review.objects.filter(user_id = user_id).count()
    context = {'user':user, 'reviews': reviews, 'total': total}
    return render(request, 'book_review/user.html', context)

def books(request):
    books = Book.objects.all()
    recent = Review.objects.all().order_by('-created_at')[:3]

    context = {'books':books, 'recent':recent}

    return render(request, 'book_review/books.html', context)

def specific(request, book_id):
    book = Book.objects.get(id = book_id)
    reviews = Review.objects.filter(book_id=book_id)
    context = {'book':book, 'reviews': reviews}
    return render(request, 'book_review/specific.html', context)



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

def add_book(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        errors = []
        if len(request.POST['title']) < 1:
            errors.append('Title can not be empty')
        if len(request.POST['author2']) < 1:
            if request.POST['author1'] == 'select':
                errors.append('Author can not be empty')
            author = request.POST['author1']
        author = request.POST['author2']
        if len(request.POST['review']) < 1:
            errors.append('Review can not be empty')
        if len(errors) > 0:
            print_messages(request, errors)
            return redirect(reverse('add'))

        book = Book.objects.create(title = request.POST['title'], author = author, user_id = user)
        review = Review.objects.create(review = request.POST['review'], rating = request.POST['rating'], user_id = user, book_id = book)
        return redirect(reverse('specific', kwargs={'book_id':book.id}))
    else:
	    return redirect(reverse('index'))

def add_review(request, book_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        book = Book.objects.get(id=book_id)
        review = Review.objects.create(review = request.POST['review'], rating = request.POST['rating'], user_id = user, book_id = book)

        return redirect(reverse('specific', kwargs={'book_id':book_id}))
    else:
	    return redirect(reverse('index'))

def delete_review(self, review_id):
    review = Review.objects.get(id = review_id)
    page = review.book_id.id
    print page
    Review.objects.filter(id = review_id).delete()
    return redirect(reverse('specific', kwargs={'book_id':page}))
