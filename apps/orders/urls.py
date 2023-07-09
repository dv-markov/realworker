from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'files', views.FileViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'orderstatuses', views.OrderStatusViewSet)
router.register(r'', views.OrderViewSet)

urlpatterns = [
    path("my/", views.MyOrderListView.as_view(), name="my-orders"),
    path("open/", views.OpenOrderListView.as_view(), name="open-orders"),
    path("details/<str:number>/", views.ShowOrderDetailsView.as_view(), name="order-details"),
    path("assign/<str:number>/", views.AssignOrderView.as_view(), name="assign-order"),
    path("change-status/<str:number>/", views.ChangeOrderStatusView.as_view(), name="change-order-status"),
    path("remove-worker/<str:number>/", views.RemoveWorkerFromOrderView.as_view(), name="remove-worker-from-order"),
    path("", include(router.urls)),
]
