from ninja import Router, File, Form
from ninja.files import UploadedFile
from .models import Truck, Spares, ImagesSpares, Units
from .schema import TruckOutListSchema, GeneralResponseSchema, SparesCreateUpdateSchema, UnitOutSchema, SparesOutSchema
from django.db.models import Q
from ninja.errors import HttpError
from django.db.models import Prefetch
from django.views.decorators.csrf import csrf_exempt


router = Router()

@router.get('/get-trucks', response={200: list[TruckOutListSchema], 400: str}, auth=None)
@csrf_exempt
def get_trucks(request):
    return Truck.objects.all()


@router.get('/units', response={200: list[UnitOutSchema], 400: str}, auth=None)
@csrf_exempt
def get_units(request):
    return Units.objects.all()


@router.get('/get-spares', response={200: GeneralResponseSchema, 400: str}, auth=None)
@csrf_exempt
def get_spares(request, title: str = None, category: int = None, truck: int = None, is_popular: bool = None, limit: int = 10, offset: int = 0):
    params = {}
    if is_popular is not None:
        params['is_popular'] = is_popular

    if category is not None:
        params['category_id'] = category

    if truck is not None:
        params['truck__id'] = truck

    query_filter = Q()
    if title:
        query_filter &= (Q(title__icontains=title) | Q(category__title__icontains=title))

    # 1. Применяем фильтры и ДОБАВЛЯЕМ prefetch_related для картинок
    # select_related('category') подтянет данные категорий одним JOIN'ом, если они нужны в схеме
    qs = Spares.objects.filter(query_filter, **params) \
        .prefetch_related('images',
                          Prefetch('truck',
                                   queryset=Truck.objects.only('id'))
                          ) \
        .distinct()

    # 2. Считаем общее количество ДО среза пагинации
    total_count = qs.count()

    # 3. Делаем слайсинг (пагинацию) на уровне базы данных
    qs = qs[offset:offset + limit]

    result = []
    for spare in qs:
        result.append({
            'id': spare.id,
            'title': spare.title,
            'description': spare.description,
            'truck': [truck.id for truck in spare.truck.all()],
            'category_id': spare.category_id,
            'price': spare.price,
            'count': spare.count,
            'is_popular': spare.is_popular,
            'images': [img.image.url for img in spare.images.all().order_by('order') if img.image]
        })

    return 200, {'count': total_count, 'result': result}


@router.get('/get-spares/{id}', response={200: SparesOutSchema}, auth=None)
@csrf_exempt
def get_one_detail(request, id: int):
    spare = (Spares.objects
                .prefetch_related('images',
                        Prefetch('truck',
                               queryset=Truck.objects.only('id'))
                ) \
                .get(pk=id))
    data = {
        'id': spare.id,
        'title': spare.title,
        'description': spare.description,
        'truck': [truck.id for truck in spare.truck.all()],
        'category_id': spare.category_id,
        'price': spare.price,
        'count': spare.count,
        'is_popular': spare.is_popular,
        'images': [img.image.url for img in spare.images.all().order_by('order') if img.image]
    }
    return data


@router.post("/spares")
def post_spares(request, body: SparesCreateUpdateSchema = Form(...), images: list[UploadedFile] = File([])):
    body = body.dict()
    trucks = body.pop('truck') or []
    spare = Spares.objects.create(**body)
    spare.truck.add(*trucks)
    ImagesSpares.objects.bulk_create([ImagesSpares(image=file_img, spare=spare) for file_img in images])

    return {200: spare.id}


@router.put("/spares/{id}")
def put_spares(
    request,
    id: int,
    body: SparesCreateUpdateSchema = Form(...),
    images: list[UploadedFile] = File([]),
    existing_image_ids: list[str] = Form([]),  # id существующих картинок в нужном порядке
):
    body = body.dict()
    trucks = body.pop('truck') or []
    spare = Spares.objects.get(pk=id)
    for attr, value in body.items():
        setattr(spare, attr, value)
    spare.save()
    spare.truck.add(*trucks)

    # переставляем существующие
    existing_images = ImagesSpares.objects.filter(spare=spare)
    remaining_ids: set[int] = set()
    for position, img_name in enumerate(existing_image_ids):
        if img_name.startswith('/media/'):
            img_name = img_name.replace('/media/', '')
        img = existing_images.filter(image=img_name).first()
        img.order = position
        img.save()
        remaining_ids.add(img.id)

    ImagesSpares.objects.filter(spare=spare).exclude(id__in=remaining_ids).delete()

    # новые добавляем в конец
    start = len(existing_image_ids)
    ImagesSpares.objects.bulk_create([
        ImagesSpares(image=file_img, spare=spare, order=start + i)
        for i, file_img in enumerate(images)
    ])

    return {200: spare.id}


@router.delete("/spares/{id}")
def delete_spares(request, id: int):
    try:
        result = Spares.objects.get(pk=id).delete()
        return {200: 'delete'}
    except Spares.DoesNotExist as err:
        raise HttpError(404, 'Spare does not exist') from err