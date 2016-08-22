from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'books/add$', views.add, name='add'),
    url(r'user/(?P<user_id>\d+)$', views.user, name='user'),
    url(r'books$', views.books, name='books'),
    url(r'books/specific$', views.specific, name='specific'),

    url(r'^user/login_process$', views.login_process, name='login_process'),
    url(r'^user/register_process$', views.register_process, name='register_process'),
    url(r'^user/logout$', views.logout, name='logout')


]
