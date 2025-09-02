from django.urls import path

from . import views

urlpatterns = [
    path("manager-dashboard/", views.manager_dashboard, name='manager-dashboard'),
    path('user-dashboard/', views.employee_dashboard, name='user-dashboard'),
    path('view-task/', views.view_task, name='view-task'),
    path('task-details/<int:task_id>/', views.task_details, name='task-details'),
    path('create-task/', views.create_task, name='create-task'),
    path('update-task/<int:id>/', views.update_task, name='update-task'),
    path('delete-task/<int:id>/', views.delete_task, name='delete-task'),
    path('dashboard-redirect/', views.deshboard_redirect , name='dashboard-redirect'),
    
]