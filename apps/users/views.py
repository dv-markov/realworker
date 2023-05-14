from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer, UserProfileSerializer
from .models import CustomUser, UserProfile


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('pk')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileView(generics.ListAPIView):
    # queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        current_user = self.request.user
        print(current_user)
        return UserProfile.objects.filter(user=current_user)
        # return UserProfile.objects.get(user__username=current_user)

    permission_classes = [permissions.IsAuthenticated]