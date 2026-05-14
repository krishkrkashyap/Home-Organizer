from django.urls import path
from . import views

app_name = 'staff'
urlpatterns = [
    path('', views.staff_list, name='list'),
    path('create/', views.staff_create, name='create'),
    path('<int:pk>/', views.staff_detail, name='detail'),
    path('<int:pk>/edit/', views.staff_edit, name='edit'),
    path('<int:pk>/delete/', views.staff_delete, name='delete'),
    path('<int:pk>/leave/', views.mark_leave, name='mark_leave'),
    path('<int:pk>/advance/', views.request_advance, name='request_advance'),
    path('<int:pk>/calendar-data/', views.leave_calendar_data, name='calendar_data'),
]
