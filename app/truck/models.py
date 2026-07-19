from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class Truck(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    photo = models.ImageField(upload_to='truck', null=True, blank=True)
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

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = ImagesSpares.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.image

        image_changed = is_new or (old_image and old_image != self.image)

        if self.image and image_changed:
            img = Image.open(self.image)
            img = img.convert("RGB")
            img.thumbnail((1200, 1200))

            buffer = BytesIO()
            img.save(buffer, format="WEBP", quality=80, optimize=True)

            filename = f"{uuid.uuid4().hex}.webp"
            self.image.save(filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

        # Удаляем старый файл ПОСЛЕ успешного сохранения нового
        if image_changed and old_image and old_image.name:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

@receiver(post_delete, sender=ImagesSpares)
def delete_image_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


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

