from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import apis


# router = DefaultRouter()
# router.register("coin", apis.CoinSynchronSet, basename="coin")
            
            
urlpatterns = [
    # path('api-v1/', include(router.urls))
    path('api-v1/coinsync', apis.CoinSynchronSet.as_view()),
]
