from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import MaterialsK, MaterialType, MaterialSupplierLink, Provider, Material, Unit
from .forms import MaterialForm  # добавим форму
from django.db.models import Q


def products_list(request):
    '''ТОВАРЫ - список материалов с фильтрацией и поиском'''
    
    search_query = ''
    type_filter = ''
    sort_order = ''
    supplier_order = 'all'
    
    # Базовый queryset
    products = MaterialsK.objects.select_related(
        'material_names', 
        'type_of_material', 
        'units'
    ).all()
    
    # Получаем все связи для отображения поставщиков
    all_suppliers_links = MaterialSupplierLink.objects.select_related(
        'providers_name'
    ).all()

    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        # Получаем параметры из GET запроса
        search_query = request.GET.get('search', '').strip()
        type_filter = request.GET.get('type', '')
        sort_order = request.GET.get('sort', '')
        supplier_order = request.GET.get('supplier', 'all')

        # Фильтрация по ПОИСКУ
        if search_query:
            products = products.filter(
                Q(material_names__material_name__icontains=search_query)
            )

        # Фильтрация по ТИПУ МАТЕРИАЛА
        if type_filter and type_filter != 'all':
            products = products.filter(type_of_material_id=type_filter)

        # Фильтрация по ПОСТАВЩИКУ
        if supplier_order and supplier_order != 'all':
            try:
                provider_obj = Provider.objects.get(provider_name=supplier_order)
                material_ids = MaterialSupplierLink.objects.filter(
                    providers_name=provider_obj
                ).values_list('materials_name_id', flat=True)
                products = products.filter(material_names_id__in=material_ids)
            except Provider.DoesNotExist:
                products = products.none()

        # Сортировка - ИСПРАВЛЕНА
        if sort_order:
            if sort_order == 'name_asc':
                products = products.order_by('material_names__material_name')
            elif sort_order == 'name_desc':
                products = products.order_by('-material_names__material_name')
            elif sort_order == 'stock_asc':
                products = products.order_by('quantity_in_stock')
            elif sort_order == 'stock_desc':
                products = products.order_by('-quantity_in_stock')
            elif sort_order == 'price_asc':
                products = products.order_by('price')
            elif sort_order == 'price_desc':
                products = products.order_by('-price')
        
        # Формируем списки для фильтров
        types = MaterialType.objects.all()
        
        supplier_names = Provider.objects.filter(
            id__in=MaterialSupplierLink.objects.values_list(
                'providers_name', 
                flat=True
            ).distinct()
        ).values_list('provider_name', flat=True).distinct()
        
        suppliers_list = ['Все поставщики'] + list(supplier_names)

    else:
        types = MaterialType.objects.none()
        suppliers_list = []

    # Пагинация
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'page_obj': page_obj,
        'supplier': all_suppliers_links,
        'types': types,
        'suppliers': suppliers_list,
        'supplier_order': supplier_order,
        'search_query': search_query,
        'sort_order': sort_order,
        'current_type': type_filter,
        'total_count': paginator.count,
        'current_count': len(page_obj),
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'products/product_list-filtered.html', context)
    
    return render(request, 'products/product_list.html', context)


# ============ CRUD OPERATIONS ============

def material_create(request):
    """CREATE - Добавление нового материала"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            suppliers = request.POST.getlist('suppliers')
            for supplier_id in suppliers:
                MaterialSupplierLink.objects.create(
                    materials_name=material.material_names,
                    providers_name_id=supplier_id
                )
            return redirect('products:product_list')
    else:
        form = MaterialForm()
    
    providers = Provider.objects.all()
    
    # ✅ ИСПРАВЛЕНИЕ: всегда передаём пустой список, если нет текущих поставщиков
    current_suppliers = []  # Для создания нового материала текущих поставщиков нет
    
    return render(request, 'products/material_form.html', {
        'form': form,
        'providers': providers,
        'current_suppliers': current_suppliers,  # Гарантированно список
        'title': 'Добавить материал'
    })


def material_update(request, pk):
    """UPDATE - Редактирование материала"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('products:product_list')
    
    material = get_object_or_404(MaterialsK, id=pk)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            # Обновление поставщиков
            MaterialSupplierLink.objects.filter(materials_name=material.material_names).delete()
            suppliers = request.POST.getlist('suppliers')
            for supplier_id in suppliers:
                MaterialSupplierLink.objects.create(
                    materials_name=material.material_names,
                    providers_name_id=supplier_id
                )
            return redirect('products:product_list')
    else:
        form = MaterialForm(instance=material)
    
    providers = Provider.objects.all()
    current_suppliers = MaterialSupplierLink.objects.filter(
        materials_name=material.material_names
    ).values_list('providers_name_id', flat=True)
    
    return render(request, 'products/material_form.html', {
        'form': form,
        'providers': providers,
        'current_suppliers': list(current_suppliers),
        'title': 'Редактировать материал',
        'material': material
    })


def material_delete(request, pk):
    """DELETE - Удаление материала"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('products:product_list')
    
    material = get_object_or_404(MaterialsK, id=pk)
    
    if request.method == 'POST':
        # Проверяем, используется ли материал в производстве
        # (здесь должна быть проверка, но пока просто удаляем)
        material.delete()
        return redirect('products:product_list')
    
    return render(request, 'products/material_confirm_delete.html', {
        'material': material
    })


def update_min_quantity(request):
    """Bulk update минимального количества для выбранных материалов"""
    if request.method == 'POST' and (request.user.is_staff or request.user.is_superuser):
        material_ids = request.POST.getlist('material_ids')
        new_min_quantity = request.POST.get('min_quantity')
        
        if material_ids and new_min_quantity:
            MaterialsK.objects.filter(
                id__in=material_ids
            ).update(min_quantity=int(new_min_quantity))
    
    return redirect('products:product_list')