from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PantryItem, InventoryItem
from .forms import PantryItemForm, InventoryItemForm

# --- Pantry ---
def pantry_list(request):
    items = PantryItem.objects.select_related('category').all()
    return render(request, 'kitchen/pantry_list.html', {'items': items})

def pantry_create(request):
    if request.method == 'POST':
        form = PantryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pantry item added.')
            return redirect('kitchen:pantry_list')
    else:
        form = PantryItemForm()
    return render(request, 'kitchen/pantry_form.html', {'form': form, 'title': 'Add Pantry Item'})

def pantry_edit(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    if request.method == 'POST':
        form = PantryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pantry item updated.')
            return redirect('kitchen:pantry_list')
    else:
        form = PantryItemForm(instance=item)
    return render(request, 'kitchen/pantry_form.html', {'form': form, 'title': 'Edit Pantry Item'})

def pantry_delete(request, pk):
    item = get_object_or_404(PantryItem, pk=pk)
    item.delete()
    messages.success(request, 'Pantry item deleted.')
    return redirect('kitchen:pantry_list')

# --- Inventory ---
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'kitchen/inventory_list.html', {'items': items})

def inventory_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item added.')
            return redirect('kitchen:inventory_list')
    else:
        form = InventoryItemForm()
    return render(request, 'kitchen/inventory_form.html', {'form': form, 'title': 'Add Inventory Item'})

def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated.')
            return redirect('kitchen:inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'kitchen/inventory_form.html', {'form': form, 'title': 'Edit Inventory Item'})

def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete()
    messages.success(request, 'Inventory item deleted.')
    return redirect('kitchen:inventory_list')
