import uuid

from django.db import models
from apps.users.models import CustomUser, Category, Specialization, Qualification, GeoData


class File(models.Model):
    # order_id = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    file_url = models.TextField(blank=True)

    def __str__(self):
        return self.file_url


class Chat(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    number = models.UUIDField(default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT, null=True)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT, null=True)
    description = models.TextField(blank=True)
    address = models.ForeignKey(GeoData, on_delete=models.PROTECT, null=True)
    # address = models.TextField(blank=True)
    date_time = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0)
    customer = models.ForeignKey(CustomUser, related_name="customer", on_delete=models.PROTECT, null=True)
    worker = models.ForeignKey(CustomUser, related_name="worker", on_delete=models.PROTECT, null=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, null=True)
    files = models.ManyToManyField("File")
    chats = models.ManyToManyField("Chat")

    def __str__(self):
        return str(self.number)


