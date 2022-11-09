from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from . import apis

# api modelviewset setting 
app_name = "auth"
router = DefaultRouter()

router.register("auth", apis.AdminRegisterAPI)
router.register("normal", apis.UserRegisterAPI)

urlpatterns = [
    path("api-v1/", include(router.urls)),
    path("auth/login/", apis.AdminLoginAPI.as_view()),
    path("user/login/", apis.UserLoginAPI.as_view()),
    
    # token
    path("token", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]