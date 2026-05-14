# Staff Auth & Role-Based Access Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or inline execution.

**Goal:** Add staff-wise login with manual credentials, role-based dashboards, and tabbed staff creation form.

**Architecture:** Tabbed staff form creates User+StaffProfile atomically; custom login redirect routes users by role; single dashboard view renders role-specific sections.

**Tech Stack:** Django 4.2, SQLite, FullCalendar, Bootstrap Icons

---

### Task 1: Remove auto-create signal, update StaffProfile model

**Files:**
- Modify: `staff/signals.py` — comment out or remove signal
- Modify: `staff/apps.py` — remove `import staff.signals` from `ready()`
- Verify: `staff/models.py` — ensure `user` OneToOneField exists (it does)

- [ ] **Disable auto_create_user signal**

`staff/signals.py`:
```python
# Disabled — user creation handled by StaffCreateForm
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import StaffProfile
# User = get_user_model()
#
# @receiver(post_save, sender=StaffProfile)
# def auto_create_user(sender, instance, created, **kwargs):
#     if created and not instance.user:
#         ...
```

- [ ] **Update apps.py to remove signal import**

`staff/apps.py`:
```python
from django.apps import AppConfig

class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff'
    # Signal removed — user creation handled by form
```

- [ ] **Verify with check**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

---

### Task 2: Create StaffCreateForm with account fields

**Files:**
- Modify: `staff/forms.py`

- [ ] **Add StaffCreateForm with username/password fields**

`staff/forms.py` — add after existing forms:
```python
from django import forms
from django.contrib.auth.models import User
from .models import StaffProfile, LeaveRecord, AdvanceRequest

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'
        widgets = {'salary_date': forms.NumberInput(attrs={'min': 1, 'max': 31})}

class StaffCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm Password')

    class Meta:
        model = StaffProfile
        fields = ['name', 'phone', 'email', 'role', 'custom_role', 'photo',
                  'is_active', 'salary_amount', 'salary_date', 'deduction_type', 'deduction_value']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        staff = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        staff.user = user
        if commit:
            staff.save()
        return staff

class StaffEditForm(StaffProfileForm):
    """For editing — no account fields, show username as read-only."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['display_username'] = forms.CharField(
                initial=self.instance.user.username,
                disabled=True,
                required=False,
                label='Username'
            )
            # Put it at top of form
            self.fields.move_to_end('display_username', last=False)
```

- [ ] **Verify with check**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

---

### Task 3: Update staff views — create, edit, dashboard, tasks

**Files:**
- Modify: `staff/views.py`
- Modify: `staff/urls.py`

- [ ] **Update staff_create and staff_edit views**

`staff/views.py` changes:

```python
from .forms import StaffProfileForm, StaffCreateForm, StaffEditForm, LeaveForm, AdvanceForm

@login_required
def staff_create(request):
    if request.method == 'POST':
        form = StaffCreateForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f'Staff {staff.name} created. Username: {form.cleaned_data["username"]}')
            return redirect('staff:list')
    else:
        form = StaffCreateForm()
    return render(request, 'staff/staff_form.html', {'form': form, 'title': 'Add Staff', 'is_create': True})

@login_required
def staff_edit(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        form = StaffEditForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff profile updated.')
            return redirect('staff:detail', pk=staff.pk)
    else:
        form = StaffEditForm(instance=staff)
    return render(request, 'staff/staff_form.html', {'form': form, 'title': 'Edit Staff', 'is_create': False})
```

- [ ] **Add my_dashboard view**

`staff/views.py` — add after my_salary:
```python
from kitchen.models import MenuPlan, InventoryItem, PantryItem, GroceryList
from tasks_app.models import AssignedTask

@login_required
def my_dashboard(request):
    try:
        staff = request.user.staff_profile
    except StaffProfile.DoesNotExist:
        messages.error(request, 'No staff profile linked.')
        return redirect('dashboard')

    today = timezone.now().date()
    role = staff.role
    context = {
        'staff': staff,
        'today_tasks': AssignedTask.objects.filter(staff=staff, assigned_date=today, is_completed=False),
        'all_tasks': AssignedTask.objects.filter(staff=staff).order_by('-assigned_date')[:10],
        'recent_salary': SalaryRecord.objects.filter(staff=staff).order_by('-year', '-month').first(),
    }

    if role == 'cook':
        context['today_menus'] = MenuPlan.objects.filter(date=today)
        context['inventory_items'] = InventoryItem.objects.all()[:5]
    elif role == 'marketer':
        context['recent_grocery'] = GroceryList.objects.all().order_by('-created_at')[:3]
        context['low_pantry'] = [p for p in PantryItem.objects.all() if p.is_low()]

    return render(request, 'staff/my_dashboard.html', context)


@login_required
def my_tasks(request):
    try:
        staff = request.user.staff_profile
    except StaffProfile.DoesNotExist:
        messages.error(request, 'No staff profile linked.')
        return redirect('dashboard')

    tasks = AssignedTask.objects.filter(staff=staff).select_related('task_template').order_by('-assigned_date')
    return render(request, 'staff/my_tasks.html', {'tasks': tasks, 'staff': staff})
```

- [ ] **Update staff/urls.py**

```python
urlpatterns = [
    # ... existing paths ...
    # Staff self-service
    path('my/profile/', views.my_profile, name='my_profile'),
    path('my/salary/', views.my_salary, name='my_salary'),
    path('my/dashboard/', views.my_dashboard, name='my_dashboard'),
    path('my/tasks/', views.my_tasks, name='my_tasks'),
]
```

- [ ] **Verify with check**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

---

### Task 4: Custom login redirect view

**Files:**
- Modify: `home_organizer/views.py`
- Modify: `home_organizer/urls.py`
- Modify: `home_organizer/settings.py`

- [ ] **Add redirect_on_login view**

`home_organizer/views.py` — add alongside existing dashboard view:

```python
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def redirect_on_login(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    try:
        staff = request.user.staff_profile
        role = staff.role
        if role == 'cook':
            return redirect('staff:my_dashboard')
        elif role == 'marketer':
            return redirect('staff:my_dashboard')
        else:
            return redirect('staff:my_dashboard')
    except Exception:
        return redirect('dashboard')
```

- [ ] **Update urls.py**

`home_organizer/urls.py`:
```python
from home_organizer.views import dashboard, redirect_on_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard'),
    # ... rest
]
```

No change to urlpatterns — `LOGIN_REDIRECT_URL` in settings points to the view name.

Actually simpler: update LOGIN_REDIRECT_URL in settings to point to the view function directly.

Django's `LOGIN_REDIRECT_URL` can be a URL name. Let me add a dedicated URL for it:

`home_organizer/urls.py`:
```python
from home_organizer.views import dashboard, redirect_on_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard'),
    path('redirect-on-login/', redirect_on_login, name='redirect_on_login'),
    # ...
]
```

- [ ] **Update settings.py**

`home_organizer/settings.py`:
```python
LOGIN_REDIRECT_URL = 'redirect_on_login'
LOGOUT_REDIRECT_URL = 'login'
```

- [ ] **Verify with check**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

---

### Task 5: Redesign staff_form.html as tabbed form

**Files:**
- Modify: `staff/templates/staff/staff_form.html`
- Modify: `static/css/style.css`

- [ ] **Rewrite staff_form.html with tabs**

`staff/templates/staff/staff_form.html`:

```django
{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="content-area">
  <div class="page-header">
    <h1>{{ title }}</h1>
  </div>
  <div class="card">
    <div class="card-body">
      <form method="post" enctype="multipart/form-data">
        {% csrf_token %}

        {% if form.non_field_errors %}
        <div class="alert alert-danger">{{ form.non_field_errors }}</div>
        {% endif %}

        <!-- Tabs -->
        <div class="form-tabs">
          <button type="button" class="form-tab active" data-tab="profile">Profile</button>
          {% if is_create %}
          <button type="button" class="form-tab" data-tab="account">Account</button>
          {% endif %}
          <button type="button" class="form-tab" data-tab="salary">Salary</button>
        </div>

        <!-- Tab: Profile -->
        <div class="form-tab-content active" id="tab-profile">
          <div class="form-grid">
            <div class="form-group">
              <label>Name</label>
              {{ form.name }}
              {% if form.name.errors %}<div class="field-error">{{ form.name.errors }}</div>{% endif %}
            </div>
            <div class="form-group">
              <label>Phone</label>
              {{ form.phone }}
            </div>
            <div class="form-group">
              <label>Email</label>
              {{ form.email }}
            </div>
            <div class="form-group">
              <label>Role</label>
              {{ form.role }}
            </div>
            <div class="form-group">
              <label>Custom Role (optional)</label>
              {{ form.custom_role }}
            </div>
            <div class="form-group">
              <label>Active</label>
              {{ form.is_active }}
            </div>
            <div class="form-group full-width">
              <label>Photo</label>
              {{ form.photo }}
              {% if form.instance.photo %}
              <div class="photo-preview"><img src="{{ form.instance.photo.url }}" alt="preview" style="max-height:120px"></div>
              {% endif %}
            </div>
          </div>
        </div>

        {% if is_create %}
        <!-- Tab: Account -->
        <div class="form-tab-content" id="tab-account">
          <div class="form-grid">
            <div class="form-group">
              <label>Username</label>
              {{ form.username }}
              {% if form.username.errors %}<div class="field-error">{{ form.username.errors }}</div>{% endif %}
            </div>
            <div class="form-group">
              <label>Password</label>
              {{ form.password }}
            </div>
            <div class="form-group">
              <label>Confirm Password</label>
              {{ form.confirm_password }}
              {% if form.confirm_password.errors %}<div class="field-error">{{ form.confirm_password.errors }}</div>{% endif %}
            </div>
          </div>
        </div>
        {% endif %}

        <!-- Tab: Salary -->
        <div class="form-tab-content" id="tab-salary">
          <div class="form-grid">
            <div class="form-group">
              <label>Salary Amount (₹)</label>
              {{ form.salary_amount }}
            </div>
            <div class="form-group">
              <label>Salary Date (1-31)</label>
              {{ form.salary_date }}
            </div>
            <div class="form-group">
              <label>Deduction Type</label>
              {{ form.deduction_type }}
            </div>
            <div class="form-group" id="deduction-value-group">
              <label>Deduction Value (for fixed amount)</label>
              {{ form.deduction_value }}
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary">
            <i class="bi bi-check-lg"></i> {% if is_create %}Create Staff{% else %}Save Changes{% endif %}
          </button>
          <a href="{% url 'staff:list' %}" class="btn btn-outline">Cancel</a>
        </div>
      </form>
    </div>
  </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
  // Tab switching
  document.querySelectorAll('.form-tab').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.form-tab').forEach(function(t) { t.classList.remove('active'); });
      document.querySelectorAll('.form-tab-content').forEach(function(t) { t.classList.remove('active'); });
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
    });
  });
  // Toggle deduction value visibility
  var deductionType = document.querySelector('[name=deduction_type]');
  var deductionGroup = document.getElementById('deduction-value-group');
  if (deductionType && deductionGroup) {
    function toggleDeduction() {
      deductionGroup.style.display = deductionType.value === 'fixed_amount' ? 'block' : 'none';
    }
    deductionType.addEventListener('change', toggleDeduction);
    toggleDeduction();
  }
</script>
{% endblock %}
```

- [ ] **Add tab styles to CSS**

Append to `static/css/style.css`:

```css
/* ====== Form Tabs ====== */
.form-tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid var(--cream-dark);
  margin-bottom: 1.5rem;
}
.form-tab {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  font-family: 'Nunito', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-muted);
  cursor: pointer;
  position: relative;
  transition: color 0.2s;
}
.form-tab:hover { color: var(--primary); }
.form-tab.active {
  color: var(--primary);
}
.form-tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary);
}
.form-tab-content { display: none; }
.form-tab-content.active { display: block; }

/* Form grid */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}
.form-grid .full-width { grid-column: 1 / -1; }
.form-group label {
  display: block;
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text);
  margin-bottom: 0.35rem;
}
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1.5px solid var(--cream-dark);
  border-radius: 8px;
  font-family: 'Nunito', sans-serif;
  font-size: 0.95rem;
  background: white;
  transition: border-color 0.2s;
}
.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(196, 149, 106, 0.15);
}
.form-actions {
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--cream-dark);
  display: flex;
  gap: 0.75rem;
}
.field-error {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}
.photo-preview {
  margin-top: 0.5rem;
}
.photo-preview img {
  border-radius: 8px;
  border: 2px solid var(--cream-dark);
}
```

- [ ] **Verify render**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

---

### Task 6: Create my_dashboard.html template

**Files:**
- Create: `staff/templates/staff/my_dashboard.html`

- [ ] **Write my_dashboard.html**

`staff/templates/staff/my_dashboard.html`:

```django
{% extends 'base.html' %}
{% load static %}
{% block title %}My Dashboard{% endblock %}
{% block page_title %}My Dashboard{% endblock %}
{% block content %}
<div class="content-area">
  <!-- Profile Card -->
  <div class="staff-welcome">
    <div class="welcome-avatar">
      {% if staff.photo %}
      <img src="{{ staff.photo.url }}" alt="{{ staff.name }}">
      {% else %}
      <span>{{ staff.name|make_list|first|upper }}</span>
      {% endif %}
    </div>
    <div class="welcome-info">
      <h2>{{ staff.name }}</h2>
      <span class="role-badge">{{ staff.custom_role|default:staff.get_role_display }}</span>
    </div>
  </div>

  <!-- Stats -->
  <div class="stats-grid" style="margin-top:1.5rem;">
    <div class="stat-card primary">
      <span class="stat-icon">📋</span>
      <div class="stat-label">Today's Tasks</div>
      <div class="stat-value">{{ today_tasks|length }}</div>
    </div>
    <div class="stat-card success">
      <span class="stat-icon">💰</span>
      <div class="stat-label">Latest Salary</div>
      <div class="stat-value">{% if recent_salary %}₹{{ recent_salary.net_salary }}{% else %}—{% endif %}</div>
    </div>
    {% if staff.role == 'cook' and today_menus %}
    <div class="stat-card warning">
      <span class="stat-icon">🍳</span>
      <div class="stat-label">Today's Menus</div>
      <div class="stat-value">{{ today_menus|length }}</div>
    </div>
    {% endif %}
    {% if staff.role == 'marketer' and low_pantry %}
    <div class="stat-card danger">
      <span class="stat-icon">⚠️</span>
      <div class="stat-label">Low Stock Items</div>
      <div class="stat-value">{{ low_pantry|length }}</div>
    </div>
    {% endif %}
  </div>

  <!-- Today's Tasks -->
  <div class="card" style="margin-top:1.5rem;">
    <div class="card-header">
      <span>Today's Tasks — {{ today|date:"l, d M" }}</span>
      <a href="{% url 'staff:my_tasks' %}" class="btn btn-sm btn-outline-primary">View All</a>
    </div>
    <div class="card-body">
      {% if today_tasks %}
      <div class="task-list">
        {% for task in today_tasks %}
        <div class="task-item">
          <span class="task-name">{{ task.task_template.name }}</span>
          <span class="task-badge {{ task.task_template.category.name|lower|default:'other' }}">{{ task.task_template.category|default:'General' }}</span>
        </div>
        {% endfor %}
      </div>
      {% else %}
      <p class="text-muted">No tasks assigned for today.</p>
      {% endif %}
    </div>
  </div>

  <!-- Role-Specific Sections -->
  {% if staff.role == 'cook' %}
  <div class="card" style="margin-top:1rem;">
    <div class="card-header"><span>Today's Menu Plans</span></div>
    <div class="card-body">
      {% if today_menus %}
      {% for menu in today_menus %}
      <div class="menu-mini">
        <span class="meal-badge">{{ menu.get_meal_type_display }}</span>
        <strong>{{ menu.dish_name }}</strong>
        {% if menu.is_completed %}<span class="badge badge-success">Done</span>{% endif %}
      </div>
      {% endfor %}
      {% else %}
      <p class="text-muted">No menus planned for today.</p>
      {% endif %}
    </div>
  </div>
  {% endif %}

  {% if staff.role == 'marketer' %}
  <div class="card" style="margin-top:1rem;">
    <div class="card-header"><span>Low Pantry Items</span></div>
    <div class="card-body">
      {% if low_pantry %}
      <ul>
        {% for item in low_pantry %}
        <li>{{ item.name }} — {{ item.quantity }} {{ item.unit }} (min: {{ item.min_quantity }})</li>
        {% endfor %}
      </ul>
      {% else %}
      <p class="text-muted">All items well stocked.</p>
      {% endif %}
    </div>
  </div>
  {% endif %}

  <!-- Quick Actions -->
  <div class="card" style="margin-top:1rem;">
    <div class="card-header"><span>Quick Links</span></div>
    <div class="card-body">
      <div class="d-flex gap-2" style="flex-wrap:wrap;">
        <a href="{% url 'staff:my_profile' %}" class="btn btn-outline-primary">My Profile</a>
        <a href="{% url 'staff:my_salary' %}" class="btn btn-outline-success">My Salary</a>
        <a href="{% url 'staff:my_tasks' %}" class="btn btn-outline-info">My Tasks</a>
        {% if staff.role == 'cook' %}
        <a href="{% url 'kitchen:menu_list' %}" class="btn btn-outline-warning">Menu Plans</a>
        <a href="{% url 'kitchen:inventory_list' %}" class="btn btn-outline-secondary">Inventory</a>
        {% endif %}
        {% if staff.role == 'marketer' %}
        <a href="{% url 'kitchen:grocery_create' %}" class="btn btn-outline-success">New Grocery</a>
        <a href="{% url 'kitchen:pantry_list' %}" class="btn btn-outline-primary">Pantry</a>
        {% endif %}
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

---

### Task 7: Create my_tasks.html template

**Files:**
- Create: `staff/templates/staff/my_tasks.html`

- [ ] **Write my_tasks.html**

`staff/templates/staff/my_tasks.html`:

```django
{% extends 'base.html' %}
{% block title %}My Tasks{% endblock %}
{% block page_title %}My Tasks{% endblock %}
{% block content %}
<div class="content-area">
  <div class="page-header">
    <h1>My Tasks</h1>
  </div>
  <div class="card">
    <div class="card-body">
      {% if tasks %}
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Task</th>
              <th>Category</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {% for task in tasks %}
            <tr>
              <td>{{ task.task_template.name }}</td>
              <td>{{ task.task_template.category|default:'—' }}</td>
              <td>{{ task.assigned_date }}</td>
              <td>
                {% if task.is_completed %}
                <span class="badge badge-success">Done</span>
                {% else %}
                <span class="badge badge-warning">Pending</span>
                {% endif %}
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      {% else %}
      <p class="text-muted">No tasks assigned yet.</p>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}
```

---

### Task 8: Update sidebar navigation by role

**Files:**
- Modify: `templates/base.html`

- [ ] **Implement role-based sidebar**

Replace the sidebar nav section in `templates/base.html` to show different links for superuser vs staff roles.

The superuser side stays as-is. For staff, conditionally show role-appropriate nav items using `request.user.staff_profile.role`:

```django
<!-- Sidebar nav — adapt by role -->
{% if request.user.is_superuser %}
  {# Current full sidebar #}
{% else %}
  {% with role=request.user.staff_profile.role %}
  <li><a href="{% url 'staff:my_dashboard' %}" class="nav-link"><i class="bi bi-speedometer2"></i><span>Dashboard</span></a></li>
  <li><a href="{% url 'staff:my_profile' %}" class="nav-link"><i class="bi bi-person"></i><span>My Profile</span></a></li>
  <li><a href="{% url 'staff:my_salary' %}" class="nav-link"><i class="bi bi-cash-coin"></i><span>My Salary</span></a></li>
  <li><a href="{% url 'staff:my_tasks' %}" class="nav-link"><i class="bi bi-list-check"></i><span>My Tasks</span></a></li>
  {% if role == 'cook' %}
  <li class="nav-section">Kitchen</li>
  <li><a href="{% url 'kitchen:menu_list' %}" class="nav-link"><i class="bi bi-book"></i><span>Menu Plans</span></a></li>
  <li><a href="{% url 'kitchen:inventory_list' %}" class="nav-link"><i class="bi bi-box-seam"></i><span>Inventory</span></a></li>
  {% endif %}
  {% if role == 'marketer' %}
  <li class="nav-section">Kitchen</li>
  <li><a href="{% url 'kitchen:grocery_list' %}" class="nav-link"><i class="bi bi-cart-check"></i><span>Grocery</span></a></li>
  <li><a href="{% url 'kitchen:pantry_list' %}" class="nav-link"><i class="bi bi-basket"></i><span>Pantry</span></a></li>
  {% endif %}
  {% endwith %}
{% endif %}
```

---

### Task 9: Add CSS for new components

**Files:**
- Modify: `static/css/style.css`

- [ ] **Add styles for staff-welcome, task-list, menu-mini, role-badge**

Append to `static/css/style.css`:

```css
/* ====== Staff Welcome Card ====== */
.staff-welcome {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  background: linear-gradient(135deg, var(--primary), #2a5a4e);
  padding: 1.5rem 2rem;
  border-radius: 12px;
  color: white;
}
.welcome-avatar {
  width: 64px; height: 64px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  flex-shrink: 0;
}
.welcome-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.welcome-info h2 {
  font-family: 'Prata', serif;
  margin: 0;
  font-size: 1.5rem;
}
.role-badge {
  background: rgba(255,255,255,0.2);
  padding: 0.2rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-block;
  margin-top: 0.25rem;
}

/* ====== Task List ====== */
.task-list { display: flex; flex-direction: column; gap: 0.5rem; }
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.75rem;
  background: var(--cream);
  border-radius: 8px;
}
.task-name { font-weight: 600; font-size: 0.95rem; }
.task-badge {
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  background: var(--cream-dark);
  color: var(--text-muted);
}

/* ====== Menu Mini ====== */
.menu-mini {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--cream-dark);
}
.menu-mini:last-child { border-bottom: none; }
.meal-badge {
  background: var(--accent);
  color: white;
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* ====== Stat Card Danger ====== */
.stat-card.danger { border-left-color: #dc3545; }
```

---

### Task 10: Final verification

**Files:**
- Run: checks and server test

- [ ] **Run full check**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Start server and test**

Run: `python manage.py runserver`
Expected: Server starts on port 8000. Login page renders at `/`. Staff creation page renders at `/staff/create/` with tabs.

- [ ] **Commit**

```bash
git add -A
git commit -m "feat: staff auth with manual credentials, role-based dashboards, tabbed form"
```
