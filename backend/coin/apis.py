from api_injection.coin import UpBitAPIGeneration as ua
from dashboard.models import CoinInforamtionally
from typing import Dict, List

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializer import CoinSynchronizationSerializer


# DestoryAPIView는 고려해볼것
class CoinSynchronSet(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CoinSynchronizationSerializer
    queryset = CoinInforamtionally.objects.all()
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.data["sync"]:
                self.queryset.all().delete()
                return self.create()
    
    def create(self, *args, **kwargs) -> Response:
        coin_list: List[Dict[str, str]] = ua.upbit_coin_total_market_json()
        self.perform_create(coin_list)
        return Response(data=coin_list, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer: ua.upbit_coin_total_market_json()) -> None:
        for data in serializer:
            self.queryset.create(
                k_name=data["korean_name"], e_name=data["english_name"],
                market_name=data["market"], market_warning=data["market_warning"]
            ).save()
    