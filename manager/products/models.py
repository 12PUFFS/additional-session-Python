# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, verbose_name='название')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, verbose_name='группа')
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING, verbose_name='разрешение')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, verbose_name='тип контента')
    codename = models.CharField(max_length=100, verbose_name='кодовое имя')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, verbose_name='пароль')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='последний вход')
    is_superuser = models.BooleanField(verbose_name='суперпользователь')
    username = models.CharField(unique=True, max_length=150, verbose_name='имя пользователя')
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    email = models.CharField(max_length=254, verbose_name='email')
    is_staff = models.BooleanField(verbose_name='персонал')
    is_active = models.BooleanField(verbose_name='активен')
    date_joined = models.DateTimeField(verbose_name='дата регистрации')

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, verbose_name='пользователь')
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, verbose_name='группа')

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, verbose_name='пользователь')
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING, verbose_name='разрешение')

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField(verbose_name='время действия')
    object_id = models.TextField(blank=True, null=True, verbose_name='ID объекта')
    object_repr = models.CharField(max_length=200, verbose_name='представление объекта')
    action_flag = models.SmallIntegerField(verbose_name='флаг действия')
    change_message = models.TextField(verbose_name='сообщение изменения')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True, verbose_name='тип контента')
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, verbose_name='пользователь')

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, verbose_name='метка приложения')
    model = models.CharField(max_length=100, verbose_name='модель')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    app = models.CharField(max_length=255, verbose_name='приложение')
    name = models.CharField(max_length=255, verbose_name='название')
    applied = models.DateTimeField(verbose_name='применено')

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, verbose_name='ключ сессии')
    session_data = models.TextField(verbose_name='данные сессии')
    expire_date = models.DateTimeField(verbose_name='истекает')

    class Meta:
        managed = False
        db_table = 'django_session'


class Material(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    material_name = models.CharField(max_length=255, verbose_name='тип материала')

    def __str__(self):
        return self.material_name

    class Meta:
        managed = False
        db_table = 'material'
        verbose_name_plural = 'материалы'


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


class MaterialsK(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    material_names = models.ForeignKey(Material, models.DO_NOTHING, db_column='material_names', verbose_name='материал')
    type_of_material = models.ForeignKey(MaterialType, models.DO_NOTHING, db_column='type_of_material', verbose_name='тип материала')
    photo = models.ImageField(upload_to ='materials', blank=True, null=True,verbose_name='изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity_in_stock = models.CharField(max_length=50, verbose_name='количество на складе')
    min_quantity = models.IntegerField(verbose_name='минимальное количество')
    package_quantity = models.IntegerField(verbose_name='количество в упаковке')
    units = models.ForeignKey('Unit', models.DO_NOTHING, db_column='units', verbose_name='единица измерения')

    def __str__(self):
        return f'{self.material_names}'

    class Meta:
        managed = False
        db_table = 'materials_k'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Materialsupplier(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    materials_name = models.ForeignKey(Material, models.DO_NOTHING, db_column='materials_name', verbose_name='материал')
    providers_name = models.ForeignKey('Provider', models.DO_NOTHING, db_column='providers_name', verbose_name='поставщик')

    def __str__(self):
        return f'{self.materials_name}'

    class Meta:
        managed = False
        db_table = 'materialsupplier'
        verbose_name = 'поставка материала'
        verbose_name_plural = 'поставки материалов'


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