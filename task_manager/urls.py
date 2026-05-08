from django.urls import path
from . import views

urlpatterns = [
    path('create-task', views.task_creation, name='create_task'),
    path('retrieve-tasks/', views.task_retrieval, name='retrieve_tasks'),
    path('update-task', views.task_update, name='update_task'),
    path('retrieve-updates/', views.task_retrieve_updates, name='retrieve_updates'),
]