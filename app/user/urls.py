from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
# from .views import CustomLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('accounts/logout/', LogoutView.as_view(next_page="/"), name='Logout'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/password_change/', PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),


    path("api/token/get", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify", TokenVerifyView.as_view(), name="token_verify"),
]