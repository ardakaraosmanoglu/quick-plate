from django.db import models

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
    options = models.JSONField(default=dict)  # Ensure options are stored as JSON

    def __str__(self):
        return self.name
    
class Order(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_options = models.JSONField(default=dict, blank=True, null=True)  # Selected options stored as JSON
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Preparing', 'Preparing'), ('Ready', 'Ready'), ('Served', 'Served')], default='Preparing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity}"
