from django.urls import path
from . import views

urlpatterns = [
    path('create-task', views.task_creation, name='create_task'),
    path('retrieve-tasks', views.task_retrieval, name='retrieve_tasks'),
]