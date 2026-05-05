from django.urls import path
from . import views 

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='product_list')
]
