from django.contrib import admin
from .models import Truck, Spares, Units, ImagesSpares
from django.utils.safestring import mark_safe  # Импортируем mark_safe


@admin.register(Units)
class UnitsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title',)


class ImagesSparesInline(admin.TabularInline):
    model = ImagesSpares
    extra = 3  # Количество пустых слотов для картинок по умолчанию
    max_num = 10  # Ограничение на максимальное количество фото (если нужно)
    fields = ('image', 'get_html_photo')
    # Обязательно указываем его в readonly_fields, иначе Django попытается сделать из него поле ввода
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, obj):
        if obj.image:
            # Превью с высотой 100 пикселей (ширина подстроится автоматически)
            return mark_safe(
                f'<img src="{obj.image.url}" height="100" style="border-radius: 5px; max-width: 200px; object-fit: cover;"/>')
        return "Нет изображения"

    # Красивое название колонки в админке
    get_html_photo.short_description = "Превью"

@admin.register(Spares)
class SparesAdmin(admin.ModelAdmin):
    list_display = ('get_main_photo', 'title', 'category', 'created_date')
    list_display_links = ('get_main_photo', 'title')
    inlines = [ImagesSparesInline]
    search_fields = ('title', 'is_popular')
    list_filter = ('truck', 'is_popular')
    filter_horizontal = ('truck',)

    def get_main_photo(self, obj):
        # Берем первую связанную картинку
        first_image = obj.images.first()
        if first_image and first_image.image:
            return mark_safe(f'<img src="{first_image.image.url}" height="60" style="border-radius: 4px;"/>')
        return "Нет фото"

    # Магия подключения стилей:
    class Media:
        css = {
            'all': ('admin/css/truck/truck_admin.css',)
        }

    get_main_photo.short_description = "Фото"