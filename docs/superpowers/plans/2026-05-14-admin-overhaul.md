# Admin Overhaul — Tasks & Kitchen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enhance Django admin for `tasks_app` and `kitchen` apps with richer list views, fieldsets, inlines, bulk actions, search, filters, and color-coded status badges.

**Architecture:** Pure Django ModelAdmin customization. No model changes, no new views/templates. All changes confined to `tasks_app/admin.py` and `kitchen/admin.py`.

**Tech Stack:** Django 4.2, `django.utils.html.format_html`

**Files Modified:**
- `tasks_app/admin.py` — rewrite all 4 ModelAdmin classes
- `kitchen/admin.py` — rewrite all 6 ModelAdmin classes

---

### Task 1: Rewrite tasks_app/admin.py — TaskCategoryAdmin + TaskTemplateAdmin

**Files:**
- Modify: `tasks_app/admin.py`

- [ ] **Step 1: Write Task 1 code**

Replace `tasks_app/admin.py` content:

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import TaskCategory, TaskTemplate, AssignedTask, Reminder


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_count']
    search_fields = ['name']

    @admin.display(description='Templates')
    def task_count(self, obj):
        return obj.tasktemplate_set.count()


@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'frequency', 'schedule_display', 'description_preview']
    list_filter = ['frequency', 'category']
    search_fields = ['name', 'description']
    list_select_related = ['category']
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'description', 'category']}),
        ('Schedule', {'fields': ['frequency', 'day_of_week', 'day_of_month']}),
    ]

    @admin.display(description='Schedule')
    def schedule_display(self, obj):
        if obj.frequency == 'weekly' and obj.day_of_week is not None:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            return days[obj.day_of_week]
        if obj.frequency == 'monthly' and obj.day_of_month is not None:
            return f'Day {obj.day_of_month}'
        return '—'

    @admin.display(description='Description')
    def description_preview(self, obj):
        if not obj.description:
            return '—'
        return obj.description[:80] + '...' if len(obj.description) > 80 else obj.description
```

- [ ] **Step 2: Verify check passes**

Run: `python manage.py check tasks_app`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 3: Commit**

```bash
git add tasks_app/admin.py
git commit -m "feat: enhance TaskCategory and TaskTemplate admin with fieldsets, schedule display, description preview"
```

---

### Task 2: AssignedTaskAdmin + ReminderAdmin with badges and bulk actions

**Files:**
- Modify: `tasks_app/admin.py`

- [ ] **Step 1: Append AssignedTaskAdmin and ReminderAdmin to tasks_app/admin.py**

Add these classes after `TaskTemplateAdmin` (before the file ends):

```python
@admin.register(AssignedTask)
class AssignedTaskAdmin(admin.ModelAdmin):
    list_display = ['staff', 'task_template', 'assigned_date', 'status_badge', 'completed_at', 'notes_preview']
    list_filter = ['is_completed', 'assigned_date', 'staff', 'task_template']
    search_fields = ['staff__name', 'task_template__name', 'notes']
    list_select_related = ['staff', 'task_template__category']
    date_hierarchy = 'assigned_date'
    fieldsets = [
        ('Assignment', {'fields': ['staff', 'task_template', 'assigned_date']}),
        ('Status', {'fields': ['is_completed', 'completed_at', 'notes']}),
    ]
    actions = ['mark_completed', 'mark_pending']

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_completed:
            return format_html('<span style="color:green;font-weight:bold;">&#10003; Completed</span>')
        return format_html('<span style="color:red;font-weight:bold;">&#10007; Pending</span>')

    @admin.display(description='Notes')
    def notes_preview(self, obj):
        if not obj.notes:
            return '—'
        return obj.notes[:60] + '...' if len(obj.notes) > 60 else obj.notes

    @admin.action(description='Mark selected as completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'{updated} task(s) marked as completed.')

    @admin.action(description='Mark selected as pending')
    def mark_pending(self, request, queryset):
        updated = queryset.update(is_completed=False)
        self.message_user(request, f'{updated} task(s) marked as pending.')


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'due_date', 'overdue_badge', 'repeat', 'is_completed']
    list_filter = ['category', 'repeat', 'is_completed']
    search_fields = ['title', 'description']
    date_hierarchy = 'due_date'
    fieldsets = [
        ('Reminder Info', {'fields': ['title', 'description', 'category']}),
        ('Schedule', {'fields': ['due_date', 'repeat']}),
        ('Status', {'fields': ['is_completed']}),
    ]
    actions = ['mark_completed']

    @admin.display(description='Overdue')
    def overdue_badge(self, obj):
        from datetime import date
        if not obj.is_completed and obj.due_date < date.today():
            return format_html('<span style="color:red;font-weight:bold;">&#9888; Overdue</span>')
        elif obj.is_completed:
            return format_html('<span style="color:green;">&#10003; Done</span>')
        return '—'

    @admin.action(description='Mark selected as completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'{updated} reminder(s) marked as completed.')
```

- [ ] **Step 2: Verify check passes**

Run: `python manage.py check tasks_app`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 3: Commit**

```bash
git add tasks_app/admin.py
git commit -m "feat: enhance AssignedTask and Reminder admin with status badges, bulk actions, fieldsets"
```

---

### Task 3: Rewrite kitchen/admin.py — Category + PantryItem

**Files:**
- Modify: `kitchen/admin.py`

- [ ] **Step 1: Write CategoryAdmin and PantryItemAdmin**

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, PantryItem, GroceryList, GroceryItem, InventoryItem, MenuPlan


class IsLowListFilter(admin.SimpleListFilter):
    title = 'stock status'
    parameter_name = 'is_low'

    def lookups(self, request, model_admin):
        return [('yes', 'Low Stock'), ('no', 'OK')]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(min_quantity__gt=0).filter(quantity__lte=models.F('min_quantity'))
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
```

Note: Add `from django.db import models` at the top import line:

```python
from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import Category, PantryItem, GroceryList, GroceryItem, InventoryItem, MenuPlan
```

- [ ] **Step 2: Verify check passes**

Run: `python manage.py check kitchen`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 3: Commit**

```bash
git add kitchen/admin.py
git commit -m "feat: enhance Category and PantryItem admin with stock badges, custom filter"
```

---

### Task 4: GroceryListAdmin with GroceryItemInline + GroceryItemAdmin

**Files:**
- Modify: `kitchen/admin.py`

- [ ] **Step 1: Add GroceryItemInline and GroceryListAdmin before GroceryItemAdmin**

Add these before the `@admin.register(GroceryItem)` line:

```python
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
```

- [ ] **Step 2: Verify check passes**

Run: `python manage.py check kitchen`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 3: Commit**

```bash
git add kitchen/admin.py
git commit -m "feat: add GroceryList inline, bulk purchase action, GroceryItem admin enhancements"
```

---

### Task 5: InventoryItemAdmin + MenuPlanAdmin

**Files:**
- Modify: `kitchen/admin.py`

- [ ] **Step 1: Add InventoryItemAdmin and MenuPlanAdmin**

Add these after `GroceryItemAdmin`:

```python
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
```

- [ ] **Step 2: Verify check passes**

Run: `python manage.py check kitchen`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 3: Full system check**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 4: Commit**

```bash
git add kitchen/admin.py
git commit -m "feat: enhance InventoryItem and MenuPlan admin with condition badges, bulk actions, fieldsets"
```

---

### Task 6: Push to GitHub

**Files:** None

- [ ] **Step 1: Push**

```bash
git push
```
