from django.db import models


class MaterialType(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    type_name = models.CharField(max_length=255, verbose_name='название типа')

    def __str__(self):
        return self.type_name

    class Meta:
        managed = False
        db_table = 'material_type'
        verbose_name = 'тип материала'
        verbose_name_plural = 'категории материалов'


class Unit(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    unit_name = models.CharField(max_length=255, verbose_name='название единицы')

    def __str__(self):
        return self.unit_name

    class Meta:
        managed = False
        db_table = 'unit'
        verbose_name = 'единица измерения'
        verbose_name_plural = 'единицы измерения'


class Provider(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    provider_name = models.CharField(max_length=255, verbose_name='название поставщика')

    def __str__(self):
        return self.provider_name

    class Meta:
        managed = False
        db_table = 'provider'
        verbose_name = 'поставщик'
        verbose_name_plural = 'поставщики'


class Material(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    material_name = models.CharField(max_length=255, verbose_name='наименование материала')

    def __str__(self):
        return self.material_name

    class Meta:
        managed = False
        db_table = 'material'
        verbose_name_plural = 'материалы'


class MaterialsK(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    material_names = models.ForeignKey(
        Material, 
        models.DO_NOTHING, 
        db_column='material_names', 
        verbose_name='материал'
    )
    type_of_material = models.ForeignKey(
        MaterialType, 
        models.DO_NOTHING, 
        db_column='type_of_material', 
        verbose_name='тип материала'
    )
    photo = models.ImageField(
        upload_to='materials', 
        blank=True, 
        null=True,
        verbose_name='изображение'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='цена'
    )
    quantity_in_stock = models.IntegerField(
        verbose_name='количество на складе'
    )
    min_quantity = models.IntegerField(
        verbose_name='минимальное количество'
    )
    package_quantity = models.IntegerField(
        verbose_name='количество в упаковке'
    )
    units = models.ForeignKey(
        Unit, 
        models.DO_NOTHING, 
        db_column='units', 
        verbose_name='единица измерения'
    )

    def __str__(self):
        return f'{self.material_names}'

    class Meta:
        managed = False
        db_table = 'materials_k'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class MaterialSupplierLink(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    materials_name = models.ForeignKey(
        Material, 
        models.DO_NOTHING, 
        db_column='materials_name', 
        verbose_name='материал'
    )
    providers_name = models.ForeignKey(
        Provider, 
        models.DO_NOTHING, 
        db_column='providers_name', 
        verbose_name='поставщик'
    )

    def __str__(self):
        return f'{self.materials_name}'

    class Meta:
        managed = False
        db_table = 'materialsupplier'
        verbose_name = 'поставка материала'
        verbose_name_plural = 'поставки материалов'