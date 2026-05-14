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
