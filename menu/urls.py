from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet, OrderViewSet, menu_view, item_detail_view

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('menu/', menu_view, name='menu'),
    path('menu/item/<int:pk>/', item_detail_view, name='item_detail'),
]
