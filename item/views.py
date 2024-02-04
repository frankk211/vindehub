from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item
from conversation.models import Conversation
from django.http import HttpResponseBadRequest

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    locatie = request.GET.get('locatie')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')  
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False).order_by('-created_at')
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    nr_conversatii = conversations.count()
    

    # Încărcați datele din fișier
    with open('localitati.json', 'r', encoding='utf-8') as file:
        localitati_data = json.load(file)

    select2_data = [{'text': loc['nume'], 'id': loc['nume']} for loc in localitati_data]

    # Filtrează obiectele în funcție de categorie și locație
    if category_id:
        items = items.filter(category_id=category_id)
    else:
        category_id=''

    if locatie:
        items = items.filter(locatie=locatie)
    else:
        locatie = ''

    # Verifică dacă price_min este un șir vid și setează la None în acest caz
    price_min = int(price_min) if price_min and price_min.isdigit() else None

    # Verifică dacă price_max este un șir vid și setează la None în acest caz
    price_max = int(price_max) if price_max and price_max.isdigit() else None

    
    if price_min is not None:
        items = items.filter(Q(price__gte=price_min))
    else:
        price_min=0
    
        

    if price_max is not None:
        items = items.filter(Q(price__lte=price_max))
    else:
        price_max=321423543543543

    if price_min and price_max:
        items = items.filter(price__range=(price_min, price_max))

    # Filtrează obiectele în funcție de căutare
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    items_per_page = 8  # Puteți ajusta acest număr la preferințele dvs.

    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page')
    try:
        items = paginator.get_page(page_number)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    

    return render(request, 'item/items.html', {
        'page': page_number,
        'select2_data': select2_data,
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': category_id,  # Convertește category_id într-un număr întreg
        'locatie': locatie,
        'price_min': price_min,
        'price_max': price_max,
        'nr_conversatii': nr_conversatii
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    if not request.session.get(f'item_{pk}_visited', False):
        # Incrementăm numărul de accesări
        item.access_count += 1
        item.save()

        # Setăm în sesiune că acest anunț a fost vizitat
        request.session[f'item_{pk}_visited'] = True


    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):

    # Încărcați datele din fișier
    with open('localitati.json', 'r', encoding='utf-8') as file:
        localitati_data = json.load(file)

    select2_data = [{'text': loc['nume'], 'id': loc['nume']} for loc in localitati_data]
    
    
    categories = Category.objects.all()
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)

            item.locatie = form.cleaned_data['locatie']
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'select2_data': select2_data,
        'form': form,
        'categories': categories,
        'title': 'Creare anunț nou',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Editare anunț',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')