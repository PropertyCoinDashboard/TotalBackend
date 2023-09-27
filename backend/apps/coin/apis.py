from typing import Any
from .models import (
    CoinSymbolCoinList,
    BitcoinEndPriceData,
    EthereumEndPriceData,
    RippleEndPriceData
)
from .serializers import (
    CoinViewListSerializer,
    BtcEndPriceSerializer,
    EthEndPriceSerializer,
    XrpEndPriceSerializer
)

from .market_apis.coin_apis import TotalCoinMarketlistConcatnate as TKC
from .market_apis.coin_apis import present_price_coin
from .market_apis.candling import coin_trading_data_concatnate
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView


# coin symbol 동기화
class MarketCoinListCreateInitialization(APIView):
    queryset = CoinSymbolCoinList.objects.all()
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.coin_model_initialization: list[dict[str, str]] = TKC().coin_classifire()

    def create_coin_entries(self) -> None:
        coins: list[CoinSymbolCoinList] = [
            CoinSymbolCoinList(
                coin_symbol=coin["coin_symbol"],
                upbit_existence=coin["market_depend"]["upbit"],
                bithum_existence=coin["market_depend"]["bithum"],
                korbit_existence=coin["market_depend"]["korbit"],
                coinone_existence=coin["market_depend"]["coinone"]
            ) for coin in self.coin_model_initialization
        ]
        self.queryset.bulk_create(coins)
        
    def get(self, request, *args, **kwargs) -> Response:
        return Response(data={"notion": "동기화를 눌러주세요"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response:
        if request.data.get("is_sync"):
            # 삭제후 다시 생성
            with transaction.atomic():
                self.queryset.delete()
                self.create_coin_entries()
            return Response(
                {"coin_list": self.coin_model_initialization},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Not coin list synchronization"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
        
# 코인 가격
class BaseCoinDataListCreateView(ListCreateAPIView):
    queryset = None
    coin_name = None
    serializer_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["timestamp"]
    
    def create(self, request, *args, **kwargs) -> Response:
        data: list[dict] = coin_trading_data_concatnate(coin_name=self.coin_name)  # 데이터를 가져옵니다.
        with transaction.atomic():
            for item in data:
                self.queryset.create(
                    timestamp=item['timestamp'],
                    trade_price=item['trade_price'],
                )
        return Response({"message": "Data has been created successfully"}, status=status.HTTP_201_CREATED)


# 코인 현재가격 가져오기 (비트코인, 이더리움, 리플... etc)
class CoinPriceView(APIView):
    def get(self, request, coin_symbol: str):
        try:
            price: float = present_price_coin(coin_symbol)
            return Response({'coin': coin_symbol, 'average_price': price}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        
        
# 전체 코인 리스트
class CoinMarketListView(ListAPIView):
    queryset = CoinSymbolCoinList.objects.all()
    serializer_class = CoinViewListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["coin_symbol"]


# 비트코인
class BtcCoinDataListCreateView(BaseCoinDataListCreateView):
    queryset = BitcoinEndPriceData.objects.all()
    serializer_class = BtcEndPriceSerializer
    coin_name = "BTC"

            
# 이더리움
class EthCoinDataListCreateView(BaseCoinDataListCreateView):
    queryset = EthereumEndPriceData.objects.all()
    serializer_class = EthEndPriceSerializer
    coin_name = "ETH"


# 리플
class XrpCoinDataListCreateView(BaseCoinDataListCreateView):
    queryset = RippleEndPriceData.objects.all()
    serializer_class = XrpEndPriceSerializer
    coin_name = "XRP"



