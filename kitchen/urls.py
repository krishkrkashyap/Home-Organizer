from django.urls import path
from . import views

app_name = 'kitchen'
urlpatterns = [
    # Pantry
    path('pantry/', views.pantry_list, name='pantry_list'),
    path('pantry/create/', views.pantry_create, name='pantry_create'),
    path('pantry/<int:pk>/edit/', views.pantry_edit, name='pantry_edit'),
    path('pantry/<int:pk>/delete/', views.pantry_delete, name='pantry_delete'),
    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/create/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
    # Grocery (will be added in Task 10)
    # Menu (will be added in Task 10)
]
