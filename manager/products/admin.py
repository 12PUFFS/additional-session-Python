from django.contrib import admin
from .models import Material, MaterialType, MaterialsK, MaterialSupplierLink, Provider, Unit

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_name')
    search_fields = ('material_name',)

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit_name')

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider_name')
    search_fields = ('provider_name',)

@admin.register(MaterialsK)
class MaterialsKAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_names', 'type_of_material', 'quantity_in_stock', 'min_quantity', 'price')
    list_filter = ('type_of_material',)
    search_fields = ('material_names__material_name',)

@admin.register(MaterialSupplierLink)
class MaterialSupplierLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'materials_name', 'providers_name')
    list_filter = ('providers_name',)