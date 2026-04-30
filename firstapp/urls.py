from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.user_signin, name='user_signin'),
    path('signup', views.user_signup, name='user_signup'),
    path('hello/', views.hello_world, name='hello_world'),
    path('hello-class/', views.HelloWorldView.as_view(), name='hello_world_class'),
]