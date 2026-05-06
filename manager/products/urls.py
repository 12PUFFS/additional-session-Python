from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='product_list'),
    path('create/', views.material_create, name='material_create'),
    path('update/<int:pk>/', views.material_update, name='material_update'),
    path('delete/<int:pk>/', views.material_delete, name='material_delete'),
    path('update-min-quantity/', views.update_min_quantity, name='update_min_quantity'),
]