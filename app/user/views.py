from ninja import Router
from ninja_jwt.authentication import JWTAuth


router = Router()


@router.get('/me', auth=JWTAuth())
def get_me(request):
    return {'id': request.user.id, 'user_name': request.user.user_name}
