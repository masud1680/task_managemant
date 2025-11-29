from django.urls import path

from . import views

urlpatterns = [
    # path("manager-dashboard/", views.manager_dashboard, name='manager-dashboard'),
    path("manager-dashboard/", views.Manager_dashboard.as_view(), name='manager-dashboard'),
    # path('user-dashboard/', views.employee_dashboard, name='user-dashboard'),
    path('user-dashboard/', views.EmployeeDashboard.as_view(), name='user-dashboard'),
    # path('view-project/', views.view_project, name='view-projects'),
    path('view-project/', views.ViewProjects.as_view(), name='view-projects'),
    # path('task-details/<int:task_id>/', views.task_details, name='task-details'),
    path('task-details/<int:task_id>/', views.TaskDetails.as_view(), name='task-details'),
    # path('create-task/', views.create_task, name='create-task'),
    path('create-task/', views.CreateTask.as_view(), name='create-task'),
    path('update-task/<int:id>/', views.update_task, name='update-task'),
    # path('delete-task/<int:id>/', views.delete_task, name='delete-task'),
    path('delete-task/<int:id>/', views.DeleteTaskView.as_view(), name='delete-task'),
   
    path('dashboard-redirect/', views.deshboard_redirect , name='dashboard-redirect'),
    
]