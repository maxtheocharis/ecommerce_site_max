# backend/ecommerce/catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Home / product list
    path("", views.product_list, name="product_list"),

    # Product detail
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    # View Cart (requires login)
    path("cart/", views.view_cart, name="view_cart"),

    # Update or Remove a single CartItem (from cart page)
    path("cart/update/<int:pk>/", views.update_cart_item, name="update_cart_item"),

    # Checkout summary → on POST, creates Order + OrderItems
    path("checkout/", views.checkout, name="checkout"),

    # Thank you page after placing an order
    path("thank-you/", views.order_thankyou, name="order_thankyou"),
]
