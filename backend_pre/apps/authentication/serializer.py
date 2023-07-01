from typing import *
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AdminUser, NormalUser
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher


# 회원 가입 및 정보 수정 일원화 
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        fields: List[str] = ["id", "name", "email", "password", "password2"]
        extra_kwargs: Dict[str, Dict[str, Any]] = {
            'password' : {
                'write_only': True,
                "style": {"input_type": "password"}
            }
        }
    
    def validate_password2(self, data: str) -> str:
        if self.initial_data["password"] == data:
            return data
        raise ValidationError(detail="비밀번호가 같지 않습니다", code="password_mismatch")
        
    def create(self, validated_data: Dict) -> None:
        del validated_data["password2"]
        
        password: str = validated_data["password"]
        user_save = super().create(validated_data)
        user_save.set_password(password)
        user_save.save()
        
        return user_save


class LoginSerializer(serializers.ModelSerializer):
    error_messages = {
        "login": "아이디와 비밀번호를 입력해주세요",
    }
    
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    
    class Meta:
        fields: List[str] = ["email", "password"]


    def validate(self, data):
        email: str = data.get("email")
        password: PasswordHasher = data.get("password")
        
        try:
            user = self.Meta.model.objects.get(email=email)
            user_password: PasswordHasher = user.password 
            pc: bool = PasswordHasher().verify(str(user_password).strip("argon2"), password)
            if pc:
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)
                data: Dict[str, Any] = {
                    "msg": "로그인 성공",
                    "info": {
                        "email": user.email,
                        "refresh": refresh,
                        'access': access
                    }
                }
                return data
        except (self.Meta.model.DoesNotExist, VerifyMismatchError):
            raise ValidationError(self.error_messages)
            
            
# 분권화 
class AdminRegisterSerializer(RegisterSerializer):  
    class Meta(RegisterSerializer.Meta):
        model = AdminUser  

        
class UserRegisterSerializer(RegisterSerializer):    
    class Meta(RegisterSerializer.Meta):
        model = NormalUser
        
        
class AdminLoginSerializer(LoginSerializer):  
    class Meta(LoginSerializer.Meta):
        model = AdminUser  
    
        
class UserLoginSerializer(LoginSerializer):    
    class Meta(LoginSerializer.Meta):
        model = NormalUser
