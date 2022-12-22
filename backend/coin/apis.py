from typing import Dict, List
from api_injection.coin_apis import TotalCoinMarketListConcatnate as TKC
from api_injection.coin_apis import UpbitAPI, BithumAPI
from dashboard.models import (
    CoinSymbolCoinList, UpbitCoinList, BitThumCoinList)
    

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializer import CoinSynchronizationSerializer
from .serializer import CoinViewListSerializer


# DestoryAPIView는 고려해볼것
class MarketListSynchronSet(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CoinSynchronizationSerializer
    coin_model_initialization = None
       
    def create(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.queryset.all().delete()
        coin_list: List[Dict[str, str]] = self.coin_model_initialization
        self.perform_create(coin_list)
        headers = self.get_success_headers(serializer.data)
                
        return Response(data={"coin_list": coin_list}, status=status.HTTP_201_CREATED, headers=headers)


class MarketListTotal(MarketListSynchronSet):
    queryset = CoinSymbolCoinList.objects.all()
    coin_model_initialization = TKC().coin_total_preprecessing()
    
    def perform_create(self, serializer) -> None:
        for data in serializer:
            self.queryset.create(
                coin_symbol=data
            ).save()
        
        
class UpbitListInitialization(MarketListSynchronSet):
    queryset = UpbitCoinList.objects.all()
    coin_model_initialization = UpbitAPI(name=None).upbit_market
    
    def perform_create(self, serializer) -> None:
        for data in serializer:
            self.queryset.create(
                market=data["market"],
                k_name=data["korean_name"], 
                e_name=data["english_name"],
                market_warning=data["market"],
            ).save()
            

class BithumListInitialization(MarketListTotal):
    queryset = BitThumCoinList.objects.all()
    coin_model_initialization = BithumAPI(name=None).bithum_market_list()


class MarketListView(ListAPIView):
    queryset = CoinSymbolCoinList.objects.all()
    serializer_class = CoinViewListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['coin_symbol']

    def get(self, *args, **kwargs):
        qs = self.request.GET.get("coin_symbol")
        qs = qs.upper()
        return Response(data={"coin": qs}, status=status.HTTP_200_OK)
