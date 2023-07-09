from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'', views.NotificationViewSet)

urlpatterns = [
    path("types/", views.NotificationTypeListView.as_view(), name="notification-types"),
    path("statuses/", views.NotificationStatusListView.as_view(), name="notification-statuses"),
    path("", include(router.urls)),
]