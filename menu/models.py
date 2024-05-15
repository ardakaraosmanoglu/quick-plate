from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    options = models.JSONField(default=dict, blank=True, null=True)  # Assuming options are stored as JSON

    def __str__(self):
        return self.name

class Order(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Preparing', 'Preparing'), ('Ready', 'Ready'), ('Served', 'Served')], default='Preparing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity}"