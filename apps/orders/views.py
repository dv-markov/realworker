import datetime
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import File, Chat, OrderStatus, Order
from .serializers import FileSerializer, ChatSerializer, OrderStatusSerializer, OrderSerializer, \
    CustomerOrderSerializer, WorkerOrderSerializer, OpenOrderSerializer, CreateOrderSerializer, OrderCreateSerializer, \
    OrderDetailSerializer, AssignOrderSerializer
from .permissions import IsCustomer, IsWorker

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


class ShowOrderDetailsView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorker]
    lookup_field = 'number'

    # опционально - фильтрация запроса при обращении в базу
    # def get_queryset(self):
    #     queryset = Order.objects.filter(order_status=1)
    #     return queryset


class AssignOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = AssignOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorker]
    lookup_field = 'number'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.worker:
            return Response({"detail": "Для этого заказа уже назначен исполнитель."}, status=status.HTTP_400_BAD_REQUEST)
        instance.worker = request.user

        try:
            instance.order_status = OrderStatus.objects.get(pk=2)
        except Exception as e:
            return Response({"detail": f"Ошибка изменения статуса заказа: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(instance)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ChangeOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = AssignOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'number'

    def partial_update(self, request, *args, **kwargs):
        def bad_request(err_text=None):
            err_text = err_text or ''
            return Response({"detail": f"Некорректно указан статус заказа, {err_text}"},
                            status=status.HTTP_400_BAD_REQUEST)

        def not_authorized():
            return Response({"detail": "Недостаточно прав пользователя для выполнения операции"},
                            status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        current_user = request.user
        new_order_status = None
        try:
            new_order_status = request.data.get('orderStatus')
        except Exception as e:
            return bad_request(e)
        print(f"instance = {instance}",
              f"instance.order_status.pk = {instance.order_status.pk}",
              f"instance.worker = {instance.worker}",
              f"instance.customer = {instance.customer}",
              f"current_user = {current_user}",
              f"current_user.role.name = {current_user.role.name}",
              f"new_order_status = {new_order_status}",
              sep='\n')

        match new_order_status:
            # case "2":  # Назначен исполнитель
            case "Назначен исполнитель":  # Назначен исполнитель

                if instance.order_status.pk != 1 or current_user.role.name != WORKER_ROLE_NAME:
                    return not_authorized()
                if instance.worker:
                    return Response({"detail": "Для этого заказа уже назначен исполнитель."},
                                    status=status.HTTP_400_BAD_REQUEST)
                instance.worker = current_user
            # case "3":  # Исполнитель приехал
            case "Исполнитель приехал":  # Исполнитель приехал
                if instance.order_status.pk != 2 or instance.worker != current_user:
                    return not_authorized()
            # case "4":  # Исполнитель работает
            case "Исполнитель работает":  # Исполнитель работает
                if instance.order_status.pk != 3 or instance.customer != current_user:
                    return not_authorized()
            # case "5":  # Заказ выполнен
            case "Заказ выполнен":  # Заказ выполнен
                if instance.order_status.pk != 4 or instance.customer != current_user:
                    return not_authorized()
            # case "6":  # Заказ закрыт заказчиком
            case "Заказ закрыт заказчиком":  # Заказ закрыт заказчиком
                if instance.customer != current_user:
                    return not_authorized()
            case _:
                return bad_request(f"статус '{new_order_status}' не может быть установлен")

        try:
            # instance.order_status = OrderStatus.objects.get(pk=int(new_order_status))
            instance.order_status = OrderStatus.objects.get(name=new_order_status)
        except Exception as e:
            return Response({"detail": f"Ошибка изменения статуса заказа: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('pk')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return Order.objects.all()
        return Order.objects.filter(pk=pk)

    @action(detail=False, methods=['post'], url_path='create',
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
    permission_classes = [permissions.IsAuthenticated, IsWorker]
    serializer_class = OpenOrderSerializer

    # возврат пустого словаря, если проверка на роль не проходит
    # заменено на permission_class IsWorker
    # def get(self, request, *args, **kwargs):
    #     user = self.request.user
    #     if user.role.name == WORKER_ROLE_NAME:
    #         return super().get(request, *args, **kwargs)
    #     return Response({})


# class CreateOrderView(generics.CreateAPIView):
#     serializer_class = CreateOrderSerializer
#     permission_classes = [permissions.IsAuthenticated]
