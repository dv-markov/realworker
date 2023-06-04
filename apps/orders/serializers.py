from rest_framework import serializers
from .models import File, Chat, OrderStatus, Order


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

    class Meta:
        model = Order
        fields = ["id",
                  "number",
                  "category",
                  "specialization",
                  "qualification",
                  "address",
                  "geo_lat",
                  "geo_lon",
                  "date_time",
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
        data['files'] = [f.file_url for f in instance.files.all()]
        data['chats'] = [chat.name for chat in instance.chats.all()]
        data['customer'] = instance.customer.name
        data['worker'] = instance.worker.name
        data['order_status'] = instance.order_status.name
        return data

