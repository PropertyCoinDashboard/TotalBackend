from .serializers import (
    AdminRegisterSerializer,
    UserRegisterSerializer,
    AdminLoginSerializer,
    NormalUserLoginSerializer,
)
from .models import AdminUser, NormalUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


# 로그인 
class UserLoginAPI(APIView):
    """
    로그인 추상화 
    """
    permission_classes = (AllowAny, ) 
    
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data)
        if login_serializer.is_valid(raise_exception=True):
            login = login_serializer.validate(data=request.data)
            if login is not False:
                return Response(login, status=status.HTTP_202_ACCEPTED)
        else:
            data = {"msg": "비정상적인 접근입니다"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginAPI(UserLoginAPI):
    serializer_class = AdminLoginSerializer
    
    
class NormalLoginAPI(UserLoginAPI):
    serializer_class = NormalUserLoginSerializer
    

"""
< ----------------------------------------------------- >
"""

# 회원 가입
class AdminRegisterAPI(CreateAPIView):
    queryset = AdminUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AdminRegisterSerializer


class UserRegisterAPI(CreateAPIView):
    queryset = NormalUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


