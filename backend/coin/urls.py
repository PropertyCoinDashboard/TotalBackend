from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import apis


# router = DefaultRouter()
# router.register("coin", apis.CoinViewSet, basename="coin")
            
            
urlpatterns = [
    path('api-v1/', apis.CoinSynchronSet.as_view())
    # path("api-v1/", include(router.urls))
]
