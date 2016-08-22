from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'books/add$', views.add, name='add'),
    url(r'user/(?P<user_id>\d+)$', views.user, name='user'),
    url(r'books$', views.books, name='books'),
    url(r'books/(?P<book_id>\d+)$', views.specific, name='specific'),
    url(r'^user/login_process$', views.login_process, name='login_process'),
    url(r'^user/register_process$', views.register_process, name='register_process'),
    url(r'^user/logout$', views.logout, name='logout'),
    url(r'^books/add_book$', views.add_book, name='add_book'),
    url(r'^books/(?P<book_id>\d+)/add_review$', views.add_review, name='add_review'),
    url(r'^reviews/(?P<review_id>\d+)/delete$', views.delete_review, name='delete_review')

]
