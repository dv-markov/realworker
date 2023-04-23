from django.db import models
from django.contrib.auth.models import AbstractUser, Group
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # username_validator = UnicodeUsernameValidator()

    name = models.CharField('ФИО', max_length=255, default='')
    city = models.CharField('Город', max_length=255, default='')
    role = models.ForeignKey(Group, on_delete=models.PROTECT, null=True)

    username = models.CharField(
        "Телефон",
        max_length=150,
        unique=True,
        help_text="Обязательно поле для регистрации",
        # validators=[username_validator],
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )

    REQUIRED_FIELDS = ["name", "city", "role", "email"]
