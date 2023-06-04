from django.contrib import admin
from .models import OrderStatus, Order, File, Chat


# Register your models here.
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(File)
admin.site.register(Chat)
