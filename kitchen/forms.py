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
