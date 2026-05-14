from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import StaffProfile, LeaveRecord, AdvanceRequest
from .forms import StaffProfileForm, LeaveForm, AdvanceForm

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
    salary_records = []  # Will be populated in Task 7
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
