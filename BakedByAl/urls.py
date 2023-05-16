from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name="BakedByAl"
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path("gallery/", views.gallery, name="gallery"),
    path("cart/", views.cart, name="cart"),
    path("order-confirmation/", views.order_confirmation, name="order-confirmation"),
    path("contact/", views.contact, name="contact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)