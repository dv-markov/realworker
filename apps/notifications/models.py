import datetime
from django.db import models
from apps.orders.models import Order, OrderStatus
from apps.users.models import CustomUser


class NotificationType(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class NotificationStatus(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    notificationTypeId = models.ForeignKey(NotificationType, on_delete=models.PROTECT, null=True)
    notificationStatusId = models.ForeignKey(NotificationStatus, on_delete=models.PROTECT, null=True)
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    recipientId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient')
    creatorId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator')
    timeCreate = models.DateTimeField(auto_now_add=True)
