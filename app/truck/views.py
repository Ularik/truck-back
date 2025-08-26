from ninja import Router
from .models import Truck, Spares
from .schema import TruckOutListSchema, SparesOutListSchema
from django.db.models import Q

router = Router()

@router.get('/get-trucks', response={200: list[TruckOutListSchema], 400: str})
def get_trucks(request):
    return Truck.objects.all()


@router.get('/get-spares', response={200: list[SparesOutListSchema], 400: str})
def get_spares(request, title: str = None, is_popular: bool = None, count: int = 10, offset: int = 0):
    if title:
        if is_popular is not None:
            return Spares.objects.filter(Q(category__title__icontains=title) | Q(title__icontains=title)
                                         & Q(is_popular=is_popular)).distinct()[offset:offset+count]
        return Spares.objects.filter(Q(category__title__icontains=title) | Q(title__icontains=title)).distinct()[offset:offset+count]

    if is_popular is not None:
        return Spares.objects.filter(is_popular=is_popular)[offset:offset + count]
    return Spares.objects.all()[offset:offset+count]


@router.get('/get-spares-count', response=int)
def get_spares_count(request, title: str = None, is_popular: bool = None):
    if title:
        if is_popular is not None:
            Spares.objects.filter(Q(category__title__icontains=title) | Q(title__icontains=title) &
                                  Q(is_popular=is_popular)).distinct().count()
        return Spares.objects.filter(Q(category__title__icontains=title) | Q(title__icontains=title)).distinct().count()
    if is_popular is not None:
        return Spares.objects.filter(is_popular=is_popular).count()
    return Spares.objects.count()