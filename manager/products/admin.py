from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Material, MaterialType, MaterialsK, Materialsupplier, Provider, Unit

admin.site.register(MaterialsK)
admin.site.register(Materialsupplier)
# admin.site.register(Material)
# admin.site.register(MaterialType)
# admin.site.register(Provider)
# admin.site.register(Unit)


admin.site.unregister(Group)


