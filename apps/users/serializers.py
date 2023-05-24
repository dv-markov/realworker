from django.contrib.auth.models import User, Group
from .models import CustomUser, UserProfile
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
