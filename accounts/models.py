from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Username kiritilishi shart")
        if not email:
            raise ValueError("Email kiritilishi shart")
        if not password:
            raise ValueError("Parol kiritilishi shart")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "seller")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo'lishi kerak.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True bo'lishi kerak.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('seller', 'Sotuvchi'),
        ('buyer', 'Xaridor'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='buyer',
        verbose_name="Foydalanuvchi roli",
        help_text="Foydalanuvchi roli: Sotuvchi yoki Xaridor"
    )

    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon raqami")
    address = models.TextField(blank=True, verbose_name="Manzil")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")

    shop_name = models.CharField(max_length=100, blank=True, verbose_name="Do'kon nomi")
    is_verified = models.BooleanField(default=False, verbose_name="Tasdiqlangan")

    objects = CustomUserManager()
    
    @property
    def is_seller(self):
        return self.role == 'seller'
    
    @property
    def is_buyer(self):
        return self.role == 'buyer'

    def __str__(self):
        if self.is_seller and self.shop_name:
            return f"{self.username} ({self.shop_name})"
        return f"{self.username} ({self.get_role_display()})"