# accounts/urls.py
from django.urls import path, include
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # returns access + refresh
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # dj-rest-auth endpoints (login/logout/password reset, etc.)    
    path("", include("dj_rest_auth.urls")),
    path('register/', RegisterView.as_view(), name='rest_register'),
    # Explicit JWT endpoints via SimpleJWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
