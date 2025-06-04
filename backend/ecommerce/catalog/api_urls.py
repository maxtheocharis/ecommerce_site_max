# backend/ecommerce/catalog/api_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, CartViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
