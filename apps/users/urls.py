from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r'role', views.RoleViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'specializations', views.SpecializationViewSet)
router.register(r'qualifications', views.QualificationViewSet)
router.register(r'geodatas', views.GeoDataViewSet)

urlpatterns = [
    path("role/", views.RoleView.as_view(), name="role-name"),
    path("", include(router.urls)),
]
