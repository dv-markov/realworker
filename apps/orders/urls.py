from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'files', views.FileViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'orderstatuses', views.OrderStatusViewSet)
router.register(r'', views.OrderViewSet)

urlpatterns = [
    path("my-orders/", views.MyOrderListView.as_view(), name="my-orders"),
    path("", include(router.urls)),
]
