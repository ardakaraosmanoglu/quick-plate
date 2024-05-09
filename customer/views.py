from django.views import generic
from django.urls import reverse_lazy
from .models import Table, MenuItem, Order

class TableListView(generic.ListView):
    model = Table
    template_name = 'tables/table_list.html'
    context_object_name = 'tables'

class TableDetailView(generic.DetailView):
    model = Table
    template_name = 'tables/table_detail.html'

class MenuItemListView(generic.ListView):
    model = MenuItem
    template_name = 'menu_items/menu_item_list.html'
    context_object_name = 'menu_items'

class MenuItemDetailView(generic.DetailView):
    model = MenuItem
    template_name = 'menu_items/menu_item_detail.html'

class OrderListView(generic.ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
