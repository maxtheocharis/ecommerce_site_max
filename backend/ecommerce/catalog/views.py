# backend/ecommerce/catalog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import SignUpForm  # Adjust import if your SignUpForm lives elsewhere


def product_list(request):
    """
    Show all products on the homepage.
    """
    products = Product.objects.all()
    return render(request, "catalog/index.html", {"products": products})


def product_detail(request, pk):
    """
    Show a single product’s details.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


@login_required
def view_cart(request):
    """
    Display the logged‐in user’s cart with all items and subtotals.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = []
    total = 0

    for ci in cart.items.select_related("product"):
        subtotal = ci.product.price * ci.quantity
        items.append({
            "id":       ci.id,
            "product":  ci.product,
            "quantity": ci.quantity,
            "price":    ci.product.price,
            "subtotal": subtotal,
        })
        total += subtotal

    return render(request, "catalog/cart.html", {
        "items": items,
        "total": total,
    })


@login_required
def update_cart_item(request, pk):
    """
    Handle “Update” or “Remove” actions from the cart page.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

    if request.method == "POST":
        if "remove" in request.POST:
            cart_item.delete()
        else:
            try:
                new_qty = int(request.POST.get("quantity", cart_item.quantity))
            except ValueError:
                new_qty = cart_item.quantity

            if new_qty <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = new_qty
                cart_item.save()

    return redirect("view_cart")


@login_required
def checkout(request):
    """
    Show a summary of the cart with a “Confirm” button.
    On POST, create an Order + OrderItems, then clear the cart.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = []
    total = 0

    for ci in cart.items.select_related("product"):
        subtotal = ci.product.price * ci.quantity
        items.append({
            "id":       ci.id,
            "product":  ci.product,
            "quantity": ci.quantity,
            "price":    ci.product.price,
            "subtotal": subtotal,
        })
        total += subtotal

    if request.method == "POST":
        # Create an Order
        order = Order.objects.create(user=request.user, total=total)
        # Create its OrderItems
        for ci in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                price=ci.product.price
            )
        # Clear the cart
        cart.items.all().delete()
        return redirect("order_thankyou")

    return render(request, "catalog/checkout.html", {
        "items": items,
        "total": total,
    })


@login_required
def order_thankyou(request):
    """
    “Thank you for your order” page.
    """
    return render(request, "catalog/thank_you.html")


def signup(request):
    """
    Simple sign‐up view: show form, save, then log in and redirect.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})
