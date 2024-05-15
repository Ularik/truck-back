from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required()
def index(request):
    return render(request, 'main/index.html')


def robots_txt(request):
    '''
    Для отображения robots.txt
    '''
    content = "User-Agent: *\nDisallow: /"
    return HttpResponse(content, content_type='text/plain')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from ninja import Router, Query

router = Router()

# Тест api
@router.get("/list")
def get_list(request):
    '''
    Получить список
    '''
    return JsonResponse({'message': 'Hello, world!'})


class GetList(APIView):
    def get(self, request):
        data = {'message': 'Hello, world!'}
        return Response(data, status=status.HTTP_200_OK)