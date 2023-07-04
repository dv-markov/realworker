from django.shortcuts import render

from django.contrib.auth.models import Group
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from .serializers import RoleSerializer, UserSerializer, CountrySerializer, CitySerializer, CategorySerializer, \
    SpecializationSerializer, QualificationSerializer, GeoDataSerializer, UserProfileSerializer, \
    CustomerDetailSerializer

from .models import CustomUser, Country, City, Category, Specialization, Qualification, GeoData, UserProfile


CUSTOMER_ROLE_NAME = "customer"
WORKER_ROLE_NAME = "worker"


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_name = request.user.name if request.user else None
        role_name = request.user.role.name if request.user.role else None

        return Response({'userName': user_name, 'roleName': role_name})


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all().order_by('pk')
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class GeoDataViewSet(viewsets.ModelViewSet):
    queryset = GeoData.objects.all()
    serializer_class = GeoDataSerializer


class UserProfileView(generics.ListAPIView):
    # queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        print(current_user)
        return UserProfile.objects.filter(user=current_user)
        # return UserProfile.objects.get(user__username=current_user)


class UserDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.role.name == CUSTOMER_ROLE_NAME:
            return CustomerDetailSerializer
        # elif user.role.name == WORKER_ROLE_NAME:
        #     return WorkerOrderSerializer
