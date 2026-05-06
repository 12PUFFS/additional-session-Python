from django.shortcuts import render
from .models import MaterialsK, Materialsupplier
from django.db.models import Q

def products_list(request):
    '''ТОВАРЫ'''

    search_query = ''

    products = MaterialsK.objects.all()
    supplier = Materialsupplier.objects.all()
    
    # Проверка прав доступа для поиска
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        search_query = request.GET.get('search', '').strip()
        if search_query:
            # ✅ Исправленные фильтры с переходом по ForeignKey
            products = products.filter(
                Q(material_names__material_name__icontains=search_query) |
                Q(type_of_material__type_name__icontains=search_query) |
                Q(units__unit_name__icontains=search_query) |
                Q(price__icontains=search_query) |  # Если нужно искать по цене
                Q(quantity_in_stock__icontains=search_query)  # Если нужно по количеству
            ) 
            
    context = {
        'products': products, 
        'supplier': supplier, 
        'search_query': search_query
    }
    
    # Если это AJAX запрос, возвращаем только часть страницы
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'products/product_list-filtered.html', context)
    
    # Иначе возвращаем полную страницу
    return render(request, 'products/product_list.html', context)