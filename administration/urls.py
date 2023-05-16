from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path


app_name = 'administration'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='administration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='administration/logout.html'), name='logout'),
    path('', views.index, name='index'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_create/', views.order_create, name='order_create'),
    path('order_delete/<int:order_id>', views.order_delete, name='order_delete'),
    path('order_item_edit/<int:order_item_id>', views.order_item_edit, name='order_item_edit'),
    path('order_item_delete/<int:order_item_id>', views.order_item_delete, name='order_item_delete'),
    path('order_item_create/<int:order_id>', views.order_item_create, name='order_item_create'),
    path('gallery_items/', views.gallery_items, name='gallery_items'),
    path('gallery_item_create/', views.gallery_item_create, name='gallery_item_create'),
    path('gallery_item_edit/<int:gallery_item_id>', views.gallery_item_edit, name='gallery_item_edit'),
    path('gallery_item_delete/<int:gallery_item_id>', views.gallery_item_delete, name='gallery_item_delete'),
    path('gallery_item_detail/<int:gallery_item_id>', views.gallery_item_detail, name='gallery_item_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)