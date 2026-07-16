from django.db import models


class Truck(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    photo = models.ImageField(upload_to='truck')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Units(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='units', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа комплектующего'
        verbose_name_plural = 'Группы комплектующих'


class ImagesSpares(models.Model):
    spare = models.ForeignKey("Spares", on_delete=models.CASCADE, related_name='images', verbose_name='Запчасть')
    image = models.ImageField(upload_to='spares', verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение запчасти'
        verbose_name_plural = 'Изображения запчастей'


class Spares(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    truck = models.ManyToManyField(Truck, verbose_name='Техника', null=True, blank=True)
    category = models.ForeignKey(Units, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name='Цена')
    count = models.PositiveIntegerField(null=True, blank=True, verbose_name='Количество')
    is_popular = models.BooleanField(default=False, verbose_name='Популярность сейчас')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'

