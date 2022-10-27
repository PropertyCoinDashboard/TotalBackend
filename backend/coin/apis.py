from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import requests
from dashboard.models import CoinInforamtionally
from .serializer import CoinSynchronizationSerializer



# ModelViewSet 사용 가능 
class CoinSynchronSet(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CoinSynchronizationSerializer

    def post(self, request):
        coin_serializer = self.serializer_class(data=request.data)
        if coin_serializer.is_valid(raise_exception=True):
            url = "https://api.upbit.com/v1/market/all?isDetails=false"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            info = response.json()
            
            for data in info:
                CoinInforamtionally.objects.create(
                    k_name=data["korean_name"], e_name=data["english_name"],
                    market_name=data["market"],
                ).save()
            return Response(data=info, status=status.HTTP_200_OK)
        else:
            return Response(data={"detail": False}, status=status.HTTP_204_NO_CONTENT)
