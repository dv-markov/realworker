from rest_framework import serializers
from .models import File, Chat, OrderStatus, Order
from apps.users.models import Category, Qualification, Specialization  # , GeoData
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
    # address = serializers.CharField(source='address.__str__')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    worker = serializers.SerializerMethodField()
    dateTime = serializers.CharField(source='date_time')
    orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = ["number", "description", "address", "category", "specialization", "qualification", "worker",
                  "dateTime", "orderStatus"]

    def get_worker(self, obj):
        worker = obj.worker
        if worker is not None:
            return worker.name
        return None


class WorkerOrderSerializer(serializers.ModelSerializer):
    # address = serializers.CharField(source='address.__str__')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    customer = serializers.CharField(source='customer.name')
    dateTime = serializers.CharField(source='date_time')
    orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = ["number", "description", "address", "category", "specialization", "qualification", "customer",
                  "dateTime", "orderStatus"]


class OpenOrderSerializer(serializers.ModelSerializer):
    # address = serializers.CharField(source='address.__str__')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    customer = serializers.CharField(source='customer.name')
    dateTime = serializers.CharField(source='date_time')
    orderStatus = serializers.CharField(source='order_status.name')
    geoLat = serializers.CharField(source='geo_lat')
    geoLon = serializers.CharField(source='geo_lon')

    class Meta:
        model = Order
        fields = ["number", "address", "category", "specialization", "qualification", "customer", "dateTime",
                  "orderStatus", "price", "geoLat", "geoLon"]


class OrderDetailSerializer(serializers.ModelSerializer):
    dateTime = serializers.CharField(source='date_time')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    customer = serializers.CharField(source='customer.name')
    # worker = serializers.SerializerMethodField()
    # orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = ["address", "dateTime", "category", "specialization", "qualification", "description",
                  "price", "customer"]

    # @staticmethod
    # def get_worker(obj):
    #     worker = obj.worker
    #     if worker:
    #         return worker.name


class AssignOrderSerializer(serializers.ModelSerializer):
    dateTime = serializers.CharField(source='date_time')
    category = serializers.CharField(source='category.name')
    specialization = serializers.CharField(source='specialization.name')
    qualification = serializers.CharField(source='qualification.name')
    customer = serializers.CharField(source='customer.name')
    worker = serializers.SerializerMethodField()
    orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = ["address", "dateTime", "category", "specialization", "qualification", "description",
                  "price", "customer", "worker", "orderStatus"]

    @staticmethod
    def get_worker(obj):
        worker = obj.worker
        if worker:
            return worker.name


class CreateOrderSerializer(serializers.ModelSerializer):
    pass


class OrderCreateSerializer(serializers.Serializer):
    address = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    specialization = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all())
    qualification = serializers.PrimaryKeyRelatedField(queryset=Qualification.objects.all())
    dateTime = serializers.CharField(required=False)
    description = serializers.CharField()
    # files = serializers.ListField(child=serializers.FileField(), required=False)
    geoLat = serializers.CharField(required=False)
    geoLon = serializers.CharField(required=False)
    # orderStatus = serializers.PrimaryKeyRelatedField(queryset=OrderStatus.objects.all())

    # dateTime = serializers.DateTimeField(source='date_time', required=False)
    # orderStatus = serializers.CharField(source='order_status.name', required=False)
    #
    # class Meta:
    #     model = Order
    #     fields = ["number",
    #               "category",
    #               "specialization",
    #               "qualification",
    #               "address",
    #               "geoLat",
    #               "geoLon",
    #               "dateTime",
    #               "description",
    #               "price",
    #               "customer",
    #               "worker",
    #               "orderStatus"
    #               ]

    def create(self, validated_data):
        # Check if the user has the "customer" role
        user = self.context['request'].user
        if user.role.name != 'customer':
            raise serializers.ValidationError("Only customers can create orders.")

        # Extract validated data
        address = validated_data.get('address')
        category = validated_data.get('category')
        specialization = validated_data.get('specialization')
        qualification = validated_data.get('qualification')
        date_time = validated_data.get('dateTime')
        description = validated_data.get('description')
        # files = validated_data.get('files', [])
        geo_lat = validated_data.get('geoLat')
        geo_lon = validated_data.get('geoLon')
        order_status = OrderStatus.objects.get(pk=1)

        # Create the order
        order = Order.objects.create(
            address=address,
            category=category,
            specialization=specialization,
            qualification=qualification,
            date_time=date_time,
            description=description,
            geo_lat=geo_lat,
            geo_lon=geo_lon,
            customer=self.context['request'].user,  # Assign the current user as the customer
            order_status=order_status,  # Set the initial order status
            price=qualification.price
        )

        # Add files to the order
        # for file in files:
        #     File.objects.create(file=file, order=order)

        return order

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data.pop('id', None)
    #     return data


class OrderSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    # specialization = serializers.StringRelatedField()
    # qualification = serializers.StringRelatedField()
    # address = GeoDataSerializer()
    # customer = serializers.StringRelatedField()
    # worker = serializers.StringRelatedField()
    # order_status = serializers.StringRelatedField()
    # number = serializers.CharField(read_only=True)

    # files = serializers.StringRelatedField(many=True)
    # chats = serializers.StringRelatedField(many=True)

    geoLat = serializers.CharField(source='geo_lat', required=False)
    geoLon = serializers.CharField(source='geo_lon', required=False)
    dateTime = serializers.CharField(source='date_time', required=False)
    # address = serializers.CharField(source='address.__str__')
    orderStatus = serializers.CharField(source='order_status.name')
    # orderStatus = serializers.CharField(source='order_status.name')

    class Meta:
        model = Order
        fields = [# "id",
                  "number",
                  "category",
                  "specialization",
                  "qualification",
                  "address",
                  "geoLat",
                  "geoLon",
                  "dateTime",
                  "description",
                  # "files",
                  "price",
                  # "chats",
                  "customer",
                  "worker",
                  "orderStatus"
                  ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.name
        data['specialization'] = instance.specialization.name
        data['qualification'] = instance.qualification.name
        # data['address'] = [f"{k}: {v}" for k, v in list(instance.address.__dict__.items())[2:]]
        # data['files'] = [f.file_url for f in instance.files.all()]
        # data['chats'] = [chat.name for chat in instance.chats.all()]
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

