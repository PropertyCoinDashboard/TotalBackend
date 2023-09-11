from typing import List, Dict
from ...dashboaring.models import CoinSymbolCoinList


from .coin_api_injection.coin_apis import TotalCoinMarketlistConcatnate as TKC
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import CoinViewListSerializer


# # coin symbol 동기화
class MarketCoinListCreateInitalization(APIView):
    queryset = CoinSymbolCoinList.objects.all()
    coin_model_initialization: List[Dict[str, str]] = TKC().coin_classifire()

    def perform_create(self, serializer: Dict[str, str]) -> None:
        self.queryset.create(
            korea_name=serializer["korean_name"],
            coin_symbol=serializer["coin_symbol"],
            upbit_existence=serializer["market_depend"]["upbit"],
            bithum_existence=serializer["market_depend"]["bithum"],
            korbit_existence=serializer["market_depend"]["korbit"],
        )

    def post(self, request, format=None) -> Response:
        if request.data.get("is_sync"):
            # 일괄 삭제
            self.queryset.delete()

            # 일괄 생성
            for data in self.coin_model_initialization:
                self.perform_create(data)

            return Response(
                {"coin_list": self.coin_model_initialization},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Not coin list synchronization"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 전체 코인 리스트
class MarketListView(ListAPIView):
    queryset = CoinSymbolCoinList.objects.all()
    serializer_class = CoinViewListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["coin_symbol"]