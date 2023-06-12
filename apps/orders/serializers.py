from rest_framework import serializers
from .models import File, Chat, OrderStatus, Order
import datetime


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = "__all__"


class CustomerOrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address.__str__')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    worker = serializers.CharField(source='worker.name')
    dateTime = serializers.DateTimeField(source='date_time')
    orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = ["number", "address", "category", "specialization", "qualification", "worker", "dateTime",
                  "orderStatus"]


class WorkerOrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address.__str__')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    customer = serializers.CharField(source='customer.name')
    dateTime = serializers.DateTimeField(source='date_time')
    orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = ["number", "address", "category", "specialization", "qualification", "customer", "dateTime",
                  "orderStatus"]


class OpenOrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address.__str__')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    customer = serializers.CharField(source='customer.name')
    dateTime = serializers.DateTimeField(source='date_time')
    orderStatus = serializers.CharField(source='order_status.name')
    geoLat = serializers.CharField(source='geo_lat')
    geoLon = serializers.CharField(source='geo_lon')

    class Meta:
        model = Order
        fields = ["number", "address", "category", "specialization", "qualification", "customer", "dateTime",
                  "orderStatus", "price", "geoLat", "geoLon"]


class OrderSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    # specialization = serializers.StringRelatedField()
    # qualification = serializers.StringRelatedField()
    # address = GeoDataSerializer()
    files = serializers.StringRelatedField(many=True)
    chats = serializers.StringRelatedField(many=True)
    # customer = serializers.StringRelatedField()
    # worker = serializers.StringRelatedField()
    # order_status = serializers.StringRelatedField()
    # number = serializers.CharField(read_only=True)

    geoLat = serializers.CharField(source='geo_lat')
    geoLon = serializers.CharField(source='geo_lon')
    dateTime = serializers.StringRelatedField(source='date_time')
    # orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = ["id",
                  "number",
                  "category",
                  "specialization",
                  "qualification",
                  "address",
                  "geoLat",
                  "geoLon",
                  "dateTime",
                  "description",
                  "files",
                  "price",
                  "chats",
                  "customer",
                  "worker",
                  "order_status"
                  ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.name
        data['specialization'] = instance.specialization.name
        data['qualification'] = instance.qualification.name
        data['address'] = [f"{k}: {v}" for k, v in list(instance.address.__dict__.items())[2:]]
        # data['address'] = instance.address.__str__
        data['files'] = [f.file_url for f in instance.files.all()]
        data['chats'] = [chat.name for chat in instance.chats.all()]
        data['customer'] = instance.customer.name
        if data['worker']:
            data['worker'] = instance.worker.name
        return data

    # def create(self, validated_data):
    #     category_data = validated_data.pop('category')
    #     specialization_data = validated_data.pop('specialization')
    #     qualification_data = validated_data.pop('qualification')
    #     customer_data = validated_data.pop('customer')
    #     worker_data = validated_data.pop('worker')
    #
    #     order = Order.objects.create(**validated_data)
    #     order.category.set(category_data)
    #     order.specialization.set(specialization_data)
    #     order.qualification.set(qualification_data)
    #     order.customer = customer_data
    #     order.worker = worker_data
    #     order.save()
    #
    #     return order

    # def create(self, validated_data):
    #     current_year = datetime.datetime.now().year % 100
    #     max_order = Order.objects.order_by('-number').first()
    #     if max_order:
    #         max_order_number = int(max_order.number[-4:])
    #         new_order_number = max_order_number + 1
    #     else:
    #         new_order_number = 1
    #     validated_data['number'] = f"{current_year:02d}-{new_order_number:04d}"
    #     return super().create(validated_data)

