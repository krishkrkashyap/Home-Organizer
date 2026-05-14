from django.contrib import admin
from .models import Category, PantryItem, GroceryList, GroceryItem, InventoryItem, MenuPlan

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'unit', 'is_low']
    list_filter = ['category']

@admin.register(GroceryList)
class GroceryListAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'created_at', 'is_purchased']

@admin.register(GroceryItem)
class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'grocery_list', 'quantity_needed', 'quantity_to_buy', 'is_purchased']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'condition']
    list_filter = ['category', 'condition']

@admin.register(MenuPlan)
class MenuPlanAdmin(admin.ModelAdmin):
    list_display = ['dish_name', 'cook', 'date', 'meal_type', 'is_completed']
    list_filter = ['meal_type', 'is_completed']
