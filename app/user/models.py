from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    '''
    Что бы сделать поле как логин меняйте USERNAME_FIELD

    '''

    # Дефолтные поля
    # username, first_name, last_name, email, password, groups, user_permissions, is_staff, is_active, is_superuser, last_login, date_joined

    username = None
    first_name = None
    last_name = None

    user_name = models.CharField(max_length=150, verbose_name='Имя пользователя', unique=True)

    # phone_regex = RegexValidator(regex=r'^7\d{10}$',
    #                              message="Формат телефона: '79990001234'")
    # phone = models.CharField(validators=[phone_regex], max_length=11,
    #                          verbose_name='Номер телефона', unique=True)


    # ROLE = (
    #     (None, 'Выбрать статус'),
    #     (1, 'Админ'),
    #     (2, 'Клиент'),
    # )
    #
    # role = models.IntegerField(default=2, verbose_name="Роль ЛК", choices=ROLE,
    #                            help_text='''
    #                                          Админ - больший доступ.
    #                                          Клиент - меньший доступ.
    #                                          ''')


    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_name or 'Пользователь'

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'