from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'salary_amount', 'salary_date', 'advance_balance', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['name', 'phone']
