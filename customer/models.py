from django.db import models

class Table(models.Model):
    number = models.CharField(max_length=10)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
