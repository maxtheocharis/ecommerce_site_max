from django.db import models
from django.conf import settings

class Product(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image       = models.ImageField(upload_to='products/')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
