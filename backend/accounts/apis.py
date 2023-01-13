from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (
    AdminSerializer, UserSerializer, 
    AdminLoginSerializer, UserLoginSerializer
)

from accounts.models import AdminUser, NormalUser


class LoginAPI(APIView):
    permission_classes = (AllowAny, )
    
    def post(self, request):
        login_serializer = self.serializer_class(data=request.data)
        if login_serializer.is_valid(raise_exception=True):
            login = login_serializer.validate(data=request.data)
            if login is not False:
                return Response(login, status=status.HTTP_202_ACCEPTED)
        else:
            data = {"msg": "비정상적인 접근입니다"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    
# 정보 수정 
class CrudAPI(ModelViewSet):
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
class AdminRegisterAPI(CreateAPIView):
    queryset = AdminUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = AdminSerializer
    
    
class UserRegisterAPI(CreateAPIView):
    queryset = NormalUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    
    
# 로그인
class AdminLoginAPI(LoginAPI):
    serializer_class = AdminLoginSerializer
    
   
class UserLoginAPI(LoginAPI):
    serializer_class = UserLoginSerializer
    
    
# 회원 정보 보이는 기준을 선정해서 쿼리셋 바꿀것 
class AdminInformAPI(CrudAPI):
    queryset = AdminUser.objects.all()
    serializer_class = AdminSerializer
    

class UserInformAPI(CrudAPI):
    queryset = NormalUser.objects.all()
    serializer_class = UserSerializer
