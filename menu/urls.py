from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet, OrderViewSet, menu_view, item_detail_view
from . import views

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('menu/', menu_view, name='menu'),
    path('menu/item/<int:pk>/', item_detail_view, name='item_detail'),
    path('order-confirmation/', views.order_confirmation_view, name='order_confirmation'),
]

# For serving media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

