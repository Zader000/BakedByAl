from django.contrib import admin
from .models import GalleryItem, OrderItem, Order

# Register your models here.
admin.site.register(GalleryItem)
admin.site.register(OrderItem)
admin.site.register(Order)