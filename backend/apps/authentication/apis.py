from .serializers import (
    AdminRegisterSerializer,
    UserRegisterSerializer,
    AdminLoginSerializer,
    NormalUserLoginSerializer,
)
from .models import AdminUser, NormalUser
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import permissions as P
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import Serializer


# 로그인 
class UserLoginAPI(APIView):
    """
    로그인 추상화 
    """
    permission_classes: P = (P.AllowAny, )
    serializer_class: Serializer = None
    
    def get(self, request, *args, **kwargs) -> Response:
        return Response(data={"notice": "로그인을 위한 이메일 비밀번호를 입력해주세요..!"}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs) -> Response:
        login_serializer = self.serializer_class(data=request.data)
        if login_serializer.is_valid(raise_exception=False):
            login = login_serializer.validate(data=request.data)
            if login is not False:
                return Response(login, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(self.serializer_class.error_messages, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes: P = (P.AllowAny,)
    serializer_class: Serializer = AdminRegisterSerializer


class UserRegisterAPI(CreateAPIView):
    queryset = NormalUser.objects.all()
    permission_classes: P = (P.AllowAny,)
    serializer_class: Serializer = UserRegisterSerializer


