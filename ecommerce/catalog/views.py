from django.shortcuts      import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models               import Product, Cart, CartItem
from django.shortcuts      import render, redirect
from django.contrib.auth   import login
from .forms                import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = SignUpForm()
    return render(request, 'catalog/signup.html', {'form': form})



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


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    # Build a list of items with computed subtotals
    items = []
    total = 0
    for ci in cart.items.select_related('product'):
        subtotal = ci.product.price * ci.quantity
        items.append({
            'product': ci.product,
            'quantity': ci.quantity,
            'price':    ci.product.price,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total': total,
    })