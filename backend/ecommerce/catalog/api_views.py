# backend/ecommerce/catalog/api_views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET   /api/products/       → list all products
    GET   /api/products/{pk}/  → retrieve a single product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class CartViewSet(viewsets.ViewSet):
    """
    - GET    /api/cart/               → return the current user’s cart
    - POST   /api/cart/add_item/      → add or increment quantity
    - PATCH  /api/cart/{item_pk}/     → update a single CartItem’s quantity or delete it
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # GET /api/cart/
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add_item")
    def add_item(self, request):
        """
        POST /api/cart/add_item/
        JSON payload: { "product_id": <int>, "quantity": <int> } (quantity optional, default 1)
        """
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if product_id is None:
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = max(quantity, 1)
        else:
            cart_item.quantity += quantity

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
        PATCH /api/cart/{item_pk}/
        JSON payload: { "quantity": <int> }
        If quantity ≤ 0, this deletes the CartItem.
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        quantity = int(request.data.get("quantity", cart_item.quantity))
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
