from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    # нужно указать логин (тел., мэйл или что-то еще) из модели CustomUser
    # что бы поменять по умолчанию логин, нужно поле user_name заменить на свое, например email
    def create_user(self, user_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not user_name:
            raise ValueError('Нет нужного поля')
        # phone = self.normalize_email(phone)
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # нужно указать логин (тел., мэйл или что-то еще) из модели CustomUser
    def create_superuser(self, user_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(user_name, password, **extra_fields)