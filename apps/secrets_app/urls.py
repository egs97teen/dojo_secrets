from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'register$', views.register, name="register"),
  url(r'login$', views.login, name="login"),
  url(r'logout$', views.logout, name="logout"),
  url(r'main$', views.main, name="main"),
  url(r'popular$', views.popular, name="popular"),
  url(r'secret$', views.secret, name="secret"),
  url(r'^like/(?P<id>\d+)$', views.like, name="like"),
  url(r'^delete/(?P<id>\d+)$', views.delete, name="delete"),
  url(r'^my_likes$', views.my_likes, name="my_likes"),
  url(r'^my_unlikes$', views.my_unlikes, name="my_unlikes")
]