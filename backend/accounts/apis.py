from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (
    AdminSerializer, UserSerializer, 
    AdminLoginSerializer, UserLoginSerializer
)

from accounts.models import AdminUser, NormalUser


class LoginViewAPI(APIView):
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
    
    
# 회원 가입
class AdminRegisterAPI(ModelViewSet):
    queryset = AdminUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = AdminSerializer
    
    
class UserRegisterAPI(ModelViewSet):
    queryset = NormalUser.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer


# 로그인 
class AdminLoginAPI(LoginViewAPI):
    serializer_class = AdminLoginSerializer
    
    
class UserLoginAPI(LoginViewAPI):
    serializer_class = UserLoginSerializer
