from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')

class UserManager(models.Manager):
    def validateReg(self, request):
        errors = []
        if len(request.POST['name']) < 2:
            errors.append('Name can not be less than 2 characters')
        elif not request.POST['name'].isalpha() and request.POST['name'].isspace():
            errors.append('Name should only contain letters')

        if len(request.POST['email']) < 1:
            errors.append('Email can not be empty')
        elif not EMAIL_REGEX.match(request.POST['email']):
            errors.append('Email is not valid')

        try:
            user = User.objects.get(email = request.POST['email'])
            errors.append('This email is already being used')
        except ObjectDoesNotExist:
            pass

        try:
            user = User.objects.get(alias = request.POST['alias'])
            errors.append('This alias is already being used')
        except ObjectDoesNotExist:
            pass

        if len(errors) > 0:
            return (False, errors)
        return (True, "none")

    def validateRegPass(self, request):
        errors = []
        if len(request.POST['password']) < 1:
            errors.append('Password can not be empty')
        elif len(request.POST['password']) < 8:
            errors.append('Password should be more than 7 characters')
        elif not PASS_REGEX.match(request.POST['password']):
            errors.append('Password should contain at least one apper case letter and one number')
        if request.POST['password'] != request.POST['repeat']:
            errors.append('Password repeat did not match the password')

        if len(errors) > 0:
            return (False, errors)
        return (True, "none")

    def validateLogin(self, request):
        from bcrypt import hashpw, gensalt
        errors = []
        try:
	        user = self.get(email=request.POST['email'])
	        password = user.pw_hash.encode()
	        loginpass = request.POST['password'].encode()
	        print password
	        print hashpw(loginpass, password)
	        if hashpw(loginpass, password) == password:
	            return (True, user)
	        else:
	            errors.append("Sorry, no password match. Please try again.")
	            return (False, errors)
        except ObjectDoesNotExist:
            pass
        errors.append("Sorry, no email found. Please try again.")
        return (False, errors)

    def delete(self, user_id):
        self.filter(id = user_id).delete()

class User(models.Model):
      name = models.CharField(max_length=255)
      alias = models.CharField(max_length=45)
      email = models.EmailField(max_length=45)
      pw_hash = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

      objects = models.Manager()
      manager = UserManager()

class Book(models.Model):
      title = models.CharField(max_length=255)
      author = models.CharField(max_length=255)
      user_id = models.ForeignKey(User, related_name='book_to_user')
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
      review = models.TextField(max_length=1000)
      rating = models.PositiveSmallIntegerField()
      user_id = models.ForeignKey(User, related_name='review_to_user')
      book_id = models.ForeignKey(Book, related_name='review_to_book')
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
