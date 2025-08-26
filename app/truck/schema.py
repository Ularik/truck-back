from ninja import Schema, ModelSchema, FilterSchema
from .models import Truck, Spares
from typing import Optional


class TruckOutListSchema(ModelSchema):
    class Meta:
        model = Truck
        fields = '__all__'


class SparesOutListSchema(ModelSchema):
    class Meta:
        model = Spares
        fields = '__all__'


class SparesFilterSchema(FilterSchema):
    title: Optional[str] = None
    truck: Optional[str] = None
