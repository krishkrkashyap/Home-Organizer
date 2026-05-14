# Staff Authentication & Role-Based Access

## Overview

Implement staff-wise login, role-based dashboards, and a redesigned tabbed staff creation form with manual credential entry.

## 1. Staff Creation Form (Tabbed)

### Layout
Three tabs on `/staff/create/` and `/staff/<pk>/edit/`:

- **Tab 1: Profile** — name, phone, email, photo upload, role selector (dropdown + custom_role text field), is_active toggle
- **Tab 2: Account** — username, password, confirm password (only on create; hidden on edit)
- **Tab 3: Salary** — salary_amount, salary_date, deduction_type dropdown, deduction_value (shown conditionally when deduction_type is fixed_amount)

### Behavior
- On create: validates username uniqueness, password match, creates `User` + `StaffProfile` in one transaction via form save override
- On edit: account fields hidden (username shown as read-only)
- Remove the `auto_create_user` post_save signal (superseded by form)

## 2. Login Redirect

### Custom redirect view
- Replace `LOGIN_REDIRECT_URL = 'dashboard'` with a custom `redirect_on_login` view
- Checks: `request.user.is_superuser` → admin dashboard
- Otherwise: `request.user.staff_profile.role` → role-specific staff dashboard

### Role-based redirect targets
- `is_superuser` → `dashboard` (current admin dashboard)
- `cook` → `kitchen:dashboard` (kitchen-focused)
- `marketer` → `kitchen:grocery_list` (grocery-focused)
- `servant`, `driver`, `gardener`, `security` → `staff:my_dashboard` (task-focused)

## 3. Staff Role Dashboard

### Single view with conditional sections
URL: `/staff/my/dashboard/`

Logic:
```python
def my_dashboard(request):
    staff = request.user.staff_profile
    role = staff.role
    context = {'staff': staff}
    # Common: today's tasks, profile summary, recent salary
    context['today_tasks'] = AssignedTask.objects.filter(staff=staff, assigned_date=today)
    context['recent_salary'] = SalaryRecord.objects.filter(staff=staff).first()
    
    # Role-specific
    if role == 'cook':
        context['today_menus'] = MenuPlan.objects.filter(date=today)
        context['inventory_items'] = InventoryItem.objects.all()[:5]
    elif role == 'marketer':
        context['recent_grocery'] = GroceryList.objects.filter()[:3]
        context['low_pantry'] = [p for p in PantryItem.objects.all() if p.is_low()]
    return render(request, 'staff/my_dashboard.html', context)
```

### Template sections
- Top: welcome + profile card (name, role, photo)
- Stats: active tasks count, salary this month, role-specific counts
- Today's tasks list with toggle buttons
- Role-specific cards (menus for cook, low-stock for marketer)
- Quick action buttons (role-specific)

## 4. Sidebar Adaptation

### By role
- **Superuser**: Full sidebar — Staff, Salaries, Pantry, Grocery, Inventory, Menu Plans, Tasks, Reminders, Admin
- **Cook**: My Dashboard, My Profile, My Salary, Menu Plans, Inventory, Tasks
- **Marketer**: My Dashboard, My Profile, My Salary, Grocery, Pantry, Tasks
- **Others**: My Dashboard, My Profile, My Salary, My Tasks

All roles see: Dashboard link, Logout button.

## 5. Existing Views to Keep

- `my_profile` — read-only staff detail (keep)
- `my_salary` — staff salary list (keep)
- Add `my_tasks` — shows tasks assigned to current staff only

## Files to Change

| File | Change |
|------|--------|
| `staff/models.py` | Remove `auto_create_user` signal import |
| `staff/forms.py` | Add `StaffCreateForm` with account fields; keep `StaffProfileForm` for edit |
| `staff/views.py` | Add `staff_create` override; add `my_dashboard`, `my_tasks` views |
| `staff/urls.py` | Add `my/dashboard/`, `my/tasks/` URLs |
| `staff/signals.py` | Remove file (or disable signal) |
| `staff/apps.py` | Remove signal import in `ready()` |
| `staff/templates/staff/staff_form.html` | Redesign as tabbed form |
| `staff/templates/staff/my_dashboard.html` | New — role-based dashboard |
| `staff/templates/staff/my_tasks.html` | New — staff's own tasks |
| `home_organizer/urls.py` | Replace `LOGIN_REDIRECT_URL` with custom redirect view |
| `home_organizer/views.py` | Add `redirect_on_login` view |
| `templates/base.html` | Update sidebar links by role |
| `static/css/style.css` | Add tabbed form styles |
