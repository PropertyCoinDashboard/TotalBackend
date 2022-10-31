from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .serializer import (
    AdminSerializer, UserSerializer
)

from accounts.models import AdminUser, NormalUser


# 정보 수정 
class UDAPI(ModelViewSet):
    permission_classes = (IsAuthenticated, )

    def destroy(self, request, *args, **kwargs):
        user_id = int(self.kwargs.get("pk"))
        if self.request.user.id == user_id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"remove": True}, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {"detail": "정보를 확인하여주세요"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)  


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
class AdminInformAPI(UDAPI):
    queryset = AdminUser.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = AdminSerializer
    
    
# 일반 유저 기능 
class UserInformAPI(UDAPI):
    queryset = NormalUser.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
