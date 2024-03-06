from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    CustomLoginAPIView,
    CustomRegisterAPIView,
    UserApiView,
    VerifyEmailAPIView,
)


urlpatterns = [
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/", CustomLoginAPIView.as_view()),
    path("signup/", CustomRegisterAPIView.as_view()),
    path(
        "profile/<int:pk>/",
        UserApiView.as_view({"get": "retrieve", "patch": "partial_update"}),
    ),
    path("verify-email/", VerifyEmailAPIView.as_view()),
]
