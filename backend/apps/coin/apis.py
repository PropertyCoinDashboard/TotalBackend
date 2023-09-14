from .models import (
    CoinSymbolCoinList,
    BitcoinEndPriceData,
    EthereumEndPriceData
)
from .serializers import (
    CoinViewListSerializer,
    BtcEndPriceSerializer,
    EthEndPriceSerializer
)

from .market_apis.coin_apis import TotalCoinMarketlistConcatnate as TKC
from .market_apis.candling import coin_trading_data_concatnate
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView


# # coin symbol 동기화
class MarketCoinListCreateInitialization(APIView):
    queryset = CoinSymbolCoinList.objects.all()
    coin_model_initialization: list[dict[str, str]] = TKC().coin_classifire()

    def create_coin_entries(self, serializer: dict[str, str]) -> None:
        self.queryset.create(
            coin_symbol=serializer["coin_symbol"],
            upbit_existence=serializer["market_depend"]["upbit"],
            bithum_existence=serializer["market_depend"]["bithum"],
            korbit_existence=serializer["market_depend"]["korbit"],
        )

    def post(self, request, *args, **kwargs) -> Response:
        if request.data.get("is_sync"):
            # 일괄 삭제
            with transaction.atomic():
                self.queryset.delete()
                
                # 일괄 생성
                for data in self.coin_model_initialization:
                    self.create_coin_entries(data)

            return Response(
                {"coin_list": self.coin_model_initialization},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Not coin list synchronization"},
                status=status.HTTP_400_BAD_REQUEST,
            )

# 코인 가격
class BaseCoinDataListCreateView(ListCreateAPIView):
    queryset = None
    serializer_class = None
    coin_name = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["timestamp"]
    
    def create(self, request, *args, **kwargs):
        data = coin_trading_data_concatnate(coin_name=self.coin_name)  # 데이터를 가져옵니다.
        print("data -->", data[0]["coin_symbol"])
        with transaction.atomic():
            for item in data:
                self.queryset.create(
                    timestamp=item['timestamp'],
                    trade_price=item['trade_price'],
                )

        return Response({"message": "Data has been created successfully"}, status=status.HTTP_201_CREATED)


class BtcCoinDataListCreateView(BaseCoinDataListCreateView):
    queryset = BitcoinEndPriceData.objects.all()
    serializer_class = BtcEndPriceSerializer
    coin_name = "BTC"
            

class EthCoinDataListCreateView(BaseCoinDataListCreateView):
    queryset = EthereumEndPriceData.objects.all()
    serializer_class = EthEndPriceSerializer
    coin_name = "ETH"



# 전체 코인 리스트
class CoinMarketListView(ListAPIView):
    queryset = CoinSymbolCoinList.objects.all()
    serializer_class = CoinViewListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["coin_symbol"]