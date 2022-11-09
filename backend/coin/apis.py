from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from dashboard.models import CoinInforamtionally
from .serializer import CoinSynchronizationSerializer
from api_injection.coin import upbit_coin_total_market_json



# DestoryAPIView는 고려해볼것 
class CoinSynchronSet(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CoinSynchronizationSerializer
    queryset = CoinInforamtionally.objects.all()
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.data["sync"] == True:
                self.queryset.all().delete()
                return self.create()
    
    def create(self, *args, **kwargs):
        coin_list = upbit_coin_total_market_json()
        self.perform_create(coin_list)
        return Response(data=coin_list, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer):
        for data in serializer:
            self.queryset.create(
                k_name=data["korean_name"], e_name=data["english_name"],
                market_name=data["market"], market_warning=data["market_warning"]
            ).save()
            