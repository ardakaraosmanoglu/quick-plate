### APPENDICES

#### A. Instructions for Installing the System

The steps to be taken to run this project are as follows:

1. **Install Python and Django:**
   - Ensure you have Python installed on your system. If not, download and install it from [python.org](https://www.python.org/).
   - Install Django using pip: `pip install django`.

2. **Set Up the Project:**
   - Clone the project repository from the source.
   - Navigate to the project directory: `cd QuickPlate`.

3. **Set Up the Virtual Environment:**
   - Create a virtual environment: `python -m venv env`.
   - Activate the virtual environment:
     - On Windows: `env\Scripts\activate`
     - On macOS/Linux: `source env/bin/activate`

4. **Install Dependencies:**
   - Install required dependencies: `pip install -r requirements.txt`.

5. **Configure the Database:**
   - Open `settings.py` located in the `quickplate` directory.
   - Ensure the `DATABASES` setting is configured to use SQLite:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': BASE_DIR / "db.sqlite3",
         }
     }
     ```

6. **Apply Migrations:**
   - Apply database migrations: `python manage.py migrate`.

7. **Create a Superuser:**
   - Create an admin user for the Django admin interface: `python manage.py createsuperuser`.

8. **Run the Development Server:**
   - Start the development server: `python manage.py runserver`.

9. **Access the Application:**
   - Open your web browser and go to `http://127.0.0.1:8000`.

10. **Configure Media and Static Files:**
    - Ensure you have the appropriate directories for media and static files. Update `settings.py` as needed.

#### B. Code for the System

##### B.1 `views.py`
```python
from rest_framework import viewsets
from .models import Category, MenuItem, Order
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MenuItemOptionForm
from decimal import Decimal
from django.db.models import Q

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
    query = request.GET.get('q', '')
    if query:
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(details__icontains=query)
        )
    else:
        menu_items = MenuItem.objects.all()
    categories = Category.objects.all()
    return render(request, 'menu.html', {'categories': categories, 'menu_items': menu_items, 'query': query})

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
            return redirect('order_confirmation')
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

def checkout_view(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method:
            return redirect('payment_success')  # Redirect to a payment success page
    return render(request, 'checkout.html')

def payment_success_view(request):
    return render(request, 'payment_success.html')
```

##### B.2 `models.py`
```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_images/')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    details = models.TextField(blank=True, null=True)
    options = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_options = models.JSONField(default=dict, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Preparing', 'Preparing'), ('Ready', 'Ready'), ('Served', 'Served')], default='Preparing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity}"
```

##### B.3 `urls.py`
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet, OrderViewSet, menu_view, item_detail_view, order_list_view, customer_order_view, checkout_view, payment_success_view
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
    path('orders/', order_list_view, name='order_list'),
    path('customer-orders/', customer_order_view, name='customer_orders'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment-success/', payment_success_view, name='payment_success'),
]

# For serving media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
```

##### B.4 `serializers.py`
```python
from rest_framework import serializers
from .models import Category, MenuItem, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
```

##### B.5 `forms.py`
```python
from django import forms

class MenuItemOptionForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', {})
        super(MenuItemOptionForm, self).__init__(*args, **kwargs)
        if options:
            for option, choices in options.items():
                self.fields[option] = forms.ChoiceField(
                    choices=[(choice, choice) for choice in choices],
                    label=option
                )
```

##### B.6 `admin.py`
```python
from django.contrib import admin
from .models import Category, MenuItem, Order

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
```
