from django.urls import path
from . import views

urlpatterns = [
    path('tables/', views.TableListView.as_view(), name='table_list'),
    path('tables/<int:pk>/', views.TableDetailView.as_view(), name='table_detail'),
    path('menu-items/', views.MenuItemListView.as_view(), name='menu_item_list'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu_item_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
