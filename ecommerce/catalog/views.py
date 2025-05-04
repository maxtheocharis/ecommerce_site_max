from django.shortcuts      import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models               import Product, Cart, CartItem

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/index1.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product, _ = get_object_or_404(Product, pk=pk), None
    cart, _    = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'catalog/cart.html', {'cart': cart})
