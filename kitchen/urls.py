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
    # Grocery
    path('grocery/', views.grocery_list, name='grocery_list'),
    path('grocery/create/', views.grocery_create, name='grocery_create'),
    path('grocery/<int:pk>/', views.grocery_detail, name='grocery_detail'),
    path('grocery/<int:pk>/purchase/', views.grocery_mark_purchased, name='grocery_purchase'),
    path('grocery/item/<int:pk>/purchase/', views.grocery_purchase_item, name='grocery_item_purchase'),
    # Menu
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/create/', views.menu_create, name='menu_create'),
    path('menu/<int:pk>/edit/', views.menu_edit, name='menu_edit'),
    path('menu/<int:pk>/step/<int:step_num>/toggle/', views.menu_toggle_step, name='menu_toggle_step'),
]
