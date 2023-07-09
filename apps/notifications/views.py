from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Notification, NotificationType, NotificationStatus
from .serializers import NotificationSerializer, NotificationTypeSerializer, NotificationStatusSerializer
from .permissions import IsCustomer, IsWorker

CUSTOMER_ROLE_NAME = "customer"
WORKER_ROLE_NAME = "worker"


class NotificationTypeListView(generics.ListAPIView):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationStatusListView(generics.ListAPIView):
    queryset = NotificationStatus.objects.all()
    serializer_class = NotificationStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
