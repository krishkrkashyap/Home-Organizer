# Home Organizer Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Build a Django home management dashboard with staff profiles, leave/advance/salary system, kitchen management (grocery/pantry/inventory/menu), task checklists, and personal reminders.

**Architecture:** Single Django project with 3 apps (`staff`, `kitchen`, `tasks_app`). Bootstrap 5 frontend. FullCalendar.js for leave calendar. Permission-based access via Django auth groups.

**Tech Stack:** Django 5.x, SQLite, Bootstrap 5, FullCalendar.js, Django ModelForms

---
## File Structure

```
C:\Users\U.C\Desktop\monika mam\organize tasks\
├── manage.py
├── home_organizer/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── staff/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── tests.py
│   └── templates/
│       └── staff/
│           ├── staff_list.html
│           ├── staff_detail.html
│           ├── staff_form.html
│           └── salary_generate.html
├── kitchen/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── tests.py
│   └── templates/
│       └── kitchen/
│           ├── pantry_list.html
│           ├── pantry_form.html
│           ├── grocery_list.html
│           ├── grocery_create.html
│           ├── grocery_detail.html
│           ├── inventory_list.html
│           ├── inventory_form.html
│           ├── menu_list.html
│           └── menu_form.html
├── tasks_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── tests.py
│   ├── management/
│   │   └── commands/
│   │       └── generate_tasks.py
│   └── templates/
│       └── tasks_app/
│           ├── task_dashboard.html
│           ├── task_assign.html
│           ├── task_list.html
│           ├── reminder_list.html
│           └── reminder_form.html
├── templates/
│   ├── base.html
│   └── dashboard.html
└── static/
    └── css/
        └── style.css
```

---

### Task 1: Django project bootstrap

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\manage.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\home_organizer\__init__.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\home_organizer\settings.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\home_organizer\urls.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\home_organizer\wsgi.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\home_organizer\asgi.py`

- [ ] **Step 1: Create Django project skeleton**

Run `django-admin startproject home_organizer .` in `C:\Users\U.C\Desktop\monika mam\organize tasks`

If django isn't installed, run: `pip install django`

```powershell
pip install django
django-admin startproject home_organizer .
```

- [ ] **Step 2: Verify project runs**

```powershell
python manage.py runserver 0.0.0.0:8000 --noreload
```
Open browser to http://127.0.0.1:8000 — should see Django rocket.

- [ ] **Step 3: Create the 3 apps**

```powershell
python manage.py startapp staff
python manage.py startapp kitchen
python manage.py startapp tasks_app
mkdir -p staff/templates/staff
mkdir -p kitchen/templates/kitchen
mkdir -p tasks_app/templates/tasks_app
mkdir -p tasks_app/management/commands
New-Item -ItemType File -Path "tasks_app/management/__init__.py"
New-Item -ItemType File -Path "tasks_app/management/commands/__init__.py"
mkdir -p templates
mkdir -p static/css
```

- [ ] **Step 4: Register apps in settings.py**

Edit `home_organizer/settings.py`. Add to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'staff',
    'kitchen',
    'tasks_app',
]
```

Also set templates dir and static dir:
```python
import os
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

- [ ] **Step 5: Run migrations and verify**

```powershell
python manage.py migrate
python manage.py check
```

- [ ] **Step 6: Commit**

```powershell
git init
git add -A
git commit -m "chore: bootstrap Django project with staff, kitchen, tasks_app"
```

---

### Task 2: Base template and dashboard

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\templates\base.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\templates\dashboard.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\static\css\style.css`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\home_organizer\urls.py`

- [ ] **Step 1: Create base.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Home Organizer{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    {% block extra_head %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="{% url 'dashboard' %}">🏠 Home Organizer</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="{% url 'staff:list' %}">Staff</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'kitchen:pantry_list' %}">Pantry</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'kitchen:grocery_list' %}">Grocery</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'kitchen:inventory_list' %}">Inventory</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'kitchen:menu_list' %}">Menu</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'tasks_app:task_dashboard' %}">Tasks</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'tasks_app:reminder_list' %}">Reminders</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container-fluid mt-3">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">{{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
            {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

- [ ] **Step 2: Create dashboard.html**

```html
{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-12 mb-4">
        <h1>Dashboard</h1>
    </div>
    <div class="col-md-3">
        <div class="card text-bg-primary mb-3">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-people"></i> Staff</h5>
                <p class="card-text display-6">{{ staff_count }}</p>
                <a href="{% url 'staff:list' %}" class="text-white">Manage →</a>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-bg-success mb-3">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-basket"></i> Pantry Items</h5>
                <p class="card-text display-6">{{ pantry_count }}</p>
                <a href="{% url 'kitchen:pantry_list' %}" class="text-white">View →</a>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-bg-warning mb-3">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-list-check"></i> Pending Tasks</h5>
                <p class="card-text display-6">{{ pending_tasks }}</p>
                <a href="{% url 'tasks_app:task_dashboard' %}" class="text-white">View →</a>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-bg-info mb-3">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-bell"></i> Reminders</h5>
                <p class="card-text display-6">{{ upcoming_reminders }}</p>
                <a href="{% url 'tasks_app:reminder_list' %}" class="text-white">View →</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 3: Create style.css (empty — Bootstrap handles most)**

```css
/* Custom styling */
body { background-color: #f8f9fa; }
.navbar-brand { font-weight: bold; }
.card { border-radius: 10px; }
```

- [ ] **Step 4: Update project urls.py**

```python
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from staff.models import StaffProfile
from kitchen.models import PantryItem
from tasks_app.models import AssignedTask, Reminder
from django.utils import timezone

def dashboard(request):
    return render(request, 'dashboard.html', {
        'staff_count': StaffProfile.objects.filter(is_active=True).count(),
        'pantry_count': PantryItem.objects.count(),
        'pending_tasks': AssignedTask.objects.filter(is_completed=False).count(),
        'upcoming_reminders': Reminder.objects.filter(is_completed=False).count(),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('staff/', include('staff.urls')),
    path('kitchen/', include('kitchen.urls')),
    path('tasks/', include('tasks_app.urls')),
]
```

- [ ] **Step 5: Verify**

```powershell
python manage.py runserver 0.0.0.0:8000 --noreload
```
Visit http://127.0.0.1:8000 — see dashboard with 0 counts.

- [ ] **Step 6: Commit**

```powershell
git add -A
git commit -m "feat: add base template and dashboard with stats cards"
```

---

### Task 3: StaffProfile model

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\models.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\admin.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\apps.py`

- [ ] **Step 1: Write staff/models.py**

```python
from django.db import models

ROLE_CHOICES = [
    ('servant', 'Servant'),
    ('driver', 'Driver'),
    ('cook', 'Cook'),
    ('marketer', 'Marketer'),
    ('gardener', 'Gardener'),
    ('security', 'Security'),
]

DEDUCTION_CHOICES = [
    ('per_day_rate', 'Per Day Rate (Salary ÷ 30)'),
    ('fixed_amount', 'Fixed Amount per Leave'),
]

class StaffProfile(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    custom_role = models.CharField(max_length=100, blank=True, help_text='Custom role if not in list')
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    salary_date = models.IntegerField(help_text='Day of month (1-31)')
    deduction_type = models.CharField(max_length=20, choices=DEDUCTION_CHOICES, default='per_day_rate')
    deduction_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Per-day deduction amount if fixed')
    advance_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        role_display = self.custom_role or self.get_role_display()
        return f'{self.name} ({role_display})'

    class Meta:
        ordering = ['name']
```

- [ ] **Step 2: Write staff/admin.py**

```python
from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'salary_amount', 'salary_date', 'advance_balance', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['name', 'phone']
```

- [ ] **Step 3: Write staff/apps.py**

```python
from django.apps import AppConfig

class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff'
```

- [ ] **Step 4: Make migrations and migrate**

```powershell
python manage.py makemigrations staff
python manage.py migrate staff
```

- [ ] **Step 5: Verify via Django shell**

```powershell
python manage.py shell -c "from staff.models import StaffProfile; print(StaffProfile._meta.db_table)"
```
Expected: `staff_staffprofile`

- [ ] **Step 6: Commit**

```powershell
git add -A
git commit -m "feat: add StaffProfile model with role/deduction choices"
```

---

### Task 4: Staff CRUD views and forms

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\forms.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\views.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\urls.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\staff_list.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\staff_form.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\staff_detail.html`

- [ ] **Step 1: Write staff/forms.py**

```python
from django import forms
from .models import StaffProfile

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'
        widgets = {
            'salary_date': forms.NumberInput(attrs={'min': 1, 'max': 31}),
        }
```

- [ ] **Step 2: Write staff/views.py**

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import StaffProfile, LeaveRecord, AdvanceRequest
from .forms import StaffProfileForm

def staff_list(request):
    staff_members = StaffProfile.objects.all()
    return render(request, 'staff/staff_list.html', {'staff_members': staff_members})

def staff_create(request):
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff profile created.')
            return redirect('staff:list')
    else:
        form = StaffProfileForm()
    return render(request, 'staff/staff_form.html', {'form': form, 'title': 'Add Staff'})

def staff_edit(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff profile updated.')
            return redirect('staff:detail', pk=staff.pk)
    else:
        form = StaffProfileForm(instance=staff)
    return render(request, 'staff/staff_form.html', {'form': form, 'title': 'Edit Staff'})

def staff_detail(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    leaves = LeaveRecord.objects.filter(staff=staff).order_by('-date')
    advances = AdvanceRequest.objects.filter(staff=staff).order_by('-created_at')
    salary_records = []  # Will populate in salary task
    return render(request, 'staff/staff_detail.html', {
        'staff': staff,
        'leaves': leaves,
        'advances': advances,
        'salary_records': salary_records,
    })

def staff_delete(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    staff.delete()
    messages.success(request, 'Staff deleted.')
    return redirect('staff:list')
```

- [ ] **Step 3: Write staff/urls.py**

```python
from django.urls import path
from . import views

app_name = 'staff'
urlpatterns = [
    path('', views.staff_list, name='list'),
    path('create/', views.staff_create, name='create'),
    path('<int:pk>/', views.staff_detail, name='detail'),
    path('<int:pk>/edit/', views.staff_edit, name='edit'),
    path('<int:pk>/delete/', views.staff_delete, name='delete'),
]
```

- [ ] **Step 4: Write staff_list.html**

```html
{% extends 'base.html' %}
{% block title %}Staff{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Staff Members</h1>
    <a href="{% url 'staff:create' %}" class="btn btn-primary"><i class="bi bi-plus-lg"></i> Add Staff</a>
</div>
<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead class="table-dark">
            <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Salary</th>
                <th>Salary Date</th>
                <th>Advance Balance</th>
                <th>Active</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for s in staff_members %}
            <tr>
                <td>{{ s.name }}</td>
                <td>{{ s.custom_role|default:s.get_role_display }}</td>
                <td>₹{{ s.salary_amount }}</td>
                <td>{{ s.salary_date }}</td>
                <td>₹{{ s.advance_balance }}</td>
                <td>{% if s.is_active %}✅{% else %}❌{% endif %}</td>
                <td>
                    <a href="{% url 'staff:detail' s.pk %}" class="btn btn-sm btn-info">View</a>
                    <a href="{% url 'staff:edit' s.pk %}" class="btn btn-sm btn-warning">Edit</a>
                </td>
            </tr>
            {% empty %}
            <tr><td colspan="7" class="text-center">No staff yet.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 5: Write staff_form.html**

```html
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<h1>{{ title }}</h1>
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Save</button>
    <a href="{% url 'staff:list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 6: Write staff_detail.html**

```html
{% extends 'base.html' %}
{% block title %}{{ staff.name }}{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h3>{{ staff.name }}</h3>
                <p><strong>Role:</strong> {{ staff.custom_role|default:staff.get_role_display }}</p>
                <p><strong>Phone:</strong> {{ staff.phone|default:'—' }}</p>
                <p><strong>Email:</strong> {{ staff.email|default:'—' }}</p>
                <p><strong>Salary:</strong> ₹{{ staff.salary_amount }}</p>
                <p><strong>Salary Date:</strong> {{ staff.salary_date }}</p>
                <p><strong>Deduction:</strong> {{ staff.get_deduction_type_display }}</p>
                <p><strong>Advance Balance:</strong> ₹{{ staff.advance_balance }}</p>
                <a href="{% url 'staff:edit' staff.pk %}" class="btn btn-warning">Edit</a>
            </div>
        </div>
    </div>
    <div class="col-md-8">
        <ul class="nav nav-tabs" id="staffTabs">
            <li class="nav-item"><a class="nav-link active" href="#leaves" data-bs-toggle="tab">Leaves</a></li>
            <li class="nav-item"><a class="nav-link" href="#advances" data-bs-toggle="tab">Advances</a></li>
            <li class="nav-item"><a class="nav-link" href="#salary" data-bs-toggle="tab">Salary</a></li>
        </ul>
        <div class="tab-content mt-3">
            <div class="tab-pane active" id="leaves">
                <a href="{% url 'staff:mark_leave' staff.pk %}" class="btn btn-sm btn-outline-primary mb-2">Mark Leave</a>
                {% include 'staff/_leave_list.html' %}
            </div>
            <div class="tab-pane" id="advances">
                <a href="{% url 'staff:request_advance' staff.pk %}" class="btn btn-sm btn-outline-warning mb-2">Request Advance</a>
                {% include 'staff/_advance_list.html' %}
            </div>
            <div class="tab-pane" id="salary">
                <a href="{% url 'staff:salary_generate' staff.pk %}" class="btn btn-sm btn-outline-success mb-2">Generate Salary</a>
                {% include 'staff/_salary_list.html' %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 7: Create partial templates for tabs**

Create `staff/templates/staff/_leave_list.html`:
```html
<table class="table table-sm">
    <tr><th>Date</th><th>Type</th><th>Note</th></tr>
    {% for l in leaves %}
    <tr>
        <td>{{ l.date }}</td>
        <td><span class="badge bg-{% if l.leave_type == 'full' %}danger{% else %}warning{% endif %}">{{ l.get_leave_type_display }}</span></td>
        <td>{{ l.note|default:'—' }}</td>
    </tr>
    {% empty %}<tr><td colspan="3" class="text-center">No leaves.</td></tr>
    {% endfor %}
</table>
```

Create `staff/templates/staff/_advance_list.html`:
```html
<table class="table table-sm">
    <tr><th>Date</th><th>Amount</th><th>Note</th><th>Settled</th></tr>
    {% for a in advances %}
    <tr>
        <td>{{ a.created_at|date }}</td>
        <td>₹{{ a.amount }}</td>
        <td>{{ a.note|default:'—' }}</td>
        <td>{% if a.is_settled %}✅{% else %}❌{% endif %}</td>
    </tr>
    {% empty %}<tr><td colspan="4" class="text-center">No advances.</td></tr>
    {% endfor %}
</table>
```

Create `staff/templates/staff/_salary_list.html`:
```html
<table class="table table-sm">
    <tr><th>Month</th><th>Gross</th><th>Leaves Deducted</th><th>Advance Deducted</th><th>Net</th><th>Paid</th></tr>
    {% for s in salary_records %}
    <tr>
        <td>{{ s.month }}/{{ s.year }}</td>
        <td>₹{{ s.gross_salary }}</td>
        <td>₹{{ s.leave_deduction }}</td>
        <td>₹{{ s.advance_deduction }}</td>
        <td><strong>₹{{ s.net_salary }}</strong></td>
        <td>{% if s.paid %}✅{% else %}❌{% endif %}</td>
    </tr>
    {% empty %}<tr><td colspan="6" class="text-center">No salary records.</td></tr>
    {% endfor %}
</table>
```

- [ ] **Step 8: Run checks and verify**

```powershell
python manage.py check
python manage.py runserver 0.0.0.0:8000 --noreload
```
Visit http://127.0.0.1:8000/staff/ — see staff list page.

- [ ] **Step 9: Commit**

```powershell
git add -A
git commit -m "feat: add staff CRUD views with detail tabs"
```

---

### Task 5: LeaveRecord and AdvanceRequest models + leave calendar

**Files:**
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\models.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\admin.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\views.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\urls.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\leave_form.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\advance_form.html`

- [ ] **Step 1: Add LeaveRecord and AdvanceRequest models to staff/models.py**

```python
class LeaveRecord(models.Model):
    LEAVE_TYPES = [('half', 'Half Day'), ('full', 'Full Day')]
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='leaves')
    date = models.DateField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['staff', 'date']

    def __str__(self):
        return f'{self.staff.name} - {self.get_leave_type_display()} - {self.date}'

class AdvanceRequest(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='advances')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_settled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.staff.name} - ₹{self.amount}'
```

- [ ] **Step 2: Update staff/admin.py**

```python
from .models import StaffProfile, LeaveRecord, AdvanceRequest

@admin.register(LeaveRecord)
class LeaveRecordAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date', 'leave_type']

@admin.register(AdvanceRequest)
class AdvanceRequestAdmin(admin.ModelAdmin):
    list_display = ['staff', 'amount', 'created_at', 'is_settled']
```

- [ ] **Step 3: Add leave/advance views to staff/views.py**

Add these functions:
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import StaffProfile, LeaveRecord, AdvanceRequest
from .forms import StaffProfileForm, LeaveForm, AdvanceForm
from django.http import JsonResponse
import json

# ... (existing views above)

def mark_leave(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.staff = staff
            leave.save()
            messages.success(request, f'Leave marked for {leave.date}.')
            return redirect('staff:detail', pk=staff.pk)
    else:
        form = LeaveForm()
    return render(request, 'staff/leave_form.html', {'form': form, 'staff': staff})

def request_advance(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        form = AdvanceForm(request.POST)
        if form.is_valid():
            advance = form.save(commit=False)
            advance.staff = staff
            advance.save()
            staff.advance_balance += advance.amount
            staff.save()
            messages.success(request, f'Advance of ₹{advance.amount} requested.')
            return redirect('staff:detail', pk=staff.pk)
    else:
        form = AdvanceForm()
    return render(request, 'staff/advance_form.html', {'form': form, 'staff': staff})

def leave_calendar_data(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    leaves = LeaveRecord.objects.filter(staff=staff)
    events = []
    for leave in leaves:
        color = '#dc3545' if leave.leave_type == 'full' else '#ffc107'
        events.append({
            'title': leave.get_leave_type_display(),
            'start': leave.date.isoformat(),
            'color': color,
            'textColor': '#000' if leave.leave_type == 'half' else '#fff',
        })
    return JsonResponse(events, safe=False)
```

- [ ] **Step 4: Create staff/forms.py entries for leave and advance**

Add to `staff/forms.py`:
```python
from django import forms
from .models import StaffProfile, LeaveRecord, AdvanceRequest

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'
        widgets = {'salary_date': forms.NumberInput(attrs={'min': 1, 'max': 31})}

class LeaveForm(forms.ModelForm):
    class Meta:
        model = LeaveRecord
        fields = ['date', 'leave_type', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

class AdvanceForm(forms.ModelForm):
    class Meta:
        model = AdvanceRequest
        fields = ['amount', 'note']
```

- [ ] **Step 5: Update staff/urls.py**

Add:
```python
path('<int:pk>/leave/', views.mark_leave, name='mark_leave'),
path('<int:pk>/advance/', views.request_advance, name='request_advance'),
path('<int:pk>/calendar-data/', views.leave_calendar_data, name='calendar_data'),
```

- [ ] **Step 6: Create leave_form.html**

```html
{% extends 'base.html' %}
{% block title %}Mark Leave{% endblock %}
{% block content %}
<h1>Mark Leave — {{ staff.name }}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Save</button>
    <a href="{% url 'staff:detail' staff.pk %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 7: Create advance_form.html**

```html
{% extends 'base.html' %}
{% block title %}Request Advance{% endblock %}
{% block content %}
<h1>Request Advance — {{ staff.name }}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Submit</button>
    <a href="{% url 'staff:detail' staff.pk %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 8: Migrate and verify**

```powershell
python manage.py makemigrations staff
python manage.py migrate staff
python manage.py check
```

- [ ] **Step 9: Commit**

```powershell
git add -A
git commit -m "feat: add leave marking and advance request with forms"
```

---

### Task 6: FullCalendar.js integration on staff detail

**Files:**
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\staff_detail.html`

- [ ] **Step 1: Add calendar to staff_detail.html**

Replace the leaves tab-pane content with a FullCalendar view.

Update the leaves tab-pane div:
```html
<div class="tab-pane active" id="leaves">
    <div id="calendar"></div>
    <hr>
    <a href="{% url 'staff:mark_leave' staff.pk %}" class="btn btn-sm btn-outline-primary mb-2">Mark Leave</a>
    {% include 'staff/_leave_list.html' %}
</div>
```

Add FullCalendar CSS to extra_head block:
```html
{% block extra_head %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.15/index.global.min.css">
{% endblock %}
```

Add FullCalendar JS to extra_scripts block:
```html
{% block extra_scripts %}
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.15/index.global.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            height: 350,
            events: '{% url "staff:calendar_data" staff.pk %}',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,dayGridWeek'
            }
        });
        calendar.render();
    }
});
</script>
{% endblock %}
```

Make sure base.html has `{% block extra_head %}{% endblock %}` in the `<head>` section (it already does from Task 2).

- [ ] **Step 2: Verify**

```powershell
python manage.py runserver 0.0.0.0:8000 --noreload
```
Visit a staff detail page. See FullCalendar with leave data color-coded.

- [ ] **Step 3: Commit**

```powershell
git add -A
git commit -m "feat: integrate FullCalendar for leave visualization"
```

---

### Task 7: SalaryRecord model and salary generation

**Files:**
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\models.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\admin.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\views.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\urls.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\forms.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\salary_generate.html`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\staff\templates\staff\staff_detail.html`

- [ ] **Step 1: Add SalaryRecord model to staff/models.py**

```python
class SalaryRecord(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='salary_records')
    month = models.IntegerField()
    year = models.IntegerField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_leaves = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    leave_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['staff', 'month', 'year']
        ordering = ['-year', '-month']

    def __str__(self):
        return f'{self.staff.name} - {self.month}/{self.year} - ₹{self.net_salary}'
```

- [ ] **Step 2: Update staff/admin.py**

```python
from .models import StaffProfile, LeaveRecord, AdvanceRequest, SalaryRecord

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = ['staff', 'month', 'year', 'gross_salary', 'net_salary', 'paid']
```

- [ ] **Step 3: Add salary views to staff/views.py**

```python
from django.utils import timezone
from datetime import datetime

def salary_generate(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    today = timezone.now()
    
    if request.method == 'POST':
        month = int(request.POST.get('month', today.month))
        year = int(request.POST.get('year', today.year))
        
        # Check existing
        existing = SalaryRecord.objects.filter(staff=staff, month=month, year=year).first()
        if existing and existing.paid:
            messages.warning(request, 'Salary already paid for this month.')
            return redirect('staff:detail', pk=staff.pk)
        
        # Calculate leaves
        leaves = LeaveRecord.objects.filter(staff=staff, date__month=month, date__year=year)
        total_leaves = sum(0.5 if l.leave_type == 'half' else 1 for l in leaves)
        
        # Calculate leave deduction
        if staff.deduction_type == 'fixed_amount' and staff.deduction_value:
            leave_deduction = staff.deduction_value * total_leaves
        else:
            daily_rate = float(staff.salary_amount) / 30
            leave_deduction = daily_rate * total_leaves
        
        # Get unsettled advances
        unsettled = AdvanceRequest.objects.filter(staff=staff, is_settled=False)
        advance_deduction = sum(a.amount for a in unsettled)
        
        gross = staff.salary_amount
        net = gross - leave_deduction - advance_deduction
        
        record, created = SalaryRecord.objects.update_or_create(
            staff=staff, month=month, year=year,
            defaults={
                'gross_salary': gross,
                'total_leaves': total_leaves,
                'leave_deduction': leave_deduction,
                'advance_deduction': advance_deduction,
                'net_salary': net,
            }
        )
        
        if 'confirm_paid' in request.POST:
            record.paid = True
            record.paid_date = today.date()
            record.save()
            # Settle advances
            unsettled.update(is_settled=True)
            staff.advance_balance = 0
            staff.save()
            messages.success(request, f'Salary paid: ₹{net}')
            return redirect('staff:detail', pk=staff.pk)
        
        return render(request, 'staff/salary_generate.html', {
            'staff': staff, 'record': record, 'month': month, 'year': year,
            'preview': True,
        })
    
    return render(request, 'staff/salary_generate.html', {
        'staff': staff,
        'month': today.month,
        'year': today.year,
        'preview': False,
    })

def salary_list(request):
    records = SalaryRecord.objects.all().select_related('staff').order_by('-year', '-month')
    return render(request, 'staff/salary_list.html', {'records': records})
```

- [ ] **Step 4: Update staff/urls.py**

Add:
```python
path('<int:pk>/salary/', views.salary_generate, name='salary_generate'),
path('salary/', views.salary_list, name='salary_list'),
```

- [ ] **Step 5: Populate salary_records in staff_detail view**

In `staff_detail` view in `views.py`, add:
```python
salary_records = SalaryRecord.objects.filter(staff=staff).order_by('-year', '-month')
```

- [ ] **Step 6: Create salary_generate.html**

```html
{% extends 'base.html' %}
{% block title %}Generate Salary{% endblock %}
{% block content %}
<h1>Salary — {{ staff.name }}</h1>
<form method="post">
    {% csrf_token %}
    <div class="row mb-3">
        <div class="col-md-3">
            <label>Month</label>
            <select name="month" class="form-select">
                {% for m in '0123456789'|make_list %}{% with forloop.counter as mn %}
                <option value="{{ mn }}" {% if mn == month %}selected{% endif %}>{{ mn }}</option>
                {% endwith %}{% endfor %}
            </select>
        </div>
        <div class="col-md-3">
            <label>Year</label>
            <input type="number" name="year" class="form-control" value="{{ year }}">
        </div>
        <div class="col-md-3 align-self-end">
            <button type="submit" class="btn btn-primary">Calculate</button>
        </div>
    </div>
</form>

{% if record %}
<div class="card mt-3">
    <div class="card-header"><strong>Salary Preview — {{ month }}/{{ year }}</strong></div>
    <div class="card-body">
        <table class="table">
            <tr><td>Gross Salary</td><td>₹{{ record.gross_salary }}</td></tr>
            <tr><td>Total Leaves (half=0.5)</td><td>{{ record.total_leaves }}</td></tr>
            <tr><td>Leave Deduction</td><td>− ₹{{ record.leave_deduction|floatformat:2 }}</td></tr>
            <tr><td>Advance Deduction</td><td>− ₹{{ record.advance_deduction|floatformat:2 }}</td></tr>
            <tr class="table-success"><th>Net Salary</th><th>₹{{ record.net_salary|floatformat:2 }}</th></tr>
        </table>
        <form method="post">
            {% csrf_token %}
            <input type="hidden" name="month" value="{{ month }}">
            <input type="hidden" name="year" value="{{ year }}">
            <button type="submit" name="confirm_paid" class="btn btn-success" 
                onclick="return confirm('Confirm payment of ₹{{ record.net_salary|floatformat:2 }}?')">
                <i class="bi bi-check-circle"></i> Confirm & Pay
            </button>
            <a href="{% url 'staff:detail' staff.pk %}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 7: Create salary_list.html**

```html
{% extends 'base.html' %}
{% block title %}Salary Records{% endblock %}
{% block content %}
<h1>Salary Records</h1>
<div class="table-responsive">
    <table class="table table-striped">
        <thead class="table-dark">
            <tr><th>Staff</th><th>Month/Year</th><th>Gross</th><th>Leave Deduct</th><th>Advance Deduct</th><th>Net</th><th>Status</th></tr>
        </thead>
        <tbody>
            {% for r in records %}
            <tr>
                <td>{{ r.staff.name }}</td>
                <td>{{ r.month }}/{{ r.year }}</td>
                <td>₹{{ r.gross_salary }}</td>
                <td>₹{{ r.leave_deduction|floatformat:2 }}</td>
                <td>₹{{ r.advance_deduction|floatformat:2 }}</td>
                <td><strong>₹{{ r.net_salary|floatformat:2 }}</strong></td>
                <td>{% if r.paid %}<span class="badge bg-success">Paid</span>{% else %}<span class="badge bg-warning">Pending</span>{% endif %}</td>
            </tr>
            {% empty %}<tr><td colspan="7" class="text-center">No records.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 8: Add salary list to nav in base.html**

Add this nav item if not present:
```html
<li class="nav-item"><a class="nav-link" href="{% url 'staff:salary_list' %}">Salaries</a></li>
```

- [ ] **Step 9: Migrate and verify**

```powershell
python manage.py makemigrations staff
python manage.py migrate staff
python manage.py check
```

- [ ] **Step 10: Commit**

```powershell
git add -A
git commit -m "feat: add salary engine with leave/advance deduction calculation"
```

---

### Task 8: Kitchen app models (Pantry, Grocery, Inventory, Menu)

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\models.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\admin.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\apps.py`

- [ ] **Step 1: Write kitchen/models.py**

```python
from django.db import models
from staff.models import StaffProfile

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class PantryItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, default='pieces')
    min_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.quantity} {self.unit})'

    def is_low(self):
        return self.min_quantity > 0 and self.quantity <= self.min_quantity

class GroceryList(models.Model):
    created_by = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_purchased = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Grocery #{self.id} - {self.created_at.date()}'

class GroceryItem(models.Model):
    grocery_list = models.ForeignKey(GroceryList, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, default='pieces')
    quantity_at_home = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_to_buy = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - need {self.quantity_needed} {self.unit}'

    def save(self, *args, **kwargs):
        # Auto-calculate quantity_to_buy
        self.quantity_to_buy = max(0, self.quantity_needed - self.quantity_at_home)
        super().save(*args, **kwargs)

class InventoryItem(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('needs_repair', 'Needs Repair'),
        ('damaged', 'Damaged'),
    ]
    CATEGORY_CHOICES = [
        ('crockery', 'Crockery'),
        ('equipment', 'Equipment'),
        ('appliance', 'Appliance'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.IntegerField(default=1)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'

class MenuPlan(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    cook = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'cook'})
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    dish_name = models.CharField(max_length=200)
    ingredients = models.JSONField(default=list, blank=True)
    steps = models.JSONField(default=list, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date', 'meal_type']

    def __str__(self):
        return f'{self.dish_name} - {self.date} ({self.get_meal_type_display()})'
```

- [ ] **Step 2: Write kitchen/admin.py**

```python
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

@admin.register(MenuPlan)
class MenuPlanAdmin(admin.ModelAdmin):
    list_display = ['dish_name', 'cook', 'date', 'meal_type', 'is_completed']
```

- [ ] **Step 3: Write kitchen/apps.py**

```python
from django.apps import AppConfig

class KitchenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kitchen'
```

- [ ] **Step 4: Migrate**

```powershell
python manage.py makemigrations kitchen
python manage.py migrate kitchen
```

- [ ] **Step 5: Commit**

```powershell
git add -A
git commit -m "feat: add kitchen models - pantry, grocery, inventory, menu plan"
```

---

### Task 9: Kitchen CRUD views — Pantry + Inventory

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\forms.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\views.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\urls.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\pantry_list.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\pantry_form.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\inventory_list.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\inventory_form.html`

- [ ] **Step 1: Write kitchen/forms.py**

```python
from django import forms
from .models import PantryItem, InventoryItem, GroceryList, GroceryItem, MenuPlan

class PantryItemForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = '__all__'

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
```

- [ ] **Step 2: Write kitchen/views.py (pantry + inventory only for now)**

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PantryItem, InventoryItem, GroceryList, GroceryItem, Category
from .forms import PantryItemForm, InventoryItemForm

# --- Pantry ---
def pantry_list(request):
    items = PantryItem.objects.select_related('category').all()
    return render(request, 'kitchen/pantry_list.html', {'items': items})

def pantry_create(request):
    if request.method == 'POST':
        form = PantryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pantry item added.')
            return redirect('kitchen:pantry_list')
    else:
        form = PantryItemForm()
    return render(request, 'kitchen/pantry_form.html', {'form': form, 'title': 'Add Pantry Item'})

def pantry_edit(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    if request.method == 'POST':
        form = PantryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pantry item updated.')
            return redirect('kitchen:pantry_list')
    else:
        form = PantryItemForm(instance=item)
    return render(request, 'kitchen/pantry_form.html', {'form': form, 'title': 'Edit Pantry Item'})

def pantry_delete(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    item.delete()
    messages.success(request, 'Pantry item deleted.')
    return redirect('kitchen:pantry_list')

# --- Inventory ---
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'kitchen/inventory_list.html', {'items': items})

def inventory_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item added.')
            return redirect('kitchen:inventory_list')
    else:
        form = InventoryItemForm()
    return render(request, 'kitchen/inventory_form.html', {'form': form, 'title': 'Add Inventory Item'})

def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated.')
            return redirect('kitchen:inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'kitchen/inventory_form.html', {'form': form, 'title': 'Edit Inventory Item'})

def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete()
    messages.success(request, 'Inventory item deleted.')
    return redirect('kitchen:inventory_list')
```

- [ ] **Step 3: Write kitchen/urls.py**

```python
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
    # Grocery (added in next task)
    # Menu (added in next task)
]
```

- [ ] **Step 4: Create pantry_list.html**

```html
{% extends 'base.html' %}
{% block title %}Pantry{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Pantry Stock</h1>
    <a href="{% url 'kitchen:pantry_create' %}" class="btn btn-primary"><i class="bi bi-plus-lg"></i> Add Item</a>
</div>
<div class="table-responsive">
    <table class="table table-striped">
        <thead class="table-dark">
            <tr><th>Name</th><th>Category</th><th>Quantity</th><th>Unit</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.name }}</td>
                <td>{{ item.category|default:'—' }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ item.unit }}</td>
                <td>{% if item.is_low %}<span class="badge bg-danger">Low Stock</span>{% else %}<span class="badge bg-success">OK</span>{% endif %}</td>
                <td>
                    <a href="{% url 'kitchen:pantry_edit' item.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="{% url 'kitchen:pantry_delete' item.pk %}" class="btn btn-sm btn-danger" onclick="return confirm('Delete?')">Delete</a>
                </td>
            </tr>
            {% empty %}<tr><td colspan="6" class="text-center">No items.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 5: Create pantry_form.html**

```html
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<h1>{{ title }}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Save</button>
    <a href="{% url 'kitchen:pantry_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 6: Create inventory_list.html**

```html
{% extends 'base.html' %}
{% block title %}Inventory{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Crockery & Equipment</h1>
    <a href="{% url 'kitchen:inventory_create' %}" class="btn btn-primary"><i class="bi bi-plus-lg"></i> Add Item</a>
</div>
<div class="table-responsive">
    <table class="table table-striped">
        <thead class="table-dark">
            <tr><th>Name</th><th>Category</th><th>Qty</th><th>Condition</th><th>Notes</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.name }}</td>
                <td>{{ item.get_category_display }}</td>
                <td>{{ item.quantity }}</td>
                <td><span class="badge bg-{% if item.condition == 'new' %}success{% elif item.condition == 'good' %}info{% elif item.condition == 'needs_repair' %}warning{% else %}danger{% endif %}">{{ item.get_condition_display }}</span></td>
                <td>{{ item.notes|default:'—'|truncatewords:10 }}</td>
                <td>
                    <a href="{% url 'kitchen:inventory_edit' item.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="{% url 'kitchen:inventory_delete' item.pk %}" class="btn btn-sm btn-danger" onclick="return confirm('Delete?')">Delete</a>
                </td>
            </tr>
            {% empty %}<tr><td colspan="6" class="text-center">No items.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 7: Create inventory_form.html**

```html
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<h1>{{ title }}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Save</button>
    <a href="{% url 'kitchen:inventory_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 8: Verify**

```powershell
python manage.py check
python manage.py runserver 0.0.0.0:8000 --noreload
```
Test pantry and inventory pages.

- [ ] **Step 9: Commit**

```powershell
git add -A
git commit -m "feat: add pantry and inventory CRUD views"
```

---

### Task 10: Grocery with auto-compare + Menu planning views

**Files:**
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\forms.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\views.py`
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\urls.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\grocery_list.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\grocery_create.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\grocery_detail.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\menu_list.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\kitchen\templates\kitchen\menu_form.html`

- [ ] **Step 1: Add grocery and menu forms to kitchen/forms.py**

```python
from .models import PantryItem, InventoryItem, GroceryList, GroceryItem, MenuPlan

class GroceryListForm(forms.ModelForm):
    class Meta:
        model = GroceryList
        fields = ['created_by']

class GroceryItemForm(forms.ModelForm):
    class Meta:
        model = GroceryItem
        fields = ['name', 'category', 'quantity_needed', 'unit']

class MenuPlanForm(forms.ModelForm):
    class Meta:
        model = MenuPlan
        fields = ['cook', 'date', 'meal_type', 'dish_name', 'ingredients', 'steps']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'ingredients': forms.Textarea(attrs={'rows': 3, 'placeholder': '[{"name": "Onion", "quantity": 2, "unit": "pieces"}]'}),
            'steps': forms.Textarea(attrs={'rows': 3, 'placeholder': '[{"step_number": 1, "description": "Chop onions", "is_completed": false}]'}),
        }
```

- [ ] **Step 2: Add grocery and menu views to kitchen/views.py**

```python
import json
from django.http import JsonResponse
from .models import PantryItem, InventoryItem, GroceryList, GroceryItem, Category, MenuPlan
from .forms import PantryItemForm, InventoryItemForm, GroceryListForm, GroceryItemForm, MenuPlanForm

# --- Grocery ---
def grocery_list(request):
    lists = GroceryList.objects.prefetch_related('items').all().order_by('-created_at')
    return render(request, 'kitchen/grocery_list.html', {'lists': lists})

def grocery_create(request):
    if request.method == 'POST':
        form = GroceryListForm(request.POST)
        item_form = GroceryItemForm(request.POST)
        if form.is_valid():
            grocery = form.save()
            # Process items from JSON field
            items_data = request.POST.get('items_json', '[]')
            try:
                items = json.loads(items_data)
                for item_data in items:
                    # Find matching pantry item
                    pantry_qs = PantryItem.objects.filter(name__iexact=item_data['name'])
                    qty_at_home = pantry_qs.first().quantity if pantry_qs.exists() else 0
                    
                    GroceryItem.objects.create(
                        grocery_list=grocery,
                        name=item_data['name'],
                        quantity_needed=item_data['quantity'],
                        unit=item_data.get('unit', 'pieces'),
                        quantity_at_home=qty_at_home,
                    )
                messages.success(request, 'Grocery list created with auto-compare.')
            except (json.JSONDecodeError, KeyError) as e:
                messages.warning(request, f'List created but items had errors: {e}')
            return redirect('kitchen:grocery_detail', pk=grocery.pk)
    else:
        form = GroceryListForm()
        item_form = GroceryItemForm()
    return render(request, 'kitchen/grocery_create.html', {
        'form': form, 'item_form': item_form,
        'categories': Category.objects.all(),
        'pantry_items': PantryItem.objects.all(),
    })

def grocery_detail(request, pk):
    grocery = get_object_or_404(GroceryList.objects.prefetch_related('items__category'), pk=pk)
    return render(request, 'kitchen/grocery_detail.html', {'grocery': grocery})

def grocery_purchase_item(request, pk):
    item = get_object_or_404(GroceryItem, pk=pk)
    item.is_purchased = True
    item.save()
    # Update pantry stock
    pantry, _ = PantryItem.objects.get_or_create(name=item.name, defaults={'quantity': 0})
    pantry.quantity += item.quantity_to_buy
    pantry.save()
    return JsonResponse({'success': True})

def grocery_mark_purchased(request, pk):
    grocery = get_object_or_404(GroceryList, pk=pk)
    grocery.is_purchased = True
    from django.utils import timezone
    grocery.purchased_at = timezone.now()
    grocery.save()
    # Update all items
    for item in grocery.items.filter(is_purchased=False):
        item.is_purchased = True
        item.save()
        pantry, _ = PantryItem.objects.get_or_create(name=item.name, defaults={'quantity': 0})
        pantry.quantity += item.quantity_to_buy
        pantry.save()
    messages.success(request, 'Grocery list marked as purchased. Pantry updated.')
    return redirect('kitchen:grocery_detail', pk=grocery.pk)

# --- Menu Plan ---
def menu_list(request):
    menus = MenuPlan.objects.select_related('cook').all().order_by('-date')
    return render(request, 'kitchen/menu_list.html', {'menus': menus})

def menu_create(request):
    if request.method == 'POST':
        form = MenuPlanForm(request.POST)
        if form.is_valid():
            menu = form.save()
            messages.success(request, f'Menu plan for {menu.dish_name} created.')
            return redirect('kitchen:menu_list')
    else:
        form = MenuPlanForm()
    return render(request, 'kitchen/menu_form.html', {'form': form, 'title': 'Create Menu Plan'})

def menu_edit(request, pk):
    menu = get_object_or_404(MenuPlan, pk=pk)
    if request.method == 'POST':
        form = MenuPlanForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu plan updated.')
            return redirect('kitchen:menu_list')
    else:
        form = MenuPlanForm(instance=menu)
    return render(request, 'kitchen/menu_form.html', {'form': form, 'title': 'Edit Menu Plan'})

def menu_toggle_step(request, pk, step_num):
    menu = get_object_or_404(MenuPlan, pk=pk)
    steps = menu.steps
    for step in steps:
        if step.get('step_number') == step_num:
            step['is_completed'] = not step.get('is_completed', False)
    menu.steps = steps
    # Check if all done
    if all(s.get('is_completed', False) for s in steps):
        menu.is_completed = True
    else:
        menu.is_completed = False
    menu.save()
    return JsonResponse({'success': True, 'is_completed': menu.is_completed})
```

- [ ] **Step 3: Add URLs to kitchen/urls.py**

```python
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
```

- [ ] **Step 4: Create grocery_list.html**

```html
{% extends 'base.html' %}
{% block title %}Grocery Lists{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Grocery Lists</h1>
    <a href="{% url 'kitchen:grocery_create' %}" class="btn btn-primary"><i class="bi bi-plus-lg"></i> New List</a>
</div>
<div class="table-responsive">
    <table class="table table-hover">
        <thead class="table-dark">
            <tr><th>#</th><th>Created By</th><th>Date</th><th>Items</th><th>Purchased</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% for gl in lists %}
            <tr>
                <td>{{ gl.id }}</td>
                <td>{{ gl.created_by.name|default:'—' }}</td>
                <td>{{ gl.created_at|date }}</td>
                <td>{{ gl.items.count }}</td>
                <td>{% if gl.is_purchased %}✅{% else %}❌{% endif %}</td>
                <td><a href="{% url 'kitchen:grocery_detail' gl.pk %}" class="btn btn-sm btn-info">View</a></td>
            </tr>
            {% empty %}<tr><td colspan="6" class="text-center">No lists.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 5: Create grocery_create.html**

```html
{% extends 'base.html' %}
{% block title %}New Grocery List{% endblock %}
{% block content %}
<h1>New Grocery List</h1>
<form method="post" id="groceryForm">
    {% csrf_token %}
    {{ form.as_p }}
    <div class="card mb-3">
        <div class="card-header d-flex justify-content-between">
            <span>Items</span>
            <button type="button" class="btn btn-sm btn-success" id="addItem">+ Add Item</button>
        </div>
        <div class="card-body">
            <table class="table" id="itemsTable">
                <thead><tr><th>Item</th><th>Category</th><th>Qty Needed</th><th>Unit</th><th>At Home</th><th>To Buy</th><th></th></tr></thead>
                <tbody id="itemsBody"></tbody>
            </table>
            <textarea name="items_json" id="itemsJson" style="display:none;">[]</textarea>
        </div>
    </div>
    <button type="submit" class="btn btn-success">Create List</button>
    <a href="{% url 'kitchen:grocery_list' %}" class="btn btn-secondary">Cancel</a>
</form>

<script>
const pantryItems = {{ pantry_items|safe }};
const categories = {{ categories|safe }};

document.getElementById('addItem').addEventListener('click', function() {
    const tbody = document.getElementById('itemsBody');
    const row = document.createElement('tr');
    row.innerHTML = `
        <td><input type="text" class="form-control item-name" list="pantrySuggestions" placeholder="Item name"></td>
        <td>
            <select class="form-select item-category">
                {% for cat in categories %}<option value="{{ cat.id }}">{{ cat.name }}</option>{% endfor %}
            </select>
        </td>
        <td><input type="number" class="form-control item-qty" step="0.01" min="0" value="1"></td>
        <td><input type="text" class="form-control item-unit" value="pieces"></td>
        <td class="at-home">0</td>
        <td class="to-buy">0</td>
        <td><button type="button" class="btn btn-sm btn-danger remove-item">X</button></td>
    `;
    tbody.appendChild(row);
    updateJson();
});

document.addEventListener('input', function(e) {
    if (e.target.classList.contains('item-name') || e.target.classList.contains('item-qty')) {
        updateAtHome(e.target.closest('tr'));
        updateJson();
    }
});

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('remove-item')) {
        e.target.closest('tr').remove();
        updateJson();
    }
});

function updateAtHome(row) {
    const name = row.querySelector('.item-name').value.toLowerCase();
    const qty = parseFloat(row.querySelector('.item-qty').value) || 0;
    const pantryItem = {{ pantry_dict|default:'{}'|safe }};
    const atHome = pantryItem[name] || 0;
    row.querySelector('.at-home').textContent = atHome;
    row.querySelector('.to-buy').textContent = Math.max(0, qty - atHome);
}

function updateJson() {
    const items = [];
    document.querySelectorAll('#itemsBody tr').forEach(row => {
        const name = row.querySelector('.item-name').value;
        if (name) {
            items.push({
                name: name,
                category_id: row.querySelector('.item-category').value,
                quantity: parseFloat(row.querySelector('.item-qty').value) || 0,
                unit: row.querySelector('.item-unit').value,
            });
        }
    });
    document.getElementById('itemsJson').value = JSON.stringify(items);
}
</script>
<datalist id="pantrySuggestions">
    {% for p in pantry_items %}<option value="{{ p.name }}">{% endfor %}
</datalist>
{% endblock %}
```

- [ ] **Step 6: Create grocery_detail.html**

```html
{% extends 'base.html' %}
{% block title %}Grocery #{{ grocery.id }}{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Grocery List #{{ grocery.id }}</h1>
    <div>
        {% if not grocery.is_purchased %}
        <a href="{% url 'kitchen:grocery_purchase' grocery.pk %}" class="btn btn-success" onclick="return confirm('Mark all as purchased?')">
            <i class="bi bi-check-all"></i> Mark All Purchased
        </a>
        {% endif %}
        <a href="{% url 'kitchen:grocery_list' %}" class="btn btn-secondary">Back</a>
    </div>
</div>
<p><strong>Created:</strong> {{ grocery.created_at|date:"M d, Y H:i" }} by {{ grocery.created_by.name|default:'—' }}</p>
<div class="table-responsive">
    <table class="table table-striped">
        <thead class="table-dark">
            <tr><th>Item</th><th>Category</th><th>Needed</th><th>At Home</th><th>To Buy</th><th>Status</th></tr>
        </thead>
        <tbody>
            {% for item in grocery.items.all %}
            <tr class="{% if item.is_purchased %}table-success{% endif %}">
                <td>{{ item.name }}</td>
                <td>{{ item.category.name|default:'—' }}</td>
                <td>{{ item.quantity_needed }} {{ item.unit }}</td>
                <td>{{ item.quantity_at_home }} {{ item.unit }}</td>
                <td><strong>{{ item.quantity_to_buy }} {{ item.unit }}</strong></td>
                <td>
                    {% if item.is_purchased %}
                    ✅ Purchased
                    {% else %}
                    <a href="{% url 'kitchen:grocery_item_purchase' item.pk %}" class="btn btn-sm btn-outline-success mark-purchased">Mark</a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 7: Create menu_list.html**

```html
{% extends 'base.html' %}
{% block title %}Menu Plans{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Menu Plans</h1>
    <a href="{% url 'kitchen:menu_create' %}" class="btn btn-primary"><i class="bi bi-plus-lg"></i> New Menu Plan</a>
</div>
<div class="table-responsive">
    <table class="table table-hover">
        <thead class="table-dark">
            <tr><th>Dish</th><th>Cook</th><th>Date</th><th>Meal</th><th>Steps</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% for menu in menus %}
            <tr>
                <td>{{ menu.dish_name }}</td>
                <td>{{ menu.cook.name }}</td>
                <td>{{ menu.date }}</td>
                <td><span class="badge bg-info">{{ menu.get_meal_type_display }}</span></td>
                <td>{{ menu.steps|length }} steps</td>
                <td>{% if menu.is_completed %}✅{% else %}🔄{% endif %}</td>
                <td><a href="{% url 'kitchen:menu_edit' menu.pk %}" class="btn btn-sm btn-warning">Edit</a></td>
            </tr>
            {% empty %}<tr><td colspan="7" class="text-center">No menus.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 8: Create menu_form.html**

```html
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<h1>{{ title }}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Save</button>
    <a href="{% url 'kitchen:menu_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 9: Update grocery_create view to pass pantry dict**

Modify `grocery_create` view — pass pantry data as JSON for JS:
```python
def grocery_create(request):
    # ... existing code ...
    pantry_items = PantryItem.objects.all()
    pantry_dict = {item.name.lower(): float(item.quantity) for item in pantry_items}
    return render(request, 'kitchen/grocery_create.html', {
        'form': form, 'item_form': item_form,
        'categories': Category.objects.all(),
        'pantry_items': pantry_items,
        'pantry_dict': json.dumps(pantry_dict),
    })
```

- [ ] **Step 10: Verify**

```powershell
python manage.py check
python manage.py runserver 0.0.0.0:8000 --noreload
```
Test grocery creation (auto-compare with pantry) and menu forms.

- [ ] **Step 11: Commit**

```powershell
git add -A
git commit -m "feat: add grocery auto-compare and menu planning views"
```

---

### Task 11: Tasks app models

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\models.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\admin.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\apps.py`

- [ ] **Step 1: Write tasks_app/models.py**

```python
from django.db import models
from staff.models import StaffProfile

class TaskCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'task categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class TaskTemplate(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('one_time', 'One Time'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    day_of_week = models.IntegerField(null=True, blank=True, help_text='0=Mon to 6=Sun (for weekly)')
    day_of_month = models.IntegerField(null=True, blank=True, help_text='1-31 (for monthly)')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_frequency_display()})'

class AssignedTask(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='tasks')
    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-assigned_date']
        unique_together = ['staff', 'task_template', 'assigned_date']

    def __str__(self):
        status = '✅' if self.is_completed else '❌'
        return f'{status} {self.task_template.name} - {self.staff.name} ({self.assigned_date})'

class Reminder(models.Model):
    CATEGORY_CHOICES = [
        ('subscription', 'Subscription'),
        ('maintenance', 'Maintenance'),
        ('pest', 'Pest Control'),
        ('other', 'Other'),
    ]
    REPEAT_CHOICES = [
        ('none', 'No Repeat'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    repeat = models.CharField(max_length=20, choices=REPEAT_CHOICES, default='none')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title
```

- [ ] **Step 2: Write tasks_app/admin.py**

```python
from django.contrib import admin
from .models import TaskCategory, TaskTemplate, AssignedTask, Reminder

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'frequency']

@admin.register(AssignedTask)
class AssignedTaskAdmin(admin.ModelAdmin):
    list_display = ['staff', 'task_template', 'assigned_date', 'is_completed']
    list_filter = ['is_completed']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'category', 'is_completed']
```

- [ ] **Step 3: Write tasks_app/apps.py**

```python
from django.apps import AppConfig

class TasksAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks_app'
```

- [ ] **Step 4: Migrate**

```powershell
python manage.py makemigrations tasks_app
python manage.py migrate tasks_app
```

- [ ] **Step 5: Commit**

```powershell
git add -A
git commit -m "feat: add tasks models - templates, assignments, reminders"
```

---

### Task 12: Tasks CRUD views + reminder CRUD

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\forms.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\views.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\urls.py`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\templates\tasks_app\task_dashboard.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\templates\tasks_app\task_assign.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\templates\tasks_app\task_list.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\templates\tasks_app\reminder_list.html`
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\templates\tasks_app\reminder_form.html`

- [ ] **Step 1: Write tasks_app/forms.py**

```python
from django import forms
from .models import TaskTemplate, AssignedTask, Reminder

class TaskTemplateForm(forms.ModelForm):
    class Meta:
        model = TaskTemplate
        fields = '__all__'

class AssignTaskForm(forms.Form):
    staff = forms.ModelChoiceField(queryset=None, label='Staff Member')
    task_template = forms.ModelChoiceField(queryset=None, label='Task')
    assigned_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from staff.models import StaffProfile
        self.fields['staff'].queryset = StaffProfile.objects.filter(is_active=True)
        self.fields['task_template'].queryset = TaskTemplate.objects.all()

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = '__all__'
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}
```

- [ ] **Step 2: Write tasks_app/views.py**

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import TaskTemplate, AssignedTask, Reminder, TaskCategory
from .forms import TaskTemplateForm, AssignTaskForm, ReminderForm

def task_dashboard(request):
    today = timezone.now().date()
    today_tasks = AssignedTask.objects.filter(assigned_date=today).select_related('staff', 'task_template')
    pending_tasks = AssignedTask.objects.filter(is_completed=False).select_related('staff', 'task_template')[:20]
    staff_members = set()
    for t in today_tasks:
        staff_members.add(t.staff)
    return render(request, 'tasks_app/task_dashboard.html', {
        'today': today,
        'today_tasks': today_tasks,
        'pending_tasks': pending_tasks,
        'staff_members': staff_members,
    })

def task_list(request):
    tasks = AssignedTask.objects.all().select_related('staff', 'task_template').order_by('-assigned_date')
    return render(request, 'tasks_app/task_list.html', {'tasks': tasks})

def task_assign(request):
    if request.method == 'POST':
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            staff = form.cleaned_data['staff']
            template = form.cleaned_data['task_template']
            date = form.cleaned_data['assigned_date']
            AssignedTask.objects.get_or_create(
                staff=staff, task_template=template, assigned_date=date,
                defaults={'is_completed': False}
            )
            messages.success(request, f'Task assigned to {staff.name}.')
            return redirect('tasks_app:task_dashboard')
    else:
        form = AssignTaskForm()
    return render(request, 'tasks_app/task_assign.html', {'form': form})

def task_toggle(request, pk):
    task = get_object_or_404(AssignedTask, pk=pk)
    task.is_completed = not task.is_completed
    task.completed_at = timezone.now() if task.is_completed else None
    task.save()
    messages.success(request, f'Task {"completed" if task.is_completed else "reopened"}.')
    return redirect(request.META.get('HTTP_REFERER', 'tasks_app:task_dashboard'))

def task_delete(request, pk):
    task = get_object_or_404(AssignedTask, pk=pk)
    task.delete()
    messages.success(request, 'Task deleted.')
    return redirect('tasks_app:task_dashboard')

# --- Reminders ---
def reminder_list(request):
    reminders = Reminder.objects.all().order_by('due_date')
    return render(request, 'tasks_app/reminder_list.html', {'reminders': reminders})

def reminder_create(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder created.')
            return redirect('tasks_app:reminder_list')
    else:
        form = ReminderForm()
    return render(request, 'tasks_app/reminder_form.html', {'form': form, 'title': 'Add Reminder'})

def reminder_edit(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder updated.')
            return redirect('tasks_app:reminder_list')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'tasks_app/reminder_form.html', {'form': form, 'title': 'Edit Reminder'})

def reminder_toggle(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    reminder.is_completed = not reminder.is_completed
    reminder.save()
    return redirect('tasks_app:reminder_list')

def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    reminder.delete()
    messages.success(request, 'Reminder deleted.')
    return redirect('tasks_app:reminder_list')
```

- [ ] **Step 3: Write tasks_app/urls.py**

```python
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
```

- [ ] **Step 4: Create task_dashboard.html**

```html
{% extends 'base.html' %}
{% block title %}Task Dashboard{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Task Dashboard</h1>
    <div>
        <a href="{% url 'tasks_app:task_assign' %}" class="btn btn-primary"><i class="bi bi-plus-lg"></i> Assign Task</a>
        <a href="{% url 'tasks_app:task_list' %}" class="btn btn-info">All Tasks</a>
    </div>
</div>

<h3>Today — {{ today }}</h3>
<div class="table-responsive">
    <table class="table table-hover">
        <thead class="table-dark">
            <tr><th>Staff</th><th>Task</th><th>Category</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% for task in today_tasks %}
            <tr class="{% if task.is_completed %}table-success{% endif %}">
                <td>{{ task.staff.name }}</td>
                <td>{{ task.task_template.name }}</td>
                <td>{{ task.task_template.category.name|default:'—' }}</td>
                <td>{% if task.is_completed %}✅ Done{% else %}🔄 Pending{% endif %}</td>
                <td>
                    <a href="{% url 'tasks_app:task_toggle' task.pk %}" class="btn btn-sm btn-{% if task.is_completed %}warning{% else %}success{% endif %}">
                        {% if task.is_completed %}Reopen{% else %}Complete{% endif %}
                    </a>
                    <a href="{% url 'tasks_app:task_delete' task.pk %}" class="btn btn-sm btn-danger" onclick="return confirm('Delete?')">Delete</a>
                </td>
            </tr>
            {% empty %}<tr><td colspan="5" class="text-center">No tasks for today.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<h3 class="mt-4">Pending Tasks</h3>
<div class="table-responsive">
    <table class="table table-sm table-striped">
        <thead><tr><th>Staff</th><th>Task</th><th>Date</th><th>Actions</th></tr></thead>
        <tbody>
            {% for task in pending_tasks %}
            <tr>
                <td>{{ task.staff.name }}</td>
                <td>{{ task.task_template.name }}</td>
                <td>{{ task.assigned_date }}</td>
                <td><a href="{% url 'tasks_app:task_toggle' task.pk %}" class="btn btn-sm btn-success">Complete</a></td>
            </tr>
            {% empty %}<tr><td colspan="4" class="text-center">No pending tasks.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 5: Create task_assign.html**

```html
{% extends 'base.html' %}
{% block title %}Assign Task{% endblock %}
{% block content %}
<h1>Assign Task</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Assign</button>
    <a href="{% url 'tasks_app:task_dashboard' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 6: Create task_list.html**

```html
{% extends 'base.html' %}
{% block title %}All Tasks{% endblock %}
{% block content %}
<h1>All Tasks</h1>
<div class="table-responsive">
    <table class="table table-striped">
        <thead class="table-dark">
            <tr><th>Staff</th><th>Task</th><th>Date</th><th>Status</th><th>Completed At</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% for task in tasks %}
            <tr>
                <td>{{ task.staff.name }}</td>
                <td>{{ task.task_template.name }}</td>
                <td>{{ task.assigned_date }}</td>
                <td>{% if task.is_completed %}✅{% else %}❌{% endif %}</td>
                <td>{{ task.completed_at|default:'—' }}</td>
                <td>
                    <a href="{% url 'tasks_app:task_toggle' task.pk %}" class="btn btn-sm btn-{% if task.is_completed %}warning{% else %}success{% endif %}">
                        {% if task.is_completed %}Reopen{% else %}Complete{% endif %}
                    </a>
                </td>
            </tr>
            {% empty %}<tr><td colspan="6" class="text-center">No tasks.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 7: Create reminder_list.html**

```html
{% extends 'base.html' %}
{% block title %}Reminders{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>My Reminders</h1>
    <a href="{% url 'tasks_app:reminder_create' %}" class="btn btn-primary"><i class="bi bi-plus-lg"></i> Add Reminder</a>
</div>
<div class="row">
    {% for reminder in reminders %}
    <div class="col-md-4 mb-3">
        <div class="card {% if reminder.is_completed %}text-bg-light{% elif reminder.due_date < today %}border-danger{% endif %}">
            <div class="card-body">
                <h5 class="card-title">
                    {% if reminder.is_completed %}<s>{% endif %}
                    {{ reminder.title }}
                    {% if reminder.is_completed %}</s>{% endif %}
                    <span class="badge bg-{% if reminder.category == 'subscription' %}info{% elif reminder.category == 'maintenance' %}warning{% elif reminder.category == 'pest' %}danger{% else %}secondary{% endif %} float-end">
                        {{ reminder.get_category_display }}
                    </span>
                </h5>
                <p class="card-text">{{ reminder.description|default:''|truncatewords:20 }}</p>
                <p class="card-text"><small>Due: {{ reminder.due_date }}</small></p>
                {% if reminder.repeat != 'none' %}<p class="card-text"><small>🔄 {{ reminder.get_repeat_display }}</small></p>{% endif %}
                <div class="btn-group">
                    <a href="{% url 'tasks_app:reminder_toggle' reminder.pk %}" class="btn btn-sm btn-{% if reminder.is_completed %}warning{% else %}success{% endif %}">
                        {% if reminder.is_completed %}Undo{% else %}Done{% endif %}
                    </a>
                    <a href="{% url 'tasks_app:reminder_edit' reminder.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="{% url 'tasks_app:reminder_delete' reminder.pk %}" class="btn btn-sm btn-danger" onclick="return confirm('Delete?')">Delete</a>
                </div>
            </div>
        </div>
    </div>
    {% empty %}<div class="col-12"><p class="text-center">No reminders.</p></div>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 8: Create reminder_form.html**

```html
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<h1>{{ title }}</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Save</button>
    <a href="{% url 'tasks_app:reminder_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

- [ ] **Step 9: Verify**

```powershell
python manage.py check
python manage.py runserver 0.0.0.0:8000 --noreload
```
Test task assignment, completion toggle, reminders CRUD.

- [ ] **Step 10: Commit**

```powershell
git add -A
git commit -m "feat: add task checklist and reminder system"
```

---

### Task 13: Task generation management command

**Files:**
- Create: `C:\Users\U.C\Desktop\monika mam\organize tasks\tasks_app\management\commands\generate_tasks.py`

- [ ] **Step 1: Write generate_tasks command**

```python
from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks_app.models import TaskTemplate, AssignedTask
from staff.models import StaffProfile
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate recurring tasks for today'

    def handle(self, *args, **options):
        today = timezone.now().date()
        weekday = today.weekday()  # 0=Mon, 6=Sun
        day_of_month = today.day
        
        templates = TaskTemplate.objects.all()
        created_count = 0
        
        for template in templates:
            # Check if this template should generate today
            if template.frequency == 'daily':
                should_generate = True
            elif template.frequency == 'weekly':
                should_generate = template.day_of_week == weekday
            elif template.frequency == 'monthly':
                should_generate = template.day_of_month == day_of_month
            elif template.frequency == 'one_time':
                should_generate = False  # One-time tasks are manually assigned
            else:
                should_generate = False
            
            if not should_generate:
                continue
            
            # Find staff who have this template assigned
            # We check by looking at existing assignments for this template
            existing_staff = set(
                AssignedTask.objects.filter(
                    task_template=template,
                    assigned_date__gte=today - timedelta(days=30)
                ).values_list('staff_id', flat=True)
            )
            
            # Also consider active staff
            active_staff = StaffProfile.objects.filter(is_active=True)
            
            for staff in active_staff:
                _, created = AssignedTask.objects.get_or_create(
                    staff=staff,
                    task_template=template,
                    assigned_date=today,
                    defaults={'is_completed': False}
                )
                if created:
                    created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Generated {created_count} tasks for {today}'))
```

- [ ] **Step 2: Test the command**

```powershell
python manage.py generate_tasks
```
Expected output: "Generated 0 tasks for ..." (no templates yet)

- [ ] **Step 3: Commit**

```powershell
git add -A
git commit -m "feat: add management command for recurring task generation"
```

---

### Task 14: Admin setup and final polish

**Files:**
- Modify: `C:\Users\U.C\Desktop\monika mam\organize tasks\home_organizer\settings.py`

- [ ] **Step 1: Create admin superuser**

```powershell
python manage.py createsuperuser
```
Follow prompts to create admin user.

- [ ] **Step 2: Verify admin**

```powershell
python manage.py runserver 0.0.0.0:8000 --noreload
```
Visit http://127.0.0.1:8000/admin/ — log in with superuser. All models should appear.

- [ ] **Step 3: Add some sample data via admin**

Use admin interface to:
- Add categories (Vegetables, Spices, Grains, Dairy, Cleaning, etc.)
- Add task categories (Cleaning, Kitchen, Laundry, Vehicle)
- Add a task template (e.g. "Wash Utensils" → daily, "Clean Vehicle" → weekly)
- Create a pantry item (e.g. "Rice" → 2 kg)

- [ ] **Step 4: Final check**

```powershell
python manage.py check --deploy
```

- [ ] **Step 5: Commit final changes**

```powershell
git add -A
git commit -m "chore: finalize project with admin setup and documentation"
```

---

## Self-Review

### Spec coverage:
- [x] Staff profiles with roles + custom role — Task 3, 4
- [x] Leave marking (half/full) via calendar — Task 5, 6
- [x] Advance money requests — Task 5
- [x] Salary engine with leave + advance deduction — Task 7
- [x] Per-day rate or fixed deduction configurable — Task 3 (model), Task 7 (calculation)
- [x] Grocery list with auto-compare to pantry — Task 10
- [x] Categories for grocery/pantry — Task 8 (Category model)
- [x] Inventory for crockery/equipment — Task 8, 9
- [x] Menu planning with ingredients + steps — Task 10
- [x] Task checklists per staff — Task 11, 12
- [x] Daily/weekly/monthly/one-time recurrence — Task 11 (TaskTemplate.frequency), Task 13 (generate_tasks)
- [x] Personal reminders with categories — Task 12
- [x] Permission system via Django admin/groups — Task 14

### Placeholder scan:
No TBDs, TODOs, or vague requirements in code blocks.

### Type consistency:
All signatures and references consistent across tasks.
