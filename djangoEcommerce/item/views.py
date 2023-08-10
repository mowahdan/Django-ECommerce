from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import NewItem, EditItem
from .models import Item

def items(request):
    items = Item.objects.filter(is_sold=False)
    
    return render(request, 'item/items.html', {
        'items': items,
    })

def details(request, item_id):
    item = get_object_or_404(Item, id = item_id)
    related_items= Item.objects.filter(category=item.category, is_sold = False).exclude(id=item_id)[0:3]
    
    return render(request, 'item/detail.html', {
                      'item': item,
                      'related_items': related_items,
                  })
  
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItem(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            return redirect('item:detail', item_id=item.id)
    else:
        form = NewItem()
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })
    
@login_required
def edit(request, item_id):
    item = get_object_or_404(Item, id = item_id, created_by = request.user)
    if request.method == 'POST':
        form = EditItem(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save()
            
            return redirect('item:detail', item_id=item.id)
    else:
        form = EditItem(instance=item)
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })
    
@login_required
def delete(request, item_id):
    item = get_object_or_404(Item, id = item_id, created_by = request.user)
    item.delete()
    
    return redirect('dashboard:index')