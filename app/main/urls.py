from django.urls import path, include
from .views import index, robots_txt, get_list, GetList

urlpatterns = [
    path('', index, name='index'),
    path('robots.txt', robots_txt),

    path('api/main/list2', GetList.as_view(), name='get_list'), # DRF вариант
]