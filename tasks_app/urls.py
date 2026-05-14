from django.urls import path
from . import views

app_name = 'tasks_app'
urlpatterns = [
    path('', views.task_dashboard, name='task_dashboard'),
    path('all/', views.task_list, name='task_list'),
    path('assign/', views.task_assign, name='task_assign'),
    path('<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    # Reminders
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/create/', views.reminder_create, name='reminder_create'),
    path('reminders/<int:pk>/edit/', views.reminder_edit, name='reminder_edit'),
    path('reminders/<int:pk>/toggle/', views.reminder_toggle, name='reminder_toggle'),
    path('reminders/<int:pk>/delete/', views.reminder_delete, name='reminder_delete'),
]
