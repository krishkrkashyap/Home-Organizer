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
