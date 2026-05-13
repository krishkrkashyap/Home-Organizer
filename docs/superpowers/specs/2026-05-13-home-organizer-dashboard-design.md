# Home Organizer Dashboard — Design Spec

## Overview
Django-based home management dashboard for tracking staff, salary, kitchen inventory, tasks, and personal reminders. Three phased builds.

---

## Phase 1: Staff, Leave, Advance, Salary

### Models

**StaffProfile**
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Required |
| phone | CharField | Optional |
| email | EmailField | Optional |
| role | CharField | ChoiceField: Servant/Driver/Cook/Marketer/Gardener/Security + `custom_role` free text |
| photo | ImageField | Optional |
| salary_amount | DecimalField | Monthly salary |
| salary_date | IntegerField | Day of month 1-31 |
| deduction_type | CharField | Choice: `per_day_rate` / `fixed_amount` |
| deduction_value | DecimalField | Nullable — used if fixed_amount |
| advance_balance | DecimalField | Running total of un-repaid advances |
| is_active | BooleanField | Default True |

**LeaveRecord**
| Field | Type | Notes |
|-------|------|-------|
| staff | ForeignKey | -> StaffProfile |
| date | DateField | Date of leave |
| leave_type | CharField | Choice: `half` / `full` |
| note | TextField | Optional |
| created_at | DateTimeField | Auto |

**AdvanceRequest**
| Field | Type | Notes |
|-------|------|-------|
| staff | ForeignKey | -> StaffProfile |
| amount | DecimalField | |
| note | TextField | Optional |
| created_at | DateTimeField | Auto |
| is_settled | BooleanField | Becomes True when deducted in salary |

**SalaryRecord**
| Field | Type | Notes |
|-------|------|-------|
| staff | ForeignKey | -> StaffProfile |
| month | IntegerField | 1-12 |
| year | IntegerField | |
| gross_salary | DecimalField | Copied from profile |
| total_leaves | DecimalField | Half=0.5, Full=1 |
| leave_deduction | DecimalField | Calculated |
| advance_deduction | DecimalField | Sum of unsettled advances |
| net_salary | DecimalField | gross - leave_deduction - advance_deduction |
| paid | BooleanField | Default False |
| paid_date | DateField | Nullable |

### Salary Calculation Logic
```
leave_deduction = total_leaves × (salary_amount / 30)
  — OR custom deduction_value if deduction_type == 'fixed_amount'

advance_deduction = sum of all unsettled AdvanceRequest for this staff

net_salary = gross_salary - leave_deduction - advance_deduction
```

On marking paid: mark all unsettled advances as settled, reset advance_balance to 0.

### Views
- Staff list / create / edit / detail
- Staff detail page with integrated FullCalendar (leave marking)
- Leave calendar with color coding: orange=half, red=full
- Advance request form on staff detail
- Salary generation page (select staff + month → preview → confirm)
- Salary history list per staff

### Permissions
- Admin (superuser) has full access
- Staff users get limited access — can only see own profile, mark own leave, request advance
- Custom permission system using Django auth groups

---

## Phase 2: Grocery, Pantry, Menu Planning, Inventory

### Models

**Category** (shared for grocery/pantry/inventory)
| Field | Type |
|-------|------|
| name | CharField |

**PantryItem** (what's at home)
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | |
| category | ForeignKey | -> Category |
| quantity | DecimalField | Current stock |
| unit | CharField | kg, g, L, ml, pieces, etc |
| min_quantity | DecimalField | Optional low-stock alert |

**GroceryList**
| Field | Type | Notes |
|-------|------|-------|
| created_by | ForeignKey | -> StaffProfile |
| created_at | DateTimeField | Auto |
| is_purchased | BooleanField | Default False |

**GroceryItem**
| Field | Type | Notes |
|-------|------|-------|
| grocery_list | ForeignKey | -> GroceryList |
| name | CharField | |
| category | ForeignKey | -> Category |
| quantity_needed | DecimalField | |
| unit | CharField | |
| quantity_at_home | DecimalField | Auto-filled from PantryItem |
| quantity_to_buy | DecimalField | Computed: needed - at_home (min 0) |
| is_purchased | BooleanField | |

**Shopping list generation**: When GroceryList is finalized, compute `quantity_to_buy = max(0, quantity_needed - quantity_at_home)`. Only show items where quantity_to_buy > 0.

**On purchase**: Update PantryItem.quantity += quantity_purchased.

**InventoryItem**
| Field | Type |
|-------|------|
| name | CharField |
| category | CharField | crockery / equipment / appliance / other |
| quantity | IntegerField |
| condition | CharField | new / good / needs_repair / damaged |
| notes | TextField |

**MenuPlan**
| Field | Type | Notes |
|-------|------|-------|
| cook | ForeignKey | -> StaffProfile |
| date | DateField | |
| meal_type | CharField | breakfast / lunch / dinner / snack |
| dish_name | CharField | |
| ingredients | JSONField | List of {name, quantity, unit} |
| steps | JSONField | Ordered list of {step_number, description, is_completed} |
| is_completed | BooleanField | |

### Views
- Pantry CRUD (stock management)
- Grocery list create — auto-comparison with pantry
- Shopping list view (filtered to items_to_buy)
- Inventory CRUD (crockery/equipment tracker)
- Menu plan create/detail (with step checkboxes)

### Permissions
- Admin: full access
- Cook: can manage menu plans + grocery lists
- Marketer: can view grocery lists, mark items purchased
- Configurable via Django admin

---

## Phase 3: Tasks & Reminders

### Models

**TaskCategory** (e.g. Cleaning, Kitchen, Vehicle, Laundry)
| Field | Type |
|-------|------|
| name | CharField |

**TaskTemplate**
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | e.g. "Wash utensils" |
| description | TextField | |
| category | ForeignKey | -> TaskCategory |
| frequency | CharField | daily / weekly / monthly / one_time |
| day_of_week | IntegerField | Nullable — for weekly (0=Mon..6=Sun) |
| day_of_month | IntegerField | Nullable — for monthly |

**AssignedTask** (instance of a task for a specific staff on a date)
| Field | Type | Notes |
|-------|------|-------|
| staff | ForeignKey | -> StaffProfile |
| task_template | ForeignKey | -> TaskTemplate |
| assigned_date | DateField | |
| is_completed | BooleanField | |
| completed_at | DateTimeField | Nullable |
| notes | TextField | Optional |

**Task generation**: When admin assigns TaskTemplate to staff, daily tasks auto-create AssignedTask entries. A management command or signal generates recurring tasks.

**Reminder**
| Field | Type | Notes |
|-------|------|-------|
| title | CharField | |
| description | TextField | |
| due_date | DateField | |
| repeat | CharField | none / daily / weekly / monthly / yearly |
| category | CharField | subscription / maintenance / pest / other |
| is_completed | BooleanField | |

### Views
- Task checklist dashboard (per staff view)
- Daily task overview (admin sees all staff tasks)
- Reminder list + create/edit

---

## Tech Stack & Setup

| Component | Choice |
|-----------|--------|
| Backend | Django 5.x |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Frontend | Bootstrap 5 + vanilla JS |
| Calendar | FullCalendar.js |
| Auth | Django auth + permission groups |
| Forms | Django ModelForms |

## URL Structure
```
/                     — Dashboard home
/staff/               — Staff list
/staff/<id>/          — Staff detail (calendar, advances)
/staff/<id>/leave/    — Mark leave (HTMX/JSON)
/staff/<id>/advance/  — Request advance
/salary/              — Salary list
/salary/generate/     — Generate salary for month
/kitchen/pantry/      — Pantry stock
/kitchen/grocery/     — Grocery lists
/kitchen/grocery/create/ — Create with auto-compare
/kitchen/inventory/   — Crockery & equipment
/kitchen/menu/        — Menu plans
/tasks/               — Task dashboard
/tasks/assign/        — Assign tasks to staff
/reminders/           — Personal reminders
```

---

## Implementation Order
1. Project bootstrap + StaffProfile CRUD
2. Leave calendar (FullCalendar integration)
3. Advance request system
4. Salary generation engine
5. Pantry + Grocery with auto-compare
6. Inventory (crockery/equipment)
7. Menu planning with step checkboxes
8. Task templates + assigned tasks + recurrence
9. Personal reminders

---

## Self-Review Checklist
- [x] No placeholders/TBDs
- [x] Internal consistency (salary date per profile matches deduction logic)
- [x] Scope clear — 3 phases, 9 implementation steps
- [x] Ambiguity resolved (leave types, deduction math, permission model)
- [x] Architecture matches feature descriptions
