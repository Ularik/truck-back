from ninja import Schema, ModelSchema, FilterSchema, File
from pydantic import ConfigDict
from ninja.files import UploadedFile
from .models import Truck, Units
from typing import Optional


class UnitsSchema(ModelSchema):
    class Meta:
        model =  Units
        fields = ("id", "title")


class TruckOutListSchema(ModelSchema):
    class Meta:
        model = Truck
        fields = '__all__'


class SparesOutSchema(Schema):
    id: int
    title: str
    description: str | None = None
    category_id: int | None = None
    truck: list[int]
    price: int
    count: int
    is_popular: bool
    images: list[str]


class SparesCreateUpdateSchema(Schema):
    title: str
    description: str
    price: int
    truck: list[int] | None = None
    category_id: int | None = None
    count: int
    is_popular: bool = False
    model_config = ConfigDict(extra='ignore')


class GeneralResponseSchema(Schema):
    count: int
    result: list[SparesOutSchema]


class SparesFilterSchema(FilterSchema):
    title: Optional[str] = None
    truck: Optional[str] = None


class UnitOutSchema(Schema):
    id: int
    title: str
    image: str | None = None