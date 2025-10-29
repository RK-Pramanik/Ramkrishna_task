from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # List of all tasks for logged-in user
    path('', views.task_list, name='list'),

    # Task detail
    path('<int:pk>/', views.task_detail, name='detail'),

    # Create new task (Teacher/Admin)
    path('create/', views.create_task, name='create'),

    # Edit task (Teacher/Admin)
    path('<int:pk>/edit/', views.edit_task, name='edit'),

    # Delete task (Teacher/Admin)
    path('<int:pk>/delete/', views.delete_task, name='delete'),

    # Update status (Student/Teacher/Admin)
    path('<int:pk>/update-status/', views.update_status, name='update_status'),

    # File submission (Student)
    path('<int:pk>/submit/', views.submit_task, name='submit'),
]
