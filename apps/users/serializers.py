from django.contrib.auth.models import User, Group
from .models import CustomUser, UserProfile
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'name', 'city', 'username', 'email', 'role']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
