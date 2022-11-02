from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import apis

# api modelviewset setting 
app_name = "auth"
router = DefaultRouter()

router.register("auth", apis.AdminRegisterAPI)
router.register("auth-all", apis.AdminInformAPI)

router.register("normal", apis.UserRegisterAPI)
router.register("normal-all", apis.UserInformAPI)

urlpatterns = [
    path("api-v1/", include(router.urls)),
]