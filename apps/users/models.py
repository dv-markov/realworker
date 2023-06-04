import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField('Роль', max_length=100, db_index=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    # username_validator = UnicodeUsernameValidator()

    name = models.CharField('ФИО', max_length=255, default='')
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)

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


class UserProfile(models.Model):
    country = models.ForeignKey('Country', on_delete=models.PROTECT, null=True)
    specializations = models.ManyToManyField('Specialization')  # , null=True)
    qualifications = models.ManyToManyField('Qualification')  # , null=True)
    photo = models.CharField('Photo', max_length=255, default='')
    company = models.CharField('Company', max_length=255, default='')
    position = models.CharField('Position', max_length=255, default='')
    last_active = models.DateTimeField('Last active', auto_now_add=True)
    messages = models.CharField('Messages', max_length=255, default='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.name


# class ReturnNameDbIndex(models.Model):
#     name = models.CharField(max_length=255, db_index=True)
#
#     def __str__(self):
#         return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT, null=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class GeoData(models.Model):
    source = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255, db_index=True)
    country_text = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city_area = models.CharField(max_length=255)
    city_district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    geo_lat = models.CharField(max_length=255)
    geo_lon = models.CharField(max_length=255)
    qc_geo = models.CharField(max_length=255)
