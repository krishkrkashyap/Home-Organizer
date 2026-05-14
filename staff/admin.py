from django.contrib import admin
from .models import StaffProfile, LeaveRecord, AdvanceRequest

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'salary_amount', 'salary_date', 'advance_balance', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['name', 'phone']

@admin.register(LeaveRecord)
class LeaveRecordAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date', 'leave_type', 'note']
    list_filter = ['leave_type']

@admin.register(AdvanceRequest)
class AdvanceRequestAdmin(admin.ModelAdmin):
    list_display = ['staff', 'amount', 'created_at', 'is_settled']
    list_filter = ['is_settled']
