from rest_framework import serializers
from .models import Notification, NotificationType, NotificationStatus
from apps.orders.models import Order, OrderStatus
from apps.users.models import CustomUser


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = "__all__"


class NotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationStatus
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
