from django.db import models
from django.utils.text import slugify
import os


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


class Spares(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    truck = models.ManyToManyField(Truck, verbose_name='Техника')
    category = models.ForeignKey(Units, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    photo = models.ImageField(upload_to='spares')
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

