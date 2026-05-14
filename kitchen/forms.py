from django import forms
from .models import PantryItem, InventoryItem

class PantryItemForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = '__all__'

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
