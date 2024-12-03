from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLES = (
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='buyer')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Поле телефона
    avatar = models.ImageField(upload_to='avatars/', default='avatars/avatar.jpg', blank=True, null=True)

    objects = CustomUserManager()

    class Meta:
        ordering = ['-is_superuser', '-role', 'username']

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/avatars/avatar.jpg'



CustomUser = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # Название поста
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


