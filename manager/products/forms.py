from django import forms
from .models import MaterialsK, Material


class MaterialForm(forms.ModelForm):
    """Форма для добавления/редактирования материала"""
    
    class Meta:
        model = MaterialsK
        fields = [
            'material_names',
            'type_of_material',
            'photo',
            'price',
            'quantity_in_stock',
            'min_quantity',
            'package_quantity',
            'units',
        ]
        widgets = {
            'material_names': forms.Select(attrs={'class': 'form-control'}),
            'type_of_material': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'min_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'package_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'units': forms.Select(attrs={'class': 'form-control'}),
        }