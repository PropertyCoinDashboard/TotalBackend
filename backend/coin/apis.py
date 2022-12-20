import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


from api_injection.coin_apis import TotalCoinmarketListConcatnate as TKC
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
        coin_list: List[Dict[str, str]] = TKC().coin_total_preprecessing()
        self.perform_create(coin_list)
        return Response(data=coin_list, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer) -> None:
        for data in serializer:
            self.queryset.create(
                e_name=data
            ).save()
    