from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    AdminRegisterSerializer,
    UserRegisterSerializer,
    AdminLoginSerializer,
    UserLoginSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from .models import AdminUser, NormalUser


class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data)
        if login_serializer.is_valid(raise_exception=False):
            login = login_serializer.validate(data=request.data)
            if login is not False:
                return Response(login, status=status.HTTP_202_ACCEPTED)
        else:
            data = {"msg": "비정상적인 접근입니다"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


# 회원 가입
class AdminRegisterAPI(CreateAPIView):
    queryset = AdminUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AdminRegisterSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRegisterAPI(CreateAPIView):
    queryset = NormalUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# 로그인
class AdminLoginAPI(LoginAPI):
    serializer_class = AdminLoginSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserLoginAPI(LoginAPI):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
