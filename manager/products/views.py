from django.shortcuts import render
from .models import MaterialsK, Materialsupplier



def products_list(request):
    '''ТОВАРЫ'''

    products = MaterialsK.objects.all()
    supplier = Materialsupplier.objects.all()
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        search_query = request.GET.get('rearch', '').strip()
        if search_query:
            products = products.filter(
                Q(material_names_icontains = search_query ) |
                Q(type_of_material_icontains = search_query) |
                Q(units_icontains = search_query)
            ) 
    context = {'products': products, 'supplier':supplier, 'search_query': search_query}
    if request.headers.get('x-requested-with') == 'XMLHttRequest':
        return render(request, 'products/product_list-filtered.html', context)
    
    return render ( request,  'products/product_list.html',context )


