from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, 
    AnonymousUser
)

from typing import List, Any
from argon2 import PasswordHasher
from dashboard.models import CommonField


# 계정 injectionally
# 프로토콜 설정 
class UserManager(BaseUserManager):
    def _create_user(self, email: str, name: str, password: PasswordHasher = None, **extra_field) -> None:
        if not email:
            raise ValueError("이미 이메일이 존재합니다..!")
    
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            password = PasswordHasher().hash(password),
            **extra_field
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email: str, name: str, password: PasswordHasher = None, **extra_field) -> None:
        extra_field.setdefault("is_staff", False)
        extra_field.setdefault("is_admin", False)
        extra_field.setdefault("is_superuser", False)
        
        return self._create_user(email, name, password, **extra_field)
    
    def create_superuser(self, email: str, name: str, password: PasswordHasher = None, **extra_field) -> None:
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_admin", True)
        extra_field.setdefault("is_superuser", True)
        
        return self._create_user(email, name, password, **extra_field)


class User(AbstractBaseUser, PermissionsMixin, CommonField):
    email = models.EmailField(
        verbose_name=_("이메일"), max_length=255, 
        unique=True, blank=False, null=False
    )
    name = models.CharField(
        verbose_name=_("이름"), max_length=5, 
        blank=False, null=False
    )
    password = models.CharField(
        verbose_name=_("패스워드"), max_length=100,
        blank=False, null=False
    )
    
    # 필수 필드 및 프로토콜 설정 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects: UserManager[Any] = UserManager()
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["name", "password"]
    
    # 어드민 메서드 
    def __str__(self) -> str:
        return f"{self.email}"
    
    def has_perm(self, perm, obj=None) -> bool:
        return True
    
    def has_module_perms(self, app_label) -> bool:
        return True
    
    class Meta:
        db_table: str = "admin_user"
        # app_label: str = "auth_user_db" 


class NormalUser(AnonymousUser, CommonField):
    email = models.EmailField(
        verbose_name=_("이메일"), max_length=255, 
        unique=True, blank=False, null=False
    )
    name = models.CharField(
        verbose_name=_("이름"), max_length=5, 
        blank=False, null=False
    )
    password = models.CharField(
        verbose_name=_("패스워드"), max_length=100,
        blank=False, null=False
    )
    
    def __str__(self) -> str:
        return "일반유저"
    
    class Meta:
        db_table: str = "normal_user"
        # app_label: str = "auth_user_db" 