from django.contrib.auth.models import User, Group
from .models import CustomUser, UserProfile
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'name', 'city', 'username', 'email', 'role']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = instance.role.name
        return data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    specializations = serializers.StringRelatedField(many=True)
    qualifications = serializers.StringRelatedField(many=True)
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = instance.country.name
        data['city'] = instance.city.name
        data['specializations'] = [spec.name for spec in instance.specializations.all()]
        data['qualifications'] = [qual.name for qual in instance.qualifications.all()]
        return data
