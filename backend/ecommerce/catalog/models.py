# backend/ecommerce/catalog/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image       = models.ImageField(upload_to="product_images/", blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user      = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user.username})"


class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity}× {self.product.name}"


class Order(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total      = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)  # unit price at time of purchase

    def __str__(self):
        return f"{self.quantity}× {self.product.name} (order #{self.order.id})"
