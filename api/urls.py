from django.urls import path 
from . import views


urlpatterns = [
    path('', views.apiOverview, name = "api-overview"),
    path('task-list/', views.taskList, name = "task-list"),
    path('task/<int:pk>/', views.taskDetail, name = "detail"),
    path('task-create/', views.create_task, name = "create"),
    path('task-update/<int:pk>/', views.update_task, name = "update"),
    path('task-delete/<int:pk>/', views.delete_task, name = "delete"),
]