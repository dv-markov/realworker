"""realworker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import include, path, re_path
from rest_framework import routers
from apps.users import views
from django.conf import settings
from django.conf.urls.static import static
# from apps.users import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'orders', views.OrderViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # ссылка на модели приложения orders
    path("api/orders/", include("apps.orders.urls")),

    # ссылка на дополнительные модели приложения users
    path("api/users/", include("apps.users.urls")),

    # admin access
    path('api/admin/', admin.site.urls),

    # userprofile
    path('api/userprofile/', views.UserProfileView.as_view()),

    # rest_framework
    path('api/', include(router.urls)),
    # path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # djoser
    # path('api/v1/auth/', include('djoser.urls')),  # djoser
    re_path(r'^api/auth/', include('djoser.urls')),  # djoser
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),  # djoser

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

