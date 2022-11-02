from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .serializer import (
    AdminSerializer, UserSerializer
)

from django.shortcuts import get_object_or_404
from accounts.models import AdminUser, NormalUser


# 회원 가입
class AdminRegisterAPI(ModelViewSet):
    queryset = AdminUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = AdminSerializer
    
    
class UserRegisterAPI(ModelViewSet):
    queryset = NormalUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    
    
# 관리자 기능 
class AdminInformAPI(ModelViewSet):
    queryset = AdminUser.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = AdminSerializer
    
    
# 일반 유저 기능 
class UserInformAPI(ModelViewSet):
    queryset = NormalUser.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    
