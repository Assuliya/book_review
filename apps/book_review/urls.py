from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'books/add$', views.add, name='add'),
    url(r'user$', views.user, name='user'),
    url(r'books$', views.books, name='books'),
    url(r'books/specific$', views.specific, name='specific')


]
