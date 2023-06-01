from django.contrib.auth.models import Group
from .models import CustomUser, UserProfile, Order, GeoData
from rest_framework import serializers
from .utils import flatten_json


class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.StringRelatedField()
    city = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        # fields = ['url', 'id', 'name', 'city', 'username', 'email', 'role']
        fields = ['name', 'city', 'username', 'email', 'role']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['city']:
            data['city'] = instance.city.name
        if data['role']:
            data['role'] = instance.role.name
        return data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class GeoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoData
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    specializations = serializers.StringRelatedField(many=True)
    qualifications = serializers.StringRelatedField(many=True)
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user',
                  'country',
                  'specializations',
                  'qualifications',
                  'photo',
                  'company',
                  'position',
                  'last_active',
                  'messages']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = instance.country.name
        data['specializations'] = [spec.name for spec in instance.specializations.all()]
        data['qualifications'] = [qual.name for qual in instance.qualifications.all()]
        data = flatten_json(data, flatten_lists=False)
        return data


class OrderSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    specialization = serializers.StringRelatedField()
    qualification = serializers.StringRelatedField()
    address = GeoDataSerializer()
    files = serializers.StringRelatedField(many=True)
    chats = serializers.StringRelatedField(many=True)
    customer = serializers.StringRelatedField()
    worker = serializers.StringRelatedField()
    order_status = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["number",
                  "category",
                  "specialization",
                  "qualification",
                  "address",
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
        data['files'] = [f.file_url for f in instance.files.all()]
        data['chats'] = [chat.name for chat in instance.chats.all()]
        data['customer'] = instance.customer.name
        data['worker'] = instance.worker.name
        data['order_status'] = instance.order_status.name
        return data
