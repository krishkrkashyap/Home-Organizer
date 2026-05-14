from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import Category, GroceryItem, GroceryList, InventoryItem, MenuPlan, PantryItem


class IsLowListFilter(admin.SimpleListFilter):
    title = 'stock status'
    parameter_name = 'is_low'

    def lookups(self, request, model_admin):
        return [('yes', 'Low Stock'), ('no', 'OK')]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(min_quantity__gt=0, quantity__lte=models.F('min_quantity'))
        if self.value() == 'no':
            return queryset.exclude(min_quantity__gt=0, quantity__lte=models.F('min_quantity'))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pantry_count', 'inventory_count']
    search_fields = ['name']

    @admin.display(description='Pantry Items')
    def pantry_count(self, obj):
        return obj.pantryitem_set.count()

    @admin.display(description='Inventory Items')
    def inventory_count(self, obj):
        return obj.inventoryitem_set.count()


@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'unit', 'min_quantity', 'stock_badge', 'updated_at']
    list_filter = ['category', IsLowListFilter]
    search_fields = ['name']
    list_select_related = ['category']
    fieldsets = [
        ('Item Info', {'fields': ['name', 'category', 'unit']}),
        ('Stock', {'fields': ['quantity', 'min_quantity']}),
    ]

    @admin.display(description='Stock')
    def stock_badge(self, obj):
        if obj.is_low():
            return format_html('<span style="color:orange;font-weight:bold;">&#9888; Low ({})</span>', obj.quantity)
        return format_html('<span style="color:green;">&#10003; OK ({})</span>', obj.quantity)


class GroceryItemInline(admin.TabularInline):
    model = GroceryItem
    extra = 1
    fields = ['name', 'category', 'quantity_needed', 'quantity_at_home', 'quantity_to_buy', 'unit', 'is_purchased']
    readonly_fields = ['quantity_to_buy']
    autocomplete_fields = ['category']


@admin.register(GroceryList)
class GroceryListAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'created_at', 'is_purchased_badge', 'item_count', 'purchased_at']
    list_filter = ['is_purchased', 'created_at']
    search_fields = ['created_by__name']
    date_hierarchy = 'created_at'
    inlines = [GroceryItemInline]
    fieldsets = [
        ('Info', {'fields': ['created_by']}),
        ('Status', {'fields': ['is_purchased', 'purchased_at']}),
    ]
    actions = ['mark_purchased']

    @admin.display(description='Purchased')
    def is_purchased_badge(self, obj):
        if obj.is_purchased:
            return format_html('<span style="color:green;font-weight:bold;">&#10003; Purchased</span>')
        return format_html('<span style="color:red;font-weight:bold;">&#10007; Open</span>')

    @admin.display(description='Items')
    def item_count(self, obj):
        return obj.items.count()

    @admin.action(description='Mark selected as purchased')
    def mark_purchased(self, request, queryset):
        updated = queryset.update(is_purchased=True)
        self.message_user(request, f'{updated} grocery list(s) marked as purchased.')


@admin.register(GroceryItem)
class GroceryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'grocery_list_link', 'category', 'quantity_needed', 'quantity_at_home', 'to_buy_display', 'unit', 'is_purchased']
    list_filter = ['is_purchased', 'category', 'grocery_list']
    search_fields = ['name']
    list_select_related = ['grocery_list', 'category']
    readonly_fields = ['quantity_to_buy']

    @admin.display(description='Grocery List')
    def grocery_list_link(self, obj):
        return format_html('<a href="{}">#{}</a>', f'/admin/kitchen/grocerylist/{obj.grocery_list_id}/change/', obj.grocery_list_id)

    @admin.display(description='To Buy')
    def to_buy_display(self, obj):
        if obj.quantity_to_buy > 0:
            return format_html('<span style="color:red;font-weight:bold;">{}</span>', obj.quantity_to_buy)
        return format_html('<span style="color:green;">{}</span>', obj.quantity_to_buy)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'condition_badge', 'notes_preview']
    list_filter = ['category', 'condition']
    search_fields = ['name', 'notes']
    fieldsets = [
        ('Item Info', {'fields': ['name', 'category', 'quantity']}),
        ('Condition', {'fields': ['condition', 'notes']}),
    ]

    @admin.display(description='Condition')
    def condition_badge(self, obj):
        colors = {
            'new': 'green',
            'good': 'blue',
            'needs_repair': 'orange',
            'damaged': 'red',
        }
        color = colors.get(obj.condition, 'gray')
        return format_html('<span style="color:{};font-weight:bold;">{}</span>', color, obj.get_condition_display())

    @admin.display(description='Notes')
    def notes_preview(self, obj):
        if not obj.notes:
            return '—'
        return obj.notes[:60] + '...' if len(obj.notes) > 60 else obj.notes


@admin.register(MenuPlan)
class MenuPlanAdmin(admin.ModelAdmin):
    list_display = ['dish_name', 'cook', 'date', 'meal_type', 'status_badge', 'ingredients_count', 'steps_count']
    list_filter = ['meal_type', 'is_completed', 'date', 'cook']
    search_fields = ['dish_name', 'cook__name']
    date_hierarchy = 'date'
    list_select_related = ['cook']
    fieldsets = [
        ('Meal Info', {'fields': ['cook', 'date', 'meal_type', 'dish_name']}),
        ('Recipe', {'fields': ['ingredients', 'steps']}),
        ('Status', {'fields': ['is_completed']}),
    ]
    actions = ['mark_completed', 'mark_pending']

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_completed:
            return format_html('<span style="color:green;font-weight:bold;">&#10003; Completed</span>')
        return format_html('<span style="color:red;font-weight:bold;">&#10007; Pending</span>')

    @admin.display(description='Ingredients')
    def ingredients_count(self, obj):
        return len(obj.ingredients)

    @admin.display(description='Steps')
    def steps_count(self, obj):
        return len(obj.steps)

    @admin.action(description='Mark selected as completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'{updated} menu(s) marked as completed.')

    @admin.action(description='Mark selected as pending')
    def mark_pending(self, request, queryset):
        updated = queryset.update(is_completed=False)
        self.message_user(request, f'{updated} menu(s) marked as pending.')
