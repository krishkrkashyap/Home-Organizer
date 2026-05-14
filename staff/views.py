from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import StaffProfile, LeaveRecord, AdvanceRequest, SalaryRecord
from .forms import StaffProfileForm, StaffCreateForm, StaffEditForm, LeaveForm, AdvanceForm

@login_required
def staff_list(request):
    staff_members = StaffProfile.objects.all()
    return render(request, 'staff/staff_list.html', {'staff_members': staff_members})

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

@login_required
def staff_detail(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    leaves = LeaveRecord.objects.filter(staff=staff).order_by('-date')
    advances = AdvanceRequest.objects.filter(staff=staff).order_by('-created_at')
    salary_records = SalaryRecord.objects.filter(staff=staff).order_by('-year', '-month')
    return render(request, 'staff/staff_detail.html', {
        'staff': staff,
        'leaves': leaves,
        'advances': advances,
        'salary_records': salary_records,
    })

@login_required
def staff_delete(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    user = staff.user
    name = staff.name
    staff.delete()
    if user:
        user.delete()
    messages.success(request, f'{name} deleted along with their user account.')
    return redirect('staff:list')

@login_required
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

@login_required
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

@login_required
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

@login_required
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
            leave_deduction = float(staff.deduction_value) * total_leaves
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

@login_required
def salary_list(request):
    records = SalaryRecord.objects.all().select_related('staff').order_by('-year', '-month')
    return render(request, 'staff/salary_list.html', {'records': records})


# --- Staff Self-Service (read-only) ---

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
        'today': today,
        'today_tasks': AssignedTask.objects.filter(staff=staff, assigned_date=today, is_completed=False),
        'all_tasks': AssignedTask.objects.filter(staff=staff).order_by('-assigned_date')[:10],
        'recent_salary': SalaryRecord.objects.filter(staff=staff).order_by('-year', '-month').first(),
    }

    if role == 'cook':
        from kitchen.models import MenuPlan, InventoryItem
        context['today_menus'] = MenuPlan.objects.filter(date=today)
        context['inventory_items'] = InventoryItem.objects.all()[:5]
    elif role == 'marketer':
        from kitchen.models import GroceryList, PantryItem
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

    tasks = AssignedTask.objects.filter(staff=staff).select_related('task_template__category').order_by('-assigned_date')
    return render(request, 'staff/my_tasks.html', {'tasks': tasks, 'staff': staff})

@login_required
def my_profile(request):
    """Staff user views own profile (read-only)."""
    try:
        staff = request.user.staff_profile
    except StaffProfile.DoesNotExist:
        messages.error(request, 'No staff profile linked to your account.')
        return redirect('dashboard')
    leaves = LeaveRecord.objects.filter(staff=staff).order_by('-date')
    advances = AdvanceRequest.objects.filter(staff=staff).order_by('-created_at')
    salary_records = SalaryRecord.objects.filter(staff=staff).order_by('-year', '-month')
    return render(request, 'staff/staff_detail.html', {
        'staff': staff,
        'leaves': leaves,
        'advances': advances,
        'salary_records': salary_records,
        'readonly': True,
    })


@login_required
def my_salary(request):
    """Staff user views own salary records (read-only)."""
    try:
        staff = request.user.staff_profile
    except StaffProfile.DoesNotExist:
        messages.error(request, 'No staff profile linked to your account.')
        return redirect('dashboard')
    records = SalaryRecord.objects.filter(staff=staff).order_by('-year', '-month')
    return render(request, 'staff/salary_list.html', {'records': records, 'readonly': True})
