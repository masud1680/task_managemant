from django.urls import path

from . import views

urlpatterns = [
    path("manager-dashboard/", views.manager_dashboard),
    path('user-dashboard/', views.users_dashboard),
    path('view-task/', views.view_task, name='view-task'),
    
    path('create-task/', views.create_task)
    
]