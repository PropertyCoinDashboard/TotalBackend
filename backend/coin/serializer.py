from typing import List
from rest_framework import serializers
from accounts.models import DataInjection

"""
직렬화 만들고  -> 요청 -> API 불러오기 요롷게 
웨어하우스는 고려해보는걸로 

사이즈가 엄청엄청 커졋네
"""


class CoinSynchronizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataInjection
        fields: List[str] = ["sync"]
        
    
    