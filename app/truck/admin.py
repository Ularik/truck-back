from django.contrib import admin
from .models import Truck, Spares, Units


@admin.register(Units)
class UnitsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title',)


@admin.register(Spares)
class SparesAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title', 'is_popular')
    list_filter = ('truck', 'is_popular')
    filter_horizontal = ('truck',)