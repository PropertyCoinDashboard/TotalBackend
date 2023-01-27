from typing import Dict, List
from api_injection.coin_apis import TotalCoinMarketlistConcatnate as TKC
from api_injection.coin_apis import UpbitAPI, BithumAPI
from dashboard.models import (
    CoinSymbolCoinList, UpbitCoinList, 
    BitThumCoinList, SearchBurketCoinIndexing)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.mixins import DestroyModelMixin
from rest_framework.generics import (
    CreateAPIView, ListAPIView, ListCreateAPIView
)

from .serializer import (
    CoinSynchronizationSerializer, CoinViewListSerializer,
    CoinBurketSerializer
)

from drf_yasg.utils import swagger_auto_schema


# 추상화된 기능 
class MarketListSynchronSet(CreateAPIView, DestroyModelMixin):
    serializer_class = CoinSynchronizationSerializer
    coin_model_initialization = None
    
    def perform_destroy(self):
        return self.queryset.all().delete()

    def create(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_destroy()
        coin_list: List[Dict[str, str]] = self.coin_model_initialization
        self.perform_create(coin_list)
        headers = self.get_success_headers(serializer.data)
                
        return Response(data={"coin_list": coin_list}, status=status.HTTP_201_CREATED, headers=headers)
    

# 빗썸 코인 저장 
class BithumListInitialization(MarketListSynchronSet):
    queryset = BitThumCoinList.objects.all()
    coin_model_initialization = BithumAPI(name=None).bithum_market_list()
    
    def perform_create(self, serializer) -> None:
        for data in serializer:
            self.queryset.create(
                coin_symbol=data
            ).save()


# 업비트 코인 저장                         
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
       

# 모든 코인 저장 
class MarketListTotalInitialization(BithumListInitialization):
    queryset = CoinSymbolCoinList.objects.all()
    coin_model_initialization = TKC().coin_total_list()
    

# 데이터 반환 
class MarketDataCreateBurketInitialization(ListCreateAPIView, MarketListSynchronSet):
    queryset = SearchBurketCoinIndexing.objects.all()
    serializer_class = CoinBurketSerializer
        
    def create(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_destroy()        
        self.perform_create(serializer=serializer)
                
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------------------------------------------------------------------#


# 전체 코인 리스트
class MarketListView(ListAPIView):
    queryset = CoinSymbolCoinList.objects.all()
    serializer_class = CoinViewListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['coin_symbol']
        


    

    
    
    

