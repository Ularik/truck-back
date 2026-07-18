from ninja import Router
from django.contrib.auth import authenticate, login, logout
from .schemas import UserAuthSchema, MessageSchema
from django.views.decorators.csrf import csrf_exempt


router = Router()


@router.get('/csrf', response={200: MessageSchema}, auth=None)
@csrf_exempt
def get_csrf(request):
    """
    Дергается фронтом один раз при старте приложения,
    чтобы браузер получил csrftoken cookie.
    """
    from django.middleware.csrf import get_token
    get_token(request)
    return 200, {"detail": "CSRF cookie set"}


@router.get('/me', response={ 200: dict, 401: str})
def get_me(request):
    return 200, {"id": request.user.id, "user_name": request.user.user_name}


@router.post('/login', response={200: dict, 401: str}, auth=None)
def login_user(request, body: UserAuthSchema):
    user = authenticate(user_name=body.user_name, password=body.password)
    if user:
        login(request, user)
        return 200, {"user": user.user_name}
    else:
        return 401, "Not auth"


@router.post('/logout', response={200: MessageSchema})
def logout_view(request):
    logout(request)
    return 200, {"detail": "Вы вышли из системы"}