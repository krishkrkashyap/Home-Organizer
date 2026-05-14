import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import PantryItem, InventoryItem, GroceryList, GroceryItem, Category, MenuPlan
from .forms import PantryItemForm, InventoryItemForm, GroceryListForm, GroceryItemForm, MenuPlanForm

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

# --- Grocery ---
def grocery_list(request):
    lists = GroceryList.objects.prefetch_related('items').all().order_by('-created_at')
    return render(request, 'kitchen/grocery_list.html', {'lists': lists})

def grocery_create(request):
    if request.method == 'POST':
        form = GroceryListForm(request.POST)
        if form.is_valid():
            grocery = form.save()
            items_data = request.POST.get('items_json', '[]')
            try:
                items = json.loads(items_data)
                for item_data in items:
                    pantry_qs = PantryItem.objects.filter(name__iexact=item_data['name'])
                    qty_at_home = float(pantry_qs.first().quantity) if pantry_qs.exists() else 0
                    GroceryItem.objects.create(
                        grocery_list=grocery,
                        name=item_data['name'],
                        quantity_needed=item_data['quantity'],
                        unit=item_data.get('unit', 'pieces'),
                        quantity_at_home=qty_at_home,
                    )
                messages.success(request, 'Grocery list created with auto-compare.')
            except (json.JSONDecodeError, KeyError) as e:
                messages.warning(request, f'List created but items had errors: {e}')
            return redirect('kitchen:grocery_detail', pk=grocery.pk)
    else:
        form = GroceryListForm()
    pantry_items = PantryItem.objects.all()
    pantry_dict = {item.name.lower(): float(item.quantity) for item in pantry_items}
    return render(request, 'kitchen/grocery_create.html', {
        'form': form,
        'categories': Category.objects.all(),
        'pantry_items': pantry_items,
        'pantry_dict': json.dumps(pantry_dict),
    })

def grocery_detail(request, pk):
    grocery = get_object_or_404(GroceryList.objects.prefetch_related('items__category'), pk=pk)
    return render(request, 'kitchen/grocery_detail.html', {'grocery': grocery})

def grocery_purchase_item(request, pk):
    item = get_object_or_404(GroceryItem, pk=pk)
    item.is_purchased = True
    item.save()
    pantry, _ = PantryItem.objects.get_or_create(name=item.name, defaults={'quantity': 0})
    pantry.quantity += item.quantity_to_buy
    pantry.save()
    return JsonResponse({'success': True})

def grocery_mark_purchased(request, pk):
    grocery = get_object_or_404(GroceryList, pk=pk)
    grocery.is_purchased = True
    from django.utils import timezone
    grocery.purchased_at = timezone.now()
    grocery.save()
    for item in grocery.items.filter(is_purchased=False):
        item.is_purchased = True
        item.save()
        pantry, _ = PantryItem.objects.get_or_create(name=item.name, defaults={'quantity': 0})
        pantry.quantity += item.quantity_to_buy
        pantry.save()
    messages.success(request, 'Grocery list marked as purchased. Pantry updated.')
    return redirect('kitchen:grocery_detail', pk=grocery.pk)

# --- Menu Plan ---
def menu_list(request):
    menus = MenuPlan.objects.select_related('cook').all().order_by('-date')
    return render(request, 'kitchen/menu_list.html', {'menus': menus})

def menu_create(request):
    if request.method == 'POST':
        form = MenuPlanForm(request.POST)
        if form.is_valid():
            menu = form.save()
            messages.success(request, f'Menu plan for {menu.dish_name} created.')
            return redirect('kitchen:menu_list')
    else:
        form = MenuPlanForm()
    return render(request, 'kitchen/menu_form.html', {'form': form, 'title': 'Create Menu Plan'})

def menu_edit(request, pk):
    menu = get_object_or_404(MenuPlan, pk=pk)
    if request.method == 'POST':
        form = MenuPlanForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu plan updated.')
            return redirect('kitchen:menu_list')
    else:
        form = MenuPlanForm(instance=menu)
    return render(request, 'kitchen/menu_form.html', {'form': form, 'title': 'Edit Menu Plan'})

def menu_toggle_step(request, pk, step_num):
    menu = get_object_or_404(MenuPlan, pk=pk)
    steps = menu.steps
    for step in steps:
        if step.get('step_number') == step_num:
            step['is_completed'] = not step.get('is_completed', False)
    menu.steps = steps
    menu.is_completed = all(s.get('is_completed', False) for s in steps)
    menu.save()
    return JsonResponse({'success': True, 'is_completed': menu.is_completed})
