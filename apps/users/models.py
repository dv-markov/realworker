from django.db import models
from django.contrib.auth.models import AbstractUser, Group
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # username_validator = UnicodeUsernameValidator()

    name = models.CharField('ФИО', max_length=255, default='')
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True)
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


class UserProfile(models.Model):
    country = models.ForeignKey('Country', on_delete=models.PROTECT, null=True)
    specializations = models.ManyToManyField('Specialization')  # , null=True)
    qualifications = models.ManyToManyField('Qualification')  # , null=True)
    photo = models.CharField('Photo', max_length=255, default='')
    company = models.CharField('Company', max_length=255, default='')
    position = models.CharField('Position', max_length=255, default='')
    last_active = models.DateTimeField('Last active', auto_now_add=True)
    messages = models.CharField('Messages', max_length=255, default='')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.user.name


class ReturnNameDbIndex(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Country(ReturnNameDbIndex):
    pass


class City(ReturnNameDbIndex):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True)


class Category(ReturnNameDbIndex):
    pass


class Specialization(ReturnNameDbIndex):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)


class Qualification(ReturnNameDbIndex):
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT, null=True)
    price = models.IntegerField(default=0)


class GeoData(models.Model):
    source = models.CharField(blank=True)
    result = models.CharField(blank=True)
    postal_code = models.CharField(blank=True)
    country = models.CharField(blank=True)
    region = models.CharField(blank=True)
    city_area = models.CharField(blank=True)
    city_district = models.CharField(blank=True)
    street = models.CharField(blank=True)
    house = models.CharField(blank=True)
    geo_lat = models.CharField(blank=True)
    geo_lon = models.CharField(blank=True)
    qc_geo = models.CharField(blank=True)


class OrderStatus(ReturnNameDbIndex):
    pass


class Order(models.Model):
    number = models.CharField(max_length=255, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT, null=True)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT, null=True)
    description = models.CharField(blank=True)
    address = models.ForeignKey(GeoData, on_delete=models.PROTECT, null=True)
    date_time = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0)
    customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True)
    worker = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, null=True)
    files = models.ManyToManyField("File")
    chats = models.ManyToManyField("Chat")

    def __str__(self):
        return self.number


class File(models.Model):
    # order_id = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    file_url = models.CharField(blank=True)

    def __str__(self):
        return self.file_url


class Chat(ReturnNameDbIndex):
    content = models.CharField(blank=True)

