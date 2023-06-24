from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from . import apis

# api modelviewset setting 
app_name = "auth"
router = DefaultRouter()

# router.register("authinform", apis.AdminInformAPI)
# router.register("userinform", apis.UserInformAPI)

urlpatterns = [
    path("api-v1/auth-login", apis.AdminLoginAPI.as_view(), name="auth-login"),
    path("api-v1/user-login", apis.UserLoginAPI.as_view(), name="user-login"),
    
    path("api-v1/auth/register", apis.AdminRegisterAPI.as_view(), name="auth-register"),
    path("api-v1/user/register", apis.UserRegisterAPI.as_view(), name="user-register"),
    
    # token
    path("token", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]