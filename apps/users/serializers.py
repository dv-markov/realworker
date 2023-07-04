# from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Role, CustomUser, UserProfile, GeoData, Country, City, Category, Specialization, Qualification
from .utils import flatten_json


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.StringRelatedField()
    city = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        # fields = ['url', 'id', 'name', 'city', 'username', 'email', 'role']
        fields = ['id', 'name', 'city', 'username', 'email', 'role']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['city']:
            data['city'] = instance.city.name
        if data['role']:
            data['role'] = instance.role.name
        return data


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = "__all__"


class GeoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoData
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    specializations = serializers.StringRelatedField(many=True)
    qualifications = serializers.StringRelatedField(many=True)
    lastActive = serializers.CharField(source="last_active")
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id',
                  'user',
                  'country',
                  'specializations',
                  'qualifications',
                  'photo',
                  'company',
                  'position',
                  'lastActive',
                  'messages']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = instance.country.name
        data['specializations'] = [spec.name for spec in instance.specializations.all()]
        data['qualifications'] = [qual.name for qual in instance.qualifications.all()]
        data = flatten_json(data, flatten_lists=False)
        return data


class CustomerDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    city = serializers.CharField(source='user.city')
    email = serializers.CharField(source='user.email')
    phone = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ["name", "middleName", "surname", "city", "position", "email", "phone"]
