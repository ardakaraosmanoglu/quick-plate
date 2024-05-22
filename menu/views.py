#views.py 

from rest_framework import viewsets
from .models import Category, MenuItem, Order
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MenuItemOptionForm
from decimal import Decimal

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
def order_confirmation_view(request):
    return render(request, 'order_confirmation.html')

def menu_view(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'categories': categories, 'menu_items': menu_items})

def item_detail_view(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemOptionForm(request.POST, options=item.options or {})
        if form.is_valid():
            selected_options = {key: value for key, value in form.cleaned_data.items() if key != 'quantity'}
            quantity = form.cleaned_data.get('quantity', 1)
            Order.objects.create(
                menu_item=item,
                quantity=quantity,
                selected_options=selected_options
            )
            return redirect('order_confirmation')  # Redirect to an order confirmation page or another page
    else:
        form = MenuItemOptionForm(options=item.options or {})
    return render(request, 'item_detail.html', {'item': item, 'form': form})

def order_list_view(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def customer_order_view(request):
    orders = Order.objects.all()
    sub_total = sum(order.menu_item.price * order.quantity for order in orders)
    vat_rate = Decimal('0.10')  # VAT rate as a Decimal
    vat = sub_total * vat_rate
    total = sub_total + vat
    return render(request, 'customer_orders.html', {
        'orders': orders,
        'sub_total': sub_total,
        'vat': vat,
        'total': total
    })
