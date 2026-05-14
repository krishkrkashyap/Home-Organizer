from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import StaffProfile
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
    return render(request, 'staff/staff_detail.html', {
        'staff': staff,
        'leaves': [],
        'advances': [],
        'salary_records': [],
    })

def staff_delete(request, pk):
    staff = get_object_or_404(StaffProfile, pk=pk)
    staff.delete()
    messages.success(request, 'Staff deleted.')
    return redirect('staff:list')
