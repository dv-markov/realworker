import datetime
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import File, Chat, OrderStatus, Order
from .serializers import FileSerializer, ChatSerializer, OrderStatusSerializer, OrderSerializer, \
    CustomerOrderSerializer, WorkerOrderSerializer, OpenOrderSerializer, CreateOrderSerializer, OrderCreateSerializer
from .permissions import IsCustomer

CUSTOMER_ROLE_NAME = "customer"
WORKER_ROLE_NAME = "worker"


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('pk')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return Order.objects.all()
        return Order.objects.filter(pk=pk)

    @action(detail=False, methods=['post'], url_path='create-order',
            permission_classes=[permissions.IsAuthenticated, IsCustomer])
    def create_order(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     current_year = datetime.datetime.now().year % 100
    #     max_order = Order.objects.order_by('-number').first()
    #     if max_order:
    #         max_order_number = int(max_order.number[-4:])
    #         new_order_number = max_order_number + 1
    #     else:
    #         new_order_number = 1
    #     serializer.save(number=f"{current_year:02d}-{new_order_number:04d}")


class MyOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.role.name == CUSTOMER_ROLE_NAME:
            return CustomerOrderSerializer
        elif user.role.name == WORKER_ROLE_NAME:
            return WorkerOrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role.name == CUSTOMER_ROLE_NAME:
            return Order.objects.filter(customer=user)
        elif user.role.name == WORKER_ROLE_NAME:
            return Order.objects.filter(worker=user)


class OpenOrderListView(generics.ListAPIView):
    queryset = Order.objects.filter(worker=None)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OpenOrderSerializer

    # def get_serializer_class(self):
    #     user = self.request.user
    #     if user.role.name == WORKER_ROLE_NAME:
    #         return OpenOrderSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.role.name == WORKER_ROLE_NAME:
            return super().get(request, *args, **kwargs)
        return Response({})


# class CreateOrderView(generics.CreateAPIView):
#     serializer_class = CreateOrderSerializer
#     permission_classes = [permissions.IsAuthenticated]
