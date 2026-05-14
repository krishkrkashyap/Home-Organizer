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
