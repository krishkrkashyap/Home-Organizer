# Admin Panel Overhaul — Task & Kitchen Apps

## Goal
Enhance Django admin for `tasks_app` and `kitchen` apps with richer list views, fieldsets, inlines, bulk actions, search, filters, and visual polish.

## Approach
Full ModelAdmin overhaul (Approach 2) — no custom admin views, no dashboard widgets.

## Task Admin

### TaskCategory
- **list_display:** `name`, `task_count` (custom method — count of TaskTemplates in category)
- **search_fields:** `name`

### TaskTemplate
- **list_display:** `name`, `category`, `frequency`, `schedule_display` (custom — shows day_of_week or day_of_month), `description_preview`, `task_count`
- **list_filter:** `frequency`, `category`
- **search_fields:** `name`, `description`
- **list_select_related:** `['category']`
- **fieldsets:**
  - **(1) Basic Info** — name, description, category
  - **(2) Schedule** — frequency, day_of_week, day_of_month

### AssignedTask
- **list_display:** `staff`, `task_template`, `assigned_date`, `status_badge` (colored badge for is_completed), `completed_at`, `notes_preview`
- **list_filter:** `is_completed`, `assigned_date`, `staff`, `task_template`
- **search_fields:** `staff__name`, `task_template__name`, `notes`
- **list_select_related:** `['staff', 'task_template__category']`
- **date_hierarchy:** `assigned_date`
- **fieldsets:**
  - **(1) Assignment** — staff, task_template, assigned_date
  - **(2) Status** — is_completed, completed_at, notes
- **actions:** `mark_completed`, `mark_pending`

### Reminder
- **list_display:** `title`, `category`, `due_date`, `overdue_badge` (red if overdue), `repeat`, `is_completed`
- **list_filter:** `category`, `repeat`, `is_completed`
- **search_fields:** `title`, `description`
- **date_hierarchy:** `due_date`
- **fieldsets:**
  - **(1) Reminder Info** — title, description, category
  - **(2) Schedule** — due_date, repeat
  - **(3) Status** — is_completed
- **actions:** `mark_completed`

## Kitchen Admin

### Category
- **list_display:** `name`, `pantry_count`, `inventory_count` (custom methods)

### PantryItem
- **list_display:** `name`, `category`, `quantity`, `unit`, `min_quantity`, `stock_badge` (green/red for is_low), `updated_at`
- **list_filter:** `category`, custom `is_low` filter
- **search_fields:** `name`
- **list_select_related:** `['category']`
- **fieldsets:**
  - **(1) Item Info** — name, category, unit
  - **(2) Stock** — quantity, min_quantity

### GroceryList
- **list_display:** `id`, `created_by`, `created_at`, `is_purchased`, `item_count`, `purchased_at`
- **list_filter:** `is_purchased`, `created_at`
- **search_fields:** `created_by__name`
- **date_hierarchy:** `created_at`
- **inlines:** `GroceryItemInline` (tabular, all GroceryItem fields except grocery_list FK)
- **fieldsets:**
  - **(1) Info** — created_by
  - **(2) Status** — is_purchased, purchased_at
- **actions:** `mark_purchased`

### GroceryItem
- **list_display:** `name`, `grocery_list`, `category`, `quantity_needed`, `quantity_at_home`, `quantity_to_buy` (read-only), `unit`, `is_purchased`
- **list_filter:** `is_purchased`, `category`, `grocery_list`
- **search_fields:** `name`
- **list_select_related:** `['grocery_list', 'category']`
- **readonly_fields:** `quantity_to_buy`

### InventoryItem
- **list_display:** `name`, `category`, `quantity`, `condition_badge` (color-coded), `notes_preview`
- **list_filter:** `category`, `condition`
- **search_fields:** `name`, `notes`
- **fieldsets:**
  - **(1) Item Info** — name, category, quantity
  - **(2) Condition** — condition, notes

### MenuPlan
- **list_display:** `dish_name`, `cook`, `date`, `meal_type`, `status_badge` (is_completed), `ingredients_count`, `steps_count`
- **list_filter:** `meal_type`, `is_completed`, `date`, `cook`
- **search_fields:** `dish_name`, `cook__name`
- **date_hierarchy:** `date`
- **list_select_related:** `['cook']`
- **fieldsets:**
  - **(1) Meal Info** — cook, date, meal_type, dish_name
  - **(2) Recipe** — ingredients (JSON prettified in template), steps (JSON prettified)
  - **(3) Status** — is_completed
- **actions:** `mark_completed`, `mark_pending`

## Shared Patterns

### Color-Coded Badges
All boolean/status fields rendered as colored `<span>` via custom admin methods:
- `is_completed=True` → green badge "✓ Completed"
- `is_completed=False` → red badge "✗ Pending"
- `is_low=True` → orange/red badge "Low Stock"
- `condition` → color per value: new=green, good=blue, needs_repair=orange, damaged=red
- Overdue → red "⚠ Overdue"

### All custom method properties
Each display method uses `short_description`, `allow_tags=True` (Django 4 compat: `format_html`).

### Bulk Actions
- `mark_completed(modeladmin, request, queryset)` — sets is_completed=True
- `mark_pending(modeladmin, request, queryset)` — sets is_completed=False
- `mark_purchased(modeladmin, request, queryset)` — sets is_purchased=True
- All actions return count message via `messages.success`

## Files to Modify
- `tasks_app/admin.py` — rewrite all 4 ModelAdmin classes
- `kitchen/admin.py` — rewrite all 6 ModelAdmin classes + add GroceryItemInline

No model changes needed. No new views/templates.
