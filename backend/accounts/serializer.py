from typing import Dict, List
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import AdminUser, NormalUser
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher

# 회원 가입 및 정보 수정 일원화 
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        extra_kwargs: Dict = {
            'password' : {
                'write_only': True,
                "style": {"input_type": "password"}
            }
        }
    
    def validate_password2(self, data: str) -> str:
        if self.initial_data["password"] == data:
            return data
        raise ValidationError(detail="비밀번호가 같지 않습니다", code="password_mismatch")
        
    def save(self, validated_data: Dict) -> None:
        del validated_data["password2"]
        
        password: str = validated_data["password"]
        user_save = super().save(validated_data)
        user_save.set_password(password)
        user_save.save()
        
        return user_save


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=120, min_length=10,
        write_only=True
    )
    class Meta:
        model = None
        fields: List[str] = ["email", "password"]
    
    def validate(self, data):
        email: str = data.get("email")
        password: PasswordHasher = data.get("password")
        
        try:
            user =  self.Meta.model.objects.get(email=email)
        except self.Meta.model.DoesNotExist:
            raise ValidationError(self.error_messages["error"])
        else:
            try:
                user_password: PasswordHasher = user.password 
                pc: bool = PasswordHasher().verify(user_password.encode(), password.encode())
                if pc:
                    token = RefreshToken.for_user(user)
                    refresh = str(token)
                    access = str(token.access_token)
                    
                    data = {
                        "msg": "로그인 성공",
                        "info": {
                            "email": user.email,
                            "refresh": refresh,
                            'access': access
                        }
                    }
                    return data
            except VerifyMismatchError:
                raise ValidationError(self.error_messages["error"])
            
            
# 분권화 
class AdminSerializer(RegisterSerializer):  
    class Meta(RegisterSerializer.Meta):
        model = AdminUser  
        fields: List[str] = ["id", "name", "email", "password", "password2"]
 
        
class UserSerializer(RegisterSerializer):    
    class Meta(RegisterSerializer.Meta):
        model = NormalUser
        fields: List[str] = ["id", "username", "email", "password", "password2"]
        
        
class AdminLoginSerializer(RegisterSerializer):  
    class Meta(LoginSerializer.Meta):
        model = AdminUser  
    
        
class UserLoginSerializer(RegisterSerializer):    
    class Meta(LoginSerializer.Meta):
        model = NormalUser
